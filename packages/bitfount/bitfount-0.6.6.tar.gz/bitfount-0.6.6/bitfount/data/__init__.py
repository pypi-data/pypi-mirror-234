"""Modules for handling model data flow.

Data plugins can also be imported from this package.
"""
import importlib as _importlib
import inspect as _inspect
import logging as _logging
import pkgutil as _pkgutil
from types import ModuleType
from typing import List as _List

from bitfount.config import BITFOUNT_PLUGIN_PATH as _BITFOUNT_PLUGIN_PATH
from bitfount.data import datasources as datasources
from bitfount.data.dataloaders import BitfountDataLoader
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.views import (
    DropColViewConfig,
    SQLViewConfig,
    ViewDatasourceConfig,
)
from bitfount.data.datasplitters import PercentageSplitter, SplitterDefinedInData
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import (
    BitfountSchemaError,
    DatabaseMissingTableError,
    DatabaseSchemaNotFoundError,
    DatabaseUnsupportedQueryError,
    DataNotLoadedError,
    DatasetSplitterError,
    DataStructureError,
    DuplicateColumnError,
)
from bitfount.data.helper import convert_epochs_to_steps
from bitfount.data.schema import BitfountSchema, TableSchema
from bitfount.data.types import (
    CategoricalRecord,
    ContinuousRecord,
    DataPathModifiers,
    DataSplit,
    ImageRecord,
    SemanticType,
    TextRecord,
)
from bitfount.data.utils import (
    DatabaseConnection,
    check_datastructure_schema_compatibility,
)
from bitfount.utils import _import_module_from_file

_logger = _logging.getLogger(__name__)
__all__: _List[str] = [
    "BitfountDataLoader",
    "BitfountSchema",
    "BitfountSchemaError",
    "CategoricalRecord",
    "ContinuousRecord",
    "DatabaseConnection",
    "DatabaseMissingTableError",
    "DatabaseSchemaNotFoundError",
    "DatabaseUnsupportedQueryError",
    "DatasetSplitterError",
    "DataNotLoadedError",
    "DataPathModifiers",
    "DataSplit",
    "DataStructure",
    "DataStructureError",
    "DropColViewConfig",
    "DuplicateColumnError",
    "ImageRecord",
    "PercentageSplitter",
    "SemanticType",
    "SplitterDefinedInData",
    "SQLViewConfig",
    "TableSchema",
    "TextRecord",
    "ViewDatasourceConfig",
    "check_datastructure_schema_compatibility",
    "convert_epochs_to_steps",
]


def _load_datasource_classes(
    classes: list, module: ModuleType, module_info: _pkgutil.ModuleInfo
) -> None:
    found_datasource = False

    for cls in classes:
        if issubclass(cls, BaseSource) and not _inspect.isabstract(cls):
            found_datasource = True
            globals().update({cls.__name__: getattr(module, cls.__name__)})
            __all__.append(cls.__name__)
        # There are too many false positives if we don't restrict classes to those
        # that inherit from BaseSource for it to be a useful log message
        elif issubclass(cls, BaseSource) and cls.__name__ not in (
            "BaseSource",
            "MultiTableSource",
            "IterableSource",
            "FileSystemIterableSource",
            "DataView",
        ):
            found_datasource = True
            _logger.warning(
                f"Found class {cls.__name__} in module {module_info.name} which "
                f"did not fully implement BaseSource. Skipping."
            )
        elif module_info.name in ("base_source", "utils"):
            # We don't want to log this because it's expected
            found_datasource = True

    if not found_datasource:
        _logger.warning(f"{module_info.name} did not contain a subclass of BaseSource.")


def _load_view_config_classes(
    classes: list, module: ModuleType, module_info: _pkgutil.ModuleInfo
) -> None:
    for cls in classes:
        if issubclass(cls, ViewDatasourceConfig) and not _inspect.isabstract(cls):
            globals().update({cls.__name__: getattr(module, cls.__name__)})
            __all__.append(cls.__name__)


# Import all concrete implementations of BaseSource in the datasources subdirectory
# as well as datasource plugins.
# Import all data view configuration classes.
for _module_info in _pkgutil.walk_packages(
    path=datasources.__path__ + [str(_BITFOUNT_PLUGIN_PATH / "datasources")],
):
    try:
        _module = _importlib.import_module(
            f"{datasources.__name__}.{_module_info.name}"
        )
    # Also catches `ModuleNotFoundError` which subclasses `ImportError`
    # Try to import the module from the plugin directory if it's not found in the
    # datasources directory
    except ImportError:
        # These modules have extra requirements that are not installed by default
        if _module_info.name in ("dicom_source"):
            _logger.debug(
                f"Error importing module {_module_info.name}. Please make "
                "sure that all required packages are installed if "
                "you are planning to use that specific module"
            )
            continue
        else:
            try:
                _module, _ = _import_module_from_file(
                    _BITFOUNT_PLUGIN_PATH / "datasources" / f"{_module_info.name}.py",
                    parent_module=datasources.__package__,
                )
                _logger.info(
                    f"Imported datasource plugin {_module_info.name}"
                    f" as {_module.__name__}"
                )
            except ImportError as ex:
                _logger.error(
                    f"Error importing datasource plugin {_module_info.name}"
                    f" under {__name__}: {str(ex)}"
                )
                _logger.debug(ex, exc_info=True)
                continue

    # Extract classes in loaded module
    _classes = [cls for _, cls in _inspect.getmembers(_module, _inspect.isclass)]

    # Check for datasource classes
    _load_datasource_classes(_classes, _module, _module_info)

    # Check for data view config classes
    _load_view_config_classes(_classes, _module, _module_info)

# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
