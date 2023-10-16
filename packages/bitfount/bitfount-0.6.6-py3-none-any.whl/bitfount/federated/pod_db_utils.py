"""Utilities for the Pod results database."""
from datetime import datetime
import hashlib
import os.path
import sqlite3
from sqlite3 import Connection
from typing import List, Optional, Sequence, cast

import numpy as np
import pandas as pd
import pandas._libs.lib as lib

from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.types import DataSplit
from bitfount.federated import _get_federated_logger
from bitfount.federated.exceptions import PodDBError
from bitfount.federated.types import SerializedProtocol

logger = _get_federated_logger(__name__)

# ######## ADAPTED FROM `pandas.io.sql.py` (CAN'T BE IMPORTED) #########

# ---- SQL without SQLAlchemy ---
# sqlite-specific sql strings and handler class
# dictionary used for readability purposes
_SQL_TYPES = {
    "string": "TEXT",
    "floating": "REAL",
    "integer": "INTEGER",
    "datetime": "TIMESTAMP",
    "date": "DATE",
    "time": "TIME",
    "boolean": "INTEGER",
}


def _sql_type_name(col: pd.Series) -> str:
    """Takes a pandas column and returns the appropriate SQLite dtype."""
    # Infer type of column, while ignoring missing values.
    # Needed for inserting typed data containing NULLs, GH 8778.
    col_type = lib.infer_dtype(col, skipna=True)

    if col_type == "timedelta64":
        logger.warning(
            "the 'timedelta' type is not supported, and will be "
            "written as integer values (ns frequency) to the database.",
        )
        col_type = "integer"

    elif col_type == "datetime64":
        col_type = "datetime"

    elif col_type == "empty":
        col_type = "string"

    elif col_type == "complex":
        raise ValueError("Complex datatypes not supported")

    if col_type not in _SQL_TYPES:
        col_type = "string"

    return _SQL_TYPES[col_type]


#########################################################################


def _add_data_to_pod_db(
    pod_name: str,
    data: pd.DataFrame,
    table_name: str,
    file_iterable_datasource: bool = False,
) -> None:
    """Adds the data in the provided dataframe to the pod database.

    Args:
        pod_name: The name of the pod the database is associated with.
        data: Dataframe to be added to the database.
        table-name: The table from the datasource corresponding to the data.

    Raises:
        ValueError: If there are clashing column names in the datasource
            and the pod database.
    """
    con = sqlite3.connect(f"{pod_name}.sqlite")
    cur = con.cursor()
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # noqa: B950
    )
    con.commit()

    if "datapoint_hash" in data.columns:
        raise ValueError(
            "`datapoint_hash` not supported as column name in the datasource."
        )
    # Placeholder for the datapoint hash
    data["datapoint_hash"] = ""

    # sqlite transforms bool values to int, so we need to make sure that
    # they are the same in the df so the hashes match
    bool_cols = [col for col in data.columns if data[col].dtype == bool]
    # replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    data[bool_cols] *= 1
    # Remove ' from column names
    for col in data.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            data.rename(columns={col: col_text}, inplace=True)
    # Reindex to make sure all columns are filled otherwise
    # might have mismatches in columns for the FileSystemIterableSource
    # as different files can have different columns filled.
    data = data.reindex(sorted(data.columns), axis=1)
    hashed_list = []
    if not file_iterable_datasource:
        for _, row in data.iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    else:
        # Special case for file iterable datasources.
        # This is because if we reload the pod,
        # and check if records have been changed one by one,
        # the columns are likely to differ between single files.
        # Since we know that these column will always be part
        # of the datasource and good identifiers for the columns,
        # we only hash them instead of all features.
        for _, row in data[["_original_filename", "_last_modified"]].iterrows():
            hashed_list.append(hashlib.sha256(str(row).encode("utf-8")).hexdigest())
    data["datapoint_hash"] = hashed_list
    # read the db data for the datasource
    # Ignoring the security warning because the sql query is trusted and
    # the table is checked that it matches the datasource tables.
    existing_data: pd.DataFrame = pd.read_sql_query(
        f'SELECT * FROM "{table_name}"', con  # nosec hardcoded_sql_expressions
    )
    existing_cols_without_index = set(
        sorted(
            [i for i in existing_data.columns if i not in ["rowID", "datapoint_hash"]]
        )
    )
    # check if df is empty or if columns all columns are the same,
    # if not all the hashes will have to be recomputed
    if (
        not existing_data.empty
        and set(sorted(data.columns)) == existing_cols_without_index
    ):
        data = pd.concat(
            [
                data,
                existing_data.drop(
                    columns=["datapoint_hash", "rowID"], errors="ignore"
                ),
            ],
            join="outer",
            ignore_index=True,
        )
        data.drop_duplicates(inplace=True)
    else:
        cur = con.cursor()
        # replace table if columns are mismatched
        cur.execute(f"DROP TABLE '{table_name}'")
        cur.execute(f"""CREATE TABLE "{table_name}" ('rowID' INTEGER PRIMARY KEY)""")
        for col in data.columns:
            cur.execute(
                f"ALTER TABLE '{table_name}' ADD COLUMN '{col}' {_sql_type_name(data[col])}"  # noqa: B950
            )
    data.to_sql(table_name, con=con, if_exists="append", index=False)
    con.close()


