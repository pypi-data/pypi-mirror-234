"""This package contains the core Bitfount codebase.

With the exception of `backends` which contains optional extra packages, every
subpackage or standalone module in this package must have an `__init__.py` file that
defines `__all__`.
"""
#   ____  _ _    __                   _
#  | __ )(_) |_ / _| ___  _   _ _ __ | |_
#  |  _ \| | __| |_ / _ \| | | | '_ \| __|
#  | |_) | | |_|  _| (_) | |_| | | | | |_
#  |____/|_|\__|_|  \___/ \__,_|_| |_|\__|
# We want logs from anything that might be imported so this has to happen at the
# top of the file
from bitfount.utils.logging_utils import _configure_logging

_configure_logging()

# If proxy support is required then it needs to happen BEFORE imports to requests,
# etc., go through so need to do it near the start
from bitfount import config  # noqa: E402

if config.BITFOUNT_PROXY_SUPPORT:
    from bitfount.utils import ssl_utils

    ssl_utils.inject_ssl_proxy_support()

import importlib as _importlib  # noqa: E402
import logging as _logging  # noqa: E402
import pkgutil as _pkgutil  # noqa: E402
import sys as _sys  # noqa: E402
from types import TracebackType as _TracebackType  # noqa: E402
from typing import (  # noqa: E402
    Any as _Any,
    List as _List,
    Optional as _Optional,
    Tuple as _Tuple,
    Type as _Type,
    cast as _cast,
)

from bitfount import (  # noqa: E402
    data,
    exceptions,
    federated,
    hooks,
    hub,
    metrics,
    models,
    runners,
    storage,
    transformations,
    types,
    utils,
)
from bitfount.__version__ import __version__  # noqa: E402, F401
from bitfount.__version__ import __yaml_versions__  # noqa: E402, F401
from bitfount.config import *  # noqa: E402, F403
from bitfount.data import *  # noqa: E402, F403
from bitfount.exceptions import *  # noqa: E402, F403
from bitfount.federated import *  # noqa: E402, F403
from bitfount.hooks import *  # noqa: E402, F403
from bitfount.hub import *  # noqa: E402, F403
from bitfount.metrics import *  # noqa: E402, F403
from bitfount.models import *  # noqa: E402, F403
from bitfount.runners import *  # noqa: E402, F403
from bitfount.storage import *  # noqa: E402, F403
from bitfount.transformations import *  # noqa: E402, F403
from bitfount.types import *  # noqa: E402, F403
from bitfount.utils import *  # noqa: E402, F403

__all__: _List[str] = []

_logger = _logging.getLogger(__name__)

# Attempt to import backends if any exist
try:
    import bitfount.backends

    _backends_imported = True
except ModuleNotFoundError:
    _backends_imported = False

# If backends has been successfully imported, attempt to import each individual backend
# and add its __all__ to __all__
if _backends_imported:
    # Find all top-level subpackages in the backends package
    for _module_info in _pkgutil.iter_modules(
        bitfount.backends.__path__, f"{bitfount.backends.__name__}."
    ):
        _module = None
        # Attempt to import backend subpackage
        try:
            _module = _importlib.import_module(_module_info.name)
        except ImportError:
            pass

        # Add backend subpackage's __all__ to __all__
        if _module is not None:
            _imports: _List[str] = []
            try:
                _imports = _module.__dict__["__all__"]
                __all__.extend(_imports)
            except KeyError:
                _logger.error(f"Couldn't import {_module}: __all__ not defined.")

            # Add backend imports defined in __all__ to globals dictionary
            globals().update({k: getattr(_module, k) for k in _imports})


__all__.extend(config.__all__)
__all__.extend(data.__all__)
__all__.extend(exceptions.__all__)
__all__.extend(federated.__all__)
__all__.extend(hooks.__all__)
__all__.extend(hub.__all__)
__all__.extend(metrics.__all__)
__all__.extend(models.__all__)
__all__.extend(runners.__all__)
__all__.extend(storage.__all__)
__all__.extend(transformations.__all__)
__all__.extend(types.__all__)
__all__.extend(utils.__all__)

# Currently, due to pdoc's reliance on `__all__`, we must iterate over `__all__`` to
# ignore every import in the documentation otherwise they become duplicated
# https://github.com/pdoc3/pdoc/issues/340
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False

# Set stacktrace dependent on config
if config._BITFOUNT_LIMIT_LOGS:
    _sys.tracebacklimit = config._BITFOUNT_TB_LIMIT

    # Jupyter/iPython has its own traceback system, so we need to handle that
    # differently
    try:
        # This function will be in scope if we're in jupyter/iPython
        ipython = get_ipython()  # type: ignore[name-defined] # Reason: see comment # noqa: B950, F405

        orig_showtraceback = ipython.showtraceback

        def _limited_showtraceback(
            exc_tuple: _Optional[
                _Tuple[_Type[BaseException], BaseException, _TracebackType]
            ] = None,
            filename: _Any = None,
            tb_offset: _Any = None,
            exception_only: bool = False,
            running_compiled_code: bool = False,
        ) -> _Any:
            """Override ipython.showtraceback so the traceback stack is limited."""
            try:
                try:
                    tb_limit = _sys.tracebacklimit
                except AttributeError:
                    # If tracebacklimit not set, use original implementation
                    return orig_showtraceback(
                        exc_tuple,
                        filename,
                        tb_offset,
                        exception_only,
                        running_compiled_code,
                    )

                # Otherwise, limit the traceback(s)
                if exc_tuple is None:
                    exc_tuple = _cast(
                        _Tuple[_Type[BaseException], BaseException, _TracebackType],
                        _sys.exc_info(),
                    )
                exc_type, exc_value, tb = exc_tuple

                # Use limit to get Nth entry from back in the traceback
                tb_stack = []
                tb_curr: _Optional[_TracebackType] = tb
                while tb_curr:
                    tb_stack.append(tb_curr)
                    tb_curr = tb_curr.tb_next
                if tb_limit < len(tb_stack):
                    # +1 as IPython interprets the exception itself as the "last frame"
                    # in the stack trace, and we want to at least see where it's raised.
                    nth_tb = tb_stack[-(tb_limit + 1)]
                else:
                    nth_tb = tb

                if nth_tb is not tb:
                    frames_str = "frames" if tb_limit > 1 else "frame"
                    _logger.warning(
                        f"Exception traceback limited to {tb_limit} {frames_str};"
                        f" see debug logs for more details"
                        f" or set BITFOUNT_TB_LIMIT environment variable to a higher"
                        f" number of frames."
                    )

                # Use this in the original implementation
                return orig_showtraceback(
                    (exc_type, exc_value, nth_tb),
                    filename,
                    tb_offset,
                    exception_only,
                    running_compiled_code,
                )
            except Exception:
                print(
                    "Error whilst printing traceback, falling back to default printer",
                    file=_sys.stderr,
                )
                return orig_showtraceback(
                    exc_tuple,
                    filename,
                    tb_offset,
                    exception_only,
                    running_compiled_code,
                )

        ipython.showtraceback = _limited_showtraceback
    except NameError:
        # We are not in a Jupyter/iPython environment
        pass
