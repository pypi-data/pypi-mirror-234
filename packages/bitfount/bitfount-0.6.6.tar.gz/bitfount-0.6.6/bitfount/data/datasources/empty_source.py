"""Contains an implementation of an empty datasource, one with no data."""
from typing import Any, List

from typing_extensions import NoReturn

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.exceptions import DataSourceError
from bitfount.types import _Dtypes


class _EmptySource(BaseSource):
    """A datasource with no data.

    This can be used in cases where data is retrieved/analysed at runtime such as
    from third-party data repositories which need runtime authentication.
    """

    def get_values(self, col_names: List[str], **kwargs: Any) -> NoReturn:
        """Raises DataSourceError as there are no columns to return."""
        raise DataSourceError(f"{self.__class__.__name__} contains no columns.")

    def get_column(self, col_name: str, **kwargs: Any) -> NoReturn:
        """Raises DataSourceError as there are no columns to return."""
        raise DataSourceError(f"{self.__class__.__name__} contains no columns.")

    def get_data(self, **kwargs: Any) -> None:
        """Returns None as there is no data."""
        return None

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Returns an empty dict as there is no data."""
        return {}

    def __len__(self) -> int:
        """Returns zero as there is no data."""
        return 0