def _add_file_iterable_datasource_to_db(
    pod_name: str, datasource: FileSystemIterableSource, table_name: str
) -> None:
    """Adds the data from a FileIterableDatasource to the pod database.

    Args:
        pod_name: The name of the pod the database is associated with.
        datasource: FileIterableSource to be added to the database.
        table_name: The table from the datasource corresponding to the data.

    """
    # Steps:
    # 1. See if db exists and if any of the filenames are in the db.
    # 2. If any of the files are in the db, we check the timestamp for last modified.
    # 3. If current last modified timestamp for any of the files is different than
    #   the one in the database we add all of them to a list, and use get_data
    #   just on those filenames.
    con = sqlite3.connect(f"{pod_name}.sqlite")
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cur.fetchall()]
    if table_name not in tables:
        # Ignoring the security warning because the sql query is trusted and
        # the table is checked that it matches the datasource tables.
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS "{table_name}" ('rowID' INTEGER PRIMARY KEY)"""  # nosec # noqa: B950
        )
        con.commit()
    cursor = con.execute(
        f"SELECT * FROM '{table_name}'"  # nosec hardcoded_sql_expressions
    )
    column_list = list(map(lambda x: x[0], cursor.description))
    reload_db = False

    if len(column_list) == 1:
        # This means only column is the `rowId` and we need
        # to load the whole datasource.
        _add_data_to_pod_db(
            pod_name=pod_name,
            data=datasource.data.copy(),
            table_name=table_name,
            file_iterable_datasource=True,
        )
    else:
        pod_data = pd.read_sql(
            f'SELECT * FROM "{table_name}"', con  # nosec hardcoded_sql_expressions
        )
        for filename in datasource.file_names:
            # Check if filename is in the database:
            db_records = pod_data[pod_data["_original_filename"] == filename]
            if len(db_records) == 1:
                db_record = db_records.squeeze()
                # If the filename already in the db:
                # Check if last_modified timestamp matches the
                # date the file has been last modified.
                # pd.to_sql adds the microseconds as well,
                # so need to make sure that we parse properly
                # so we can compare the timestamps.
                db_last_modified = datetime.fromisoformat(db_record["_last_modified"])
                # Get timestamp
                modify_time = os.path.getmtime(filename)
                modify_date = datetime.fromtimestamp(modify_time).isoformat()
                if modify_date == db_last_modified:
                    # If the last_modified timestamp matches the one in the db, continue
                    continue
                else:
                    # Get record from filename
                    updated_record = datasource._get_data(file_names=[filename])
                    _update_single_record_in_db(
                        updated_record=updated_record,
                        original_record=db_record,
                        table_name=table_name,
                        con=con,
                        cur=cur,
                    )
            elif len(db_records) == 0:
                new_record = datasource._get_data(file_names=[filename])
                # If the filename is not found in the database, it
                # means it is a new record, so we only need to
                # add that record to the db.
                _add_single_record_to_db(
                    new_record=new_record, table_name=table_name, con=con
                )
            else:  # this should not happen but `if` it does, we need to reload the whole db. # noqa: B950
                reload_db = True
                # exit the `for` loop since there is no point to continue
                # if we need to reload the database
                break
    if reload_db is True:
        _add_data_to_pod_db(
            pod_name=pod_name,
            data=datasource.data.copy(),
            table_name=table_name,
            file_iterable_datasource=True,
        )
    else:
        con.close()


def _add_single_record_to_db(
    new_record: pd.DataFrame, table_name: str, con: sqlite3.Connection
) -> None:
    """Adds a single record to the pod database."""
    bool_cols = [col for col in new_record.columns if new_record[col].dtype == bool]
    # SQLite transforms bool cols to int so we can update them here as well.
    new_record[bool_cols] *= 1

    # Remove ' from column names
    for col in new_record.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            new_record.rename(columns={col: col_text}, inplace=True)

    # Calculate hash
    new_record["datapoint_hash"] = hashlib.sha256(
        str(new_record[["_original_filename", "_last_modified"]].squeeze()).encode(
            "utf-8"
        )
    ).hexdigest()
    # Append the record to the db.
    new_record.to_sql(table_name, con=con, if_exists="append", index=False)


def _update_single_record_in_db(
    updated_record: pd.DataFrame,
    original_record: pd.Series,
    table_name: str,
    con: sqlite3.Connection,
    cur: sqlite3.Cursor,
) -> None:
    """Updates a single record in the pod_database."""
    # replace bools by their int value, as it will be done by
    # sqlite in the db anyway
    bool_cols = [
        col for col in updated_record.columns if updated_record[col].dtype == bool
    ]
    updated_record[bool_cols] *= 1

    # Remove ' from column names
    for col in updated_record.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            updated_record.rename(columns={col: col_text}, inplace=True)

    # calculate hash
    updated_record["datapoint_hash"] = hashlib.sha256(
        str(updated_record[["_original_filename", "_last_modified"]].squeeze()).encode(
            "utf-8"
        )
    ).hexdigest()
    for col, feature in updated_record.squeeze().items():
        # Note that double quotes need to be used  for `col`
        # below in case column name has spaces (quite common for DICOMs)
        query = f'UPDATE "{table_name}" SET "{col}"="{feature}" WHERE "rowID"={original_record["rowID"]}'  # noqa: B950 # nosec

        cur.execute(query)
        con.commit()


def _map_task_to_hash_add_to_db(
    serialized_protocol: SerializedProtocol, task_hash: str, project_db_con: Connection
) -> None:
    """Maps the task hash to the protocol and algorithm used.

    Adds the task to the task database if it is not already present.

    Args:
        serialized_protocol: The serialized protocol used for the task.
        task_hash: The hash of the task.
        project_db_con: The connection to the database.
    """
    algorithm_ = serialized_protocol["algorithm"]
    if not isinstance(algorithm_, Sequence):
        algorithm_ = [algorithm_]
    for algorithm in algorithm_:
        if "model" in algorithm:
            algorithm["model"].pop("schema", None)
            if algorithm["model"]["class_name"] == "BitfountModelReference":
                algorithm["model"].pop("hub", None)

    cur = project_db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: B950
    )
    data = pd.read_sql("SELECT * FROM 'task_definitions' ", project_db_con)
    if task_hash not in list(data["taskhash"]):
        logger.info("Adding task to task database")
        cur.execute(
            """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: B950
            (
                task_hash,
                serialized_protocol["class_name"],
                str(algorithm_),
            ),
        )
    else:
        logger.debug("Task already in task database")
    project_db_con.commit()


