"""Support for different "views" over existing datasets.

These allow constraining the usable data that is exposed to a modeller, or only
presenting a transformed view to the modeller rather than the raw underlying data.
"""
from abc import ABC, abstractmethod
import sqlite3
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
    cast,
)

import methodtools
import numpy as np
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.exceptions import SQLViewError
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import _ForceStypeValue, _SemanticTypeValue, _SingleOrMulti
from bitfount.types import _Dtypes
from bitfount.utils import _add_this_to_list


class DataView(BaseSource, ABC):
    """Base class for datasource views.

    Args:
        datasource: The `BaseSource` the view is generated from.
    """

    def __init__(
        self,
        datasource: BaseSource,
        data_splitter: Optional[DatasetSplitter] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._datasource = datasource
        self.data_splitter = (
            data_splitter
            if data_splitter is not None
            else self._datasource.data_splitter
        )
        self.file_names: Optional[
            List[str]
        ] = None  # Placeholder for views of FileIterableSource.
        # This needs to be overwritten by the view's way of getting the files.

    @property
    def iterable(self) -> bool:
        """This returns False if the DataSource does not subclass `IterableSource`.

        However, this property must be re-implemented in `IterableSource`, therefore it
        is not necessarily True if the DataSource inherits from `IterableSource`.
        """
        return self._datasource.iterable

    def yield_data(
        self, file_names: Optional[List[str]] = None, **kwargs: Any
    ) -> Iterator[pd.DataFrame]:
        """Yields data in batches from files that match the given file names.

        Args:
            file_names: An optional list of file names to use for yielding data.
                Otherwise, all files that have already been found will be used.
                `file_names` is always provided when this method is called from the
                Dataset as part of a task.

        Raises:
            ValueError: If no file names provided and no files have been found.
            ValueError: If underlying datasource is not FileSystemIterableSource.
        """
        # This is used by FileSystemIterableSource only,
        # so we raise an error if that's not the case and
        # then we can cast the underlying datasource
        if not isinstance(self._datasource, FileSystemIterableSource):
            raise ValueError(
                "Underlying datasource for views is not a `FileSystemIterableSource`, "
                "which is the only compatible datasource for this function."
            )
        if file_names is None and self.file_names is None:
            raise ValueError("No files found to yield data from.")
        file_names = file_names or self.file_names
        # at this point file_names should be set, so it's safe to cast
        file_names = cast(List[str], file_names)
        for file_names_partition in self._datasource.partition(
            file_names, self._datasource.partition_size
        ):
            file_names_partition = cast(List[str], file_names_partition)
            yield self._datasource._get_data(file_names_partition)
            # Delete the files after they have been processed and used
            self._datasource._cleanup(file_names_partition)


class DropColsDataview(DataView):
    """A data view that presents data with columns removed."""

    _datasource: BaseSource

    def __init__(self, datasource: BaseSource, drop_cols: _SingleOrMulti[str]) -> None:
        super().__init__(datasource)
        self._drop_cols: List[str] = (
            [drop_cols] if isinstance(drop_cols, str) else list(drop_cols)
        )
        if isinstance(self._datasource, FileSystemIterableSource):
            self.file_names = self._datasource.file_names

    # TODO: [BIT-1780] Simplify referencing data in here and in other sources
    #       We want to avoid recalculating but we don't want to cache more
    #       than one result at a time to save memory
    @methodtools.lru_cache(maxsize=1)
    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from underlying dataset.

        Will handle drop columns specified in view.

        Returns:
            A DataFrame-type object which contains the data.

        Raises:
            ValueError: if no data is returned from the original datasource.
        """
        df: Optional[pd.DataFrame] = self._datasource.get_data(**kwargs)
        # Ensure we return a copy of the dataframe rather than mutating the original
        if isinstance(df, pd.DataFrame):
            drop_df = df.drop(columns=self._drop_cols)
            return drop_df
        else:
            raise ValueError("No data returned from the underlying datasource.")

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.get_data(**kwargs)[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        df: pd.DataFrame = self.get_data(**kwargs)
        return df[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the dataset.

        Returns:
            A mapping from column names to column types.
        """
        df: pd.DataFrame = self.get_data(**kwargs)
        return self._get_data_dtypes(df)

    def __len__(self) -> int:
        return len(self.get_data())


class SQLDataView(DataView):
    """A data view that presents data with SQL query applied."""

    _datasource: BaseSource

    def __init__(
        self,
        datasource: BaseSource,
        query: str,
        pod_name: str,
        source_dataset_name: str,
    ) -> None:
        super().__init__(datasource)
        self.query = query
        self.pod_db_name = pod_name
        self.source_dataset_name = source_dataset_name
        self.file_names = (
            self._get_filenames()
            if isinstance(self._datasource, FileSystemIterableSource)
            else None
        )
        self.selected_file_names = self.file_names

    def _get_filenames(self) -> List[str]:
        """Get filenames for views generated from FileSystemIterableSource."""
        db_conn = sqlite3.connect(f"{self.pod_db_name}.sqlite")
        tables = self.get_tables()
        if not any(table in self.query for table in tables):
            raise ValueError("The table specified in the query does not exist.")
        # We get the updated query that also includes the `_original_filename`
        # column, so we can obtain the list of filenames from the view.
        query_with_original_filename = self._get_updated_query_with_metadata()
        try:
            df = pd.read_sql_query(query_with_original_filename, db_conn)
            return df["_original_filename"].to_list()
        except Exception:
            raise SQLViewError(
                "Could not obtain the filenames for the datasource. "
                "Make sure that your file-iterable datasource is properly defined."
            )

    def _get_updated_query_with_metadata(self) -> str:
        """Get updated query with metadata columns included.

        For non-iterable datasources this adds the `datapoint_hash`
        column to be returned by the query. For FileSystemIterableSource
        it also includes the `_original_filename` and `_last_modified` columns.
        """
        metadata_cols_as_str = '"datapoint_hash",'
        if isinstance(self._datasource, FileSystemIterableSource):
            metadata_cols_as_str += '"_original_filename", "_last_modified",'
        return self.query.replace("SELECT", f"SELECT {metadata_cols_as_str}")

    @methodtools.lru_cache(maxsize=1)
    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from underlying dataset.

        Will handle sql query specified in view.

        Returns:
            A DataFrame-type object which contains the data.

        Raises:
            ValueError: if the table specified in the query is not found.
        """
        # Get tables and check that table requested in
        # the query matches at least one of the tables in the database.
        db_conn = sqlite3.connect(f"{self.pod_db_name}.sqlite")
        tables = self.get_tables()
        if not any(table in self.query for table in tables):
            raise ValueError("The table specified in the query does not exist.")
        df = pd.read_sql_query(self.query, db_conn)
        db_conn.close()
        return df

    def get_tables(self) -> List[str]:
        """Get the datasource tables from the pod database."""
        db_conn = sqlite3.connect(f"{self.pod_db_name}.sqlite")
        cur = db_conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        db_conn.close()
        # tables are returned as a list of tuples where the first tuple
        # is the table name, so we need to unpack them
        return [table[0] for table in tables]

    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in the dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.get_data(**kwargs)[col].unique() for col in col_names}

    def get_column(
        self, col_name: str, table_name: Optional[str] = None, **kwargs: Any
    ) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """

        df: pd.DataFrame = self.get_data(**kwargs)
        return df[col_name]

    def get_dtypes(self, table_name: Optional[str] = None, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the dataset.

        Returns:
            A mapping from column names to column types.
        """
        df: pd.DataFrame = self.get_data(**kwargs)
        return self._get_data_dtypes(df)

    def __len__(self) -> int:
        return len(self.get_data())


_DS = TypeVar("_DS", bound=BaseSource)


class ViewDatasourceConfig(ABC, Generic[_DS]):
    """A class dictating the configuration of a view.

    Args:
        source_dataset: The name of the underlying datasource.
    """

    def __init__(self, source_dataset: str, *args: Any, **kwargs: Any) -> None:
        self.source_dataset_name = source_dataset

    @abstractmethod
    def generate_schema(self, *args: Any, **kwargs: Any) -> BitfountSchema:
        """Schema generation for views."""

    @abstractmethod
    def build(self, underlying_datasource: _DS) -> DataView:
        """Build a view instance corresponding to this config."""


class DropColViewConfig(ViewDatasourceConfig[BaseSource]):
    """Config class for DropColsDropColView.

    Args:
        drop_cols: The columns to drop.
    """

    def __init__(
        self, drop_cols: _SingleOrMulti[str], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._drop_cols: List[str] = (
            [drop_cols] if isinstance(drop_cols, str) else list(drop_cols)
        )

    def generate_schema(
        self,
        underlying_datasource: BaseSource,
        name: str,
        force_stypes: Optional[
            MutableMapping[Union[_ForceStypeValue, _SemanticTypeValue], List[str]]
        ] = None,
        schema: Optional[BitfountSchema] = None,
    ) -> BitfountSchema:
        """Schema generation for DropColViewConfig.

        Args:
            underlying_datasource: The underlying datasource for the view.
            name: The name of the DropColViewConfig.
            force_stypes: A mapping of table names to a mapping of semantic types to
                a list of column names.
            schema: A BitfountSchema object. If provided, the schema will not be
                re-generated.

        Returns:
            A BitfountSchema object.
        """
        # Actually generate the schema
        if not schema:
            view = self.build(underlying_datasource)
            view_columns = view.get_data().columns.to_list()
            if force_stypes:
                view_force_stypes = {}
                # adapt force stypes from underlying datasource to fit the drop view
                for k, v in force_stypes.items():
                    # We need special handling for `image_prefix`. This is because
                    # `image_prefix` is not part of the schema features, but just an
                    # easier way for a user to specify (especially in the YAML format).
                    # the image columns of a datasource.
                    if k not in ["image_prefix", "image"]:
                        # Extract only the columns present in the datasource.
                        view_force_stypes[k] = [col for col in v if col in view_columns]
                    elif k == "image_prefix":
                        # If `image_prefix` is in `force_stypes`, we need to add the
                        # columns that start with that prefix to the image features
                        # in the schema.
                        img_cols = [
                            col
                            for col in view_columns
                            if any(
                                col.startswith(stype)
                                for stype in force_stypes["image_prefix"]
                            )
                        ]
                        if len(img_cols) > 0:
                            # The image features might have processed so we don't
                            # want to overwrite them if that is the case
                            if "image" in view_force_stypes:
                                view_force_stypes["image"] = _add_this_to_list(
                                    img_cols, view_force_stypes["image"]
                                )
                            else:
                                view_force_stypes["image"] = img_cols
                    else:  # if k == "image"
                        # Similarly, image features might have been
                        # already added so we don't want to overwrite them
                        if "image" in view_force_stypes:
                            img_cols = [col for col in v if col in view_columns]
                            view_force_stypes["image"] = _add_this_to_list(
                                img_cols, view_force_stypes["image"]
                            )
                        else:
                            view_force_stypes["image"] = [
                                col for col in v if col in view_columns
                            ]
                view_force_stype = {name: view_force_stypes}
            else:
                view_force_stype = None

            schema = BitfountSchema()
            schema.add_datasource_tables(
                datasource=view,
                table_name=name,
                force_stypes=cast(
                    Optional[
                        Mapping[
                            str,
                            MutableMapping[
                                Union[_SemanticTypeValue, _ForceStypeValue], List[str]
                            ],
                        ]
                    ],
                    view_force_stype,
                ),
            )
        return schema

    def build(self, underlying_datasource: BaseSource) -> DropColsDataview:
        """Build a DropColsCSVDropColView from this configuration.

        Args:
            underlying_datasource: The underlying datasource for the view.
        """
        return DropColsDataview(underlying_datasource, self._drop_cols)


class SQLViewConfig(ViewDatasourceConfig[BaseSource]):
    """Config class for SQLDataViewConfig.

    Args:
        query: The SQL query for the view.

    Raises:
        ValueError: if the query does not start with SELECT.
    """

    def __init__(self, query: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Raise error at the beginning if query does not start with `SELECT`.
        # TODO: [NO_TICKET: Reason] Add better checking of the query after the query parser is built on the platform side. # noqa: B950
        if not query.lstrip().startswith("SELECT"):
            raise ValueError(
                "Unsupported query. We currently support only "
                "`SELECT ... FROM ...` queries for defining "
                "dataset views."
            )
        self.query = query

    def initialize(self, pod_name: str) -> None:
        """Initialize the view by providing the pod name for the database."""
        self.pod_name = pod_name

    def generate_schema(
        self,
        underlying_datasource: BaseSource,
        name: str,
        force_stypes: Optional[
            MutableMapping[Union[_ForceStypeValue, _SemanticTypeValue], List[str]]
        ] = None,
        schema: Optional[BitfountSchema] = None,
    ) -> BitfountSchema:
        """Schema generation for SQLDataViewConfig.

        Args:
            underlying_datasource: The underlying datasource for the view.
            name: The name of the DropColViewConfig.
            force_stypes: A mapping of table names to a mapping of semantic types to
                a list of column names.
            schema: A BitfountSchema object. If provided, the schema will not be
                re-generated.

        Returns:
            A BitfountSchema object.
        """
        if not schema:
            view = self.build(underlying_datasource)
            view_columns = view.get_data().columns.to_list()
            if force_stypes:
                view_force_stypes = {}
                # adapt force stypes from underlying datasource to fit the drop view
                for k, v in force_stypes.items():
                    # We need special handling for `image_prefix`. This is because
                    # `image_prefix` is not part of the schema features, but just an
                    # easier way for a user to specify (especially in the YAML format).
                    # the image columns of a datasource.
                    if k not in ["image_prefix", "image"]:
                        # Extract only the columns present in the datasource.
                        view_force_stypes[k] = [col for col in v if col in view_columns]
                    elif k == "image_prefix":
                        # If `image_prefix` is in `force_stypes`, we need to add the
                        # columns that start with that prefix to the image features
                        # in the schema.
                        img_cols = [
                            col
                            for col in view_columns
                            if any(
                                col.startswith(stype)
                                for stype in force_stypes["image_prefix"]
                            )
                        ]
                        if len(img_cols) > 0:
                            # The image features might have processed so we don't
                            # want to overwrite them if that is the case
                            if "image" in view_force_stypes:
                                view_force_stypes["image"] = _add_this_to_list(
                                    img_cols, view_force_stypes["image"]
                                )
                            else:
                                view_force_stypes["image"] = img_cols
                    else:  # if k == "image"
                        # Similarly, image features might have been
                        # already added so we don't want to overwrite them
                        if "image" in view_force_stypes:
                            img_cols = [col for col in v if col in view_columns]
                            view_force_stypes["image"] = _add_this_to_list(
                                img_cols, view_force_stypes["image"]
                            )
                        else:
                            view_force_stypes["image"] = [
                                col for col in v if col in view_columns
                            ]
                view_force_stype = {name: view_force_stypes}
            else:
                view_force_stype = None
            # Actually generate schema
            schema = BitfountSchema()
            schema.add_datasource_tables(
                datasource=view,
                table_name=name,
                force_stypes=cast(
                    Optional[
                        Mapping[
                            str,
                            MutableMapping[
                                Union[_SemanticTypeValue, _ForceStypeValue], List[str]
                            ],
                        ]
                    ],
                    view_force_stype,
                ),
            )
        return schema

    def build(self, underlying_datasource: BaseSource) -> SQLDataView:
        """Build a SQLDataViewConfig from this configuration.

        Args:
            underlying_datasource: The underlying datasource for the view.
        """
        return SQLDataView(
            underlying_datasource,
            query=self.query,
            pod_name=self.pod_name,
            source_dataset_name=self.source_dataset_name,
        )
