"""Algorithm for outputting results to CSV on the pod-side."""
from __future__ import annotations

from dataclasses import dataclass
import operator
import os
from pathlib import Path
import typing
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
    cast,
)

import desert
from marshmallow import fields
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union
import pandas as pd

import bitfount.config
from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.exceptions import DataSourceError
from bitfount.data.types import DataSplit
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig

if TYPE_CHECKING:
    from bitfount.types import T_FIELDS_DICT

logger = _get_federated_logger(__name__)

FILTER_MATCHING_COLUMN = "Matches all criteria"


_FilterOperatorTypes = Literal[
    "equal",
    "==",
    "equals",
    "not equal",
    "!=",
    "less than",
    "<",
    "less than or equal",
    "<=",
    "greater than",
    ">",
    "greater than or equal",
    ">=",
]

_OperatorMapping = {
    "less than": operator.lt,
    "<": operator.lt,
    "less than or equal": operator.le,
    "<=": operator.le,
    "greater than": operator.gt,
    ">": operator.gt,
    "greater than or equal": operator.ge,
    ">=": operator.ge,
    "equal": operator.eq,
    "==": operator.eq,
    "equals": operator.eq,
    "not equal": operator.ne,
    "!=": operator.ne,
}


@dataclass
class ColumnFilter:
    """Dataclass for column filtering.

    Args:
        column: The column name on which the filter will be applied.
            The filtering ignores capitalization or spaces for the
            column name.
        operator: The operator for the filtering operation. E.g.,
            "less than", ">=", "not equal", "==".
        value: The value for the filter. This is allowed to be a
            string only for `equals` or `not equal` operators,
            and needs to be a float or integer for all other operations.

    Raises:
        ValueError: If an inequality comparison operation is given
        with a value which cannot be converted to a float.
    """

    column: str = desert.field(fields.String())
    operator: str = desert.field(
        fields.String(validate=OneOf(typing.get_args(_FilterOperatorTypes)))
    )
    value: typing.Union[str, int, float] = desert.field(
        M_Union([fields.String(), fields.Integer(), fields.Float()])
    )

    def __post_init__(self) -> None:
        # check that the operator is valid:
        try:
            op = _OperatorMapping[self.operator]
            if op != operator.eq and op != operator.ne:
                try:
                    float(self.value)
                except ValueError as e:
                    raise ValueError(
                        f"Filter value `{self.value}` incompatible with "
                        f"operator type `{self.operator}`. "
                        f"Raised ValueError: {str(e)}"
                    )
        except KeyError:
            raise KeyError(
                f"Given operator `{self.operator}` is not valid."
                "Make sure your operator is one of the following : "
                f"{typing.get_args(_FilterOperatorTypes)}"
            )