def _save_results_to_db(
    project_db_con: Connection,
    datasource: BaseSource,
    results: List[np.ndarray],
    run_on_new_data_only: bool,
    pod_identifier: str,
    show_datapoints_in_results_db: bool,
    task_hash: str,
    query: Optional[str] = None,
    table: Optional[str] = None,
) -> None:
    """Saves the results to the database.

    Args:
        project_db_con: The connection to the project database.
        datasource: The datasource used for the task.
        results: The results of the task.
        run_on_new_data_only: Whether the task was run on new data only. This is
            used to determine which rows of the data should be saved to the database.
        pod_identifier: The identifier of the pod.
        show_datapoints_in_results_db: Whether to show the datapoints in the results
            database.
        task_hash: The hash of the task.
        table: The table to get pod data from. Defaults to None.
        query: The query to get pod data from SQLDataView. Defaults to None.

    """
    logger.info("Saving results to database")
    # Convert results to string
    results_as_str = [str(item) for item in results]
    # Read in existing results from the relevant database table
    pod_db_con = sqlite3.connect(f"{pod_identifier.split('/')[1]}.sqlite")
    if table is not None:
        # Ignoring the security warning because the sql query is trusted and
        # the table is checked that it matches the datasource tables in
        # `get_pod_db_table_name`, which is how it gets passed to this function.
        pod_data = pd.read_sql(
            f'SELECT * FROM "{table}"', pod_db_con  # nosec hardcoded_sql_expressions
        )
    elif query is not None:
        pod_data = pd.read_sql(query, pod_db_con)
    else:
        pod_db_con.close()
        raise PodDBError("Either table name or query needs to be passed.")
    pod_db_con.close()

    # We only care about the test data since we don't log
    # anything in the database for validation or training data
    if datasource._test_idxs is None:
        if not datasource.iterable:
            raise ValueError("Datasource has no test set, cannot save results.")
        else:
            datasource = cast(FileSystemIterableSource, datasource)
            data_splitter = datasource.data_splitter or PercentageSplitter()
            filenames = data_splitter.get_filenames(datasource, DataSplit.TEST)
            run_data = datasource.data.loc[
                datasource.data["_original_filename"].isin(filenames)
            ].reset_index(drop=True)
    else:
        run_data = datasource.data.loc[datasource._test_idxs].reset_index(drop=True)
    # Remove ' from column names
    for col in run_data.columns:
        if "'" in col:
            col_text = col.replace("'", "`")
            run_data.rename(columns={col: col_text}, inplace=True)
    # pd.read_sql does not map all dtypes correctly,
    # so convert all datetime columns appropriately
    datetime_cols = [
        col for col in run_data.columns if run_data[col].dtype == "datetime64[ns]"
    ]
    for col in datetime_cols:
        pod_data[col] = pd.to_datetime(pod_data[col])
    # Convert results to string
    # mypy_reason: This access is completely fine, the pandas stubs are overzealous
    run_data.loc[:, "results"] = results_as_str  # type: ignore[index] # Reason: see comment # noqa: B950
    columns = list(pod_data.columns)
    columns.remove("datapoint_hash")
    if isinstance(datasource, FileSystemIterableSource):
        data_w_hash = pd.merge(
            pod_data,
            run_data,
            how="outer",
            left_on=["_original_filename", "_last_modified"],
            right_on=["_original_filename", "_last_modified"],
            indicator=True,
            suffixes=[None, "_x"],
        ).loc[lambda x: x["_merge"] == "both"]
        data_w_hash = data_w_hash[columns + ["datapoint_hash", "results"]]
        columns.remove("rowID")
    else:
        # We don't need to merge on the hash, so drop it from the run_data
        if "datapoint_hash" in run_data.columns:
            run_data.drop("datapoint_hash", inplace=True, axis=1)
        if "rowID" in columns:
            columns.remove("rowID")
        # get the datapoint hashes from the pod db
        data_w_hash = pd.merge(
            pod_data,
            run_data,
            how="outer",
            left_on=columns,
            right_on=columns,
            indicator=True,
        ).loc[lambda x: x["_merge"] == "both"]
        # drop the merge indicator column
        data_w_hash.drop("_merge", inplace=True, axis=1)
    if "rowID" in data_w_hash.columns:
        data_w_hash.drop("rowID", inplace=True, axis=1)
    data_w_hash.drop_duplicates(inplace=True, keep="last")
    # Ignoring the security warning because the sql query is trusted and
    # the task_hash is calculated at __init__.
    task_data = pd.read_sql(
        f'SELECT "datapoint_hash" FROM "{task_hash}"',  # nosec hardcoded_sql_expressions # noqa: B950
        project_db_con,
    )
    # If this is the first time the task is run, it will not
    # have all the columns, so we need to make sure they are
    # added. Otherwise, we don't need to worry about the columns
    # as any alterations to them will be classified as a new task
    project_db_cur = project_db_con.cursor()

    if len(task_data) == 0 and show_datapoints_in_results_db:
        for col in columns:
            project_db_cur.execute(
                f"ALTER TABLE '{task_hash}' ADD COLUMN '{col}' {_sql_type_name(data_w_hash[col])}"  # noqa: B950
            )
    if run_on_new_data_only:
        # do merge and get new datapoints only
        data_w_hash = pd.merge(
            data_w_hash,
            task_data,
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        data_w_hash = data_w_hash.drop(columns=["rowID", "_merge"], errors="ignore")
        logger.info(
            f"The task was run on {len(data_w_hash)} "
            f"records from the datasource."  # nosec hardcoded_sql_expressions
        )

    # remove existing data from the results
    existing_data_hashes = list(
        pd.read_sql(
            f"SELECT * FROM '{task_hash}' ",  # nosec hardcoded_sql_expressions
            project_db_con,
        )["datapoint_hash"]
    )
    data_w_hash = data_w_hash[
        ~data_w_hash["datapoint_hash"].isin(existing_data_hashes)
    ].reset_index(drop=True)
    # save results to db
    if show_datapoints_in_results_db:
        data_w_hash.to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )
    else:
        data_w_hash[["datapoint_hash", "results"]].to_sql(
            f"{task_hash}", con=project_db_con, if_exists="append", index=False
        )
    logger.info("Results saved to database")