def _add_filtering_to_df(df: pd.DataFrame, filter: ColumnFilter) -> pd.DataFrame:
    """Applies the filter to the given dataframe.

    An extra column will be added to the dataframe indicating which
    rows match a given filter.

    Args:
        df: The dataframe on which the filter is applied.
        filter: A ColumnFilter instance.

    Returns:
        A dataframe with additional column added which
        indicates whether a datapoint matches the given
        condition in the ColumnFilter.
    """
    columns = [
        col
        for col in df.columns
        if filter.column.lower().replace(" ", "") == col.lower().replace(" ", "")
    ]
    if len(columns) == 0:
        raise KeyError(f"No column {filter.column} found in the data.")
    else:
        # dataframe cannot have duplicate columns, so
        # it's safe to assume it will only be one column
        matching_col = columns[0]
        value: typing.Union[str, float] = filter.value
    op = _OperatorMapping[filter.operator]
    if op != operator.eq and op != operator.ne:
        value = float(value)
    df[f"{matching_col} {filter.operator} {filter.value}"] = op(df[matching_col], value)
    df[FILTER_MATCHING_COLUMN] = (
        df[f"{matching_col} {filter.operator} {filter.value}"]
        & df[FILTER_MATCHING_COLUMN]
    )
    return df


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, None]) -> None:
        """Modeller side just logs that the csv has been saved."""
        logger.info("CSV saved to the pod.")


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm."""

    def __init__(
        self,
        path: Union[os.PathLike, str],
        original_cols: Optional[List[str]] = None,
        filter: Optional[List[ColumnFilter]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.path = Path(path)
        self.original_cols = original_cols
        self.filter = filter

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.initialise_data(datasource=datasource)

    def run(
        self,
        results_df: Union[pd.DataFrame, List[pd.DataFrame]],
        task_id: Optional[str] = None,
    ) -> pd.DataFrame:
        """Saves the results of an inference task on the pod.

        The results are saved in a CSV file, at the user specified path.

        Args:
            results_df: The results of the previous inference task.
            task_id: The ID of the task.

        Returns:
            The dataframe of results and data that is also saved to a CSV file.
        """
        # This is a temporary fix to allow for the case where the results
        # dataframe from the previous algorithm has been run on the entire dataset
        # rather than just the test set. Specifically this was done to accomodate
        # the transformer text generation and perplexity algorithms.
        if isinstance(results_df, pd.DataFrame) and len(results_df) == len(
            self.datasource
        ):
            df = self.datasource.data.join(results_df)
        else:
            # If there are no test rows, this is only okay if the datasource is iterable
            # Otherwise, we raise an error.
            if self.datasource._test_idxs is None:
                if not self.datasource.iterable:
                    raise DataSourceError(
                        "Datasource has no test set, cannot produce CSV."
                    )
                else:
                    # If the datasource is iterable, we need to use the `get_filenames`
                    # method of the data splitter to get the filenames corresponding to
                    # the test set, which are then used to filter the dataframe
                    data_splitter = (
                        self.datasource.data_splitter
                        if self.datasource.data_splitter
                        else PercentageSplitter()
                    )
                    data = cast(FileSystemIterableSource, self.datasource)
                    filenames = data_splitter.get_filenames(data, DataSplit.TEST)
                    df = data.data.loc[
                        data.data["_original_filename"].isin(filenames)
                    ].reset_index(drop=True)
            else:
                # Resetting the index here is important when
                # joining because the dataframes are matched
                # by index. Resetting the index means that
                # `.copy()` is not needed to avoid a
                # SettingWithCopyWarning.
                df = self.datasource.data.loc[self.datasource._test_idxs].reset_index(
                    drop=True
                )

            if isinstance(results_df, list):
                aux_results_df = results_df[0]
                for index in range(1, len(results_df)):
                    aux_results_df = pd.concat(
                        [aux_results_df, results_df[index]], axis=1
                    )
            else:
                aux_results_df = results_df

            # Append the results to the original data
            logger.debug("Appending results to the original data.")
            df = df.join(aux_results_df)

        # Filter the data if a filter is provided
        if self.filter is not None:
            logger.debug("Filtering data.")
            df[FILTER_MATCHING_COLUMN] = True
            for i, col_filter in enumerate(self.filter):
                logger.debug(f"Running filter {i + 1}")
                try:
                    df = _add_filtering_to_df(df, col_filter)
                except (KeyError, TypeError) as e:
                    if isinstance(e, KeyError):
                        logger.warning(
                            f"No column `{col_filter.column}` found in the data. Filtering only on remaining given columns"  # noqa: B950
                        )
                    else:
                        # if TypeError
                        logger.warning(
                            f"Filter column {col_filter.column} is incompatible with "  # noqa: B950
                            f"operator type {col_filter.operator}. "
                            f"Raised TypeError: {str(e)}"
                        )
                    logger.info(
                        f"Filtering will skip `{col_filter.column} "
                        f"{col_filter.operator} {col_filter.value}`."
                    )

        # Drop any columns that were not in the original data if specified.
        if self.original_cols is not None:
            drop_cols = [
                col
                for col in self.datasource.data.columns
                if col not in self.original_cols
            ]
            logger.debug(f"Dropping columns {drop_cols}")
            df = df.drop(drop_cols, axis=1)

        # Get the path to the CSV file.
        if task_id is not None:
            Path(self.path / f"{task_id}").mkdir(parents=True, exist_ok=True)
            csv_path = self.path / f"{task_id}" / "results.csv"

        else:
            Path(self.path).mkdir(parents=True, exist_ok=True)
            csv_path = self.path / "results.csv"
            i = 1
            while csv_path.exists():
                csv_path = self.path / f"results ({i}).csv"
                i += 1

        # If the csv file does not exist, we write the header as well as the data.
        # Otherwise, we only write the data and append it to the existing file.
        df.round(decimals=2).to_csv(
            csv_path, mode="a", header=not csv_path.exists(), index=False
        )

        return df


class CSVReportAlgorithm(BaseAlgorithmFactory):
    """Algorithm for generating the CSV results reports.

    Args:
        save_path: The folder path where the csv report should be saved.
            The CSV report will have the same name as the taskID.
        original_cols: The tabular columns from the datasource to include
            in the report. If not specified it will include all
            tabular columns from the datasource.
        filter: A list of `ColumnFilter` instances on which
            we will filter the data on. Defaults to None. If supplied,
            columns will be added to the output csv indicating the
            records that match the specified criteria. If more than one
            `ColumnFilter` is given, and additional column will be added
            to the output csv indicating the datapoints that match all
            given criteria (as well as the individual matches)
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "save_path": fields.Str(),
        "original_cols": fields.List(fields.Str(), allow_none=True),
        "filter": fields.Nested(
            desert.schema_class(ColumnFilter), many=True, allow_none=True
        ),
    }

    def __init__(
        self,
        save_path: Optional[Union[str, os.PathLike]] = None,
        original_cols: Optional[List[str]] = None,
        filter: Optional[List[ColumnFilter]] = None,
        **kwargs: Any,
    ) -> None:
        self.save_path: Path
        if save_path is None:
            self.save_path = bitfount.config.BITFOUNT_OUTPUT_DIR
        else:
            self.save_path = Path(save_path)

        self.original_cols = original_cols
        self.filter = filter
        super().__init__(**kwargs)

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Modeller-side of the algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            path=self.save_path,
            filter=self.filter,
            original_cols=self.original_cols,
            **kwargs,
        )
