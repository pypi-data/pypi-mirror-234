"""Dealing with interactions with configuration and environment variables."""
from importlib import util
from importlib.machinery import ModuleSpec
from functools import lru_cache
import logging
import os
from pathlib import Path
from typing import Callable, Dict, Final, List, Optional, Tuple, cast

import GPUtil
from environs import Env

from bitfount.__version__ import __yaml_versions__ as yaml_versions

__all__: List[str] = [
    # Storage and log locations
    "BITFOUNT_HOME",
    "BITFOUNT_STORAGE_PATH",
    "BITFOUNT_PLUGIN_PATH",
    "BITFOUNT_FEDERATED_PLUGIN_PATH",
    "BITFOUNT_KEY_STORE",
    "BITFOUNT_LOGS_DIR",
    "BITFOUNT_OUTPUT_DIR",
    "BITFOUNT_CACHE_DIR",
    # Compatibility/extras options
    "BITFOUNT_USE_MPS",
    "BITFOUNT_PROXY_SUPPORT",
    "BITFOUNT_DEFAULT_TORCH_DEVICE",
    # Message Service
    "BITFOUNT_ONLINE_CHECK_HARD_LIMIT",
    "BITFOUNT_ONLINE_CHECK_SOFT_LIMIT",
    # Logging/Error Handling
    "_BITFOUNT_LIMIT_LOGS",
    "BITFOUNT_LOG_TO_FILE",
    "_BITFOUNT_TB_LIMIT",
    # Task environment variables
    "BITFOUNT_TASK_BATCH_SIZE",
    "BITFOUNT_DEFAULT_BATCHED_EXECUTION",
    # Backend engine
    "BITFOUNT_ENGINE",
    # GPU
    "get_gpu_metadata",
    # YAML versioning
    "_BITFOUNT_COMPATIBLE_YAML_VERSIONS",
]

from marshmallow import ValidationError

logger = logging.getLogger(__name__)


# Validators
def _validate_torch_device(arg: str) -> None:
    if arg in ("cpu", "mps") or arg.startswith("cuda"):
        return
    else:
        raise ValidationError(
            "Invalid choice for default torch device, should be one of:"
            ' "cpu",'
            ' "mps",'
            ' "cuda",'
            ' or "cuda:<device_id>" (e.g. "cuda:1").'
        )


# This is needed at the top of the module so all the envvars can be linked to it
env = Env()

#######################################
# Public Config/Environment Variables #
#######################################
# Storage and log locations
BITFOUNT_HOME: Path = env.path("BITFOUNT_HOME", default=Path.home()).expanduser()
BITFOUNT_STORAGE_PATH: Path = env.path(
    "BITFOUNT_STORAGE_PATH", default=BITFOUNT_HOME / ".bitfount"
).expanduser()
BITFOUNT_PLUGIN_PATH: Path = env.path(
    "BITFOUNT_PLUGIN_PATH", default=BITFOUNT_STORAGE_PATH / "_plugins"
).expanduser()
BITFOUNT_FEDERATED_PLUGIN_PATH: Path = env.path(
    "BITFOUNT_FEDERATED_PLUGIN_PATH", default=BITFOUNT_PLUGIN_PATH / "federated"
).expanduser()
BITFOUNT_KEY_STORE: Path = env.path(
    "BITFOUNT_KEY_STORE", default=BITFOUNT_STORAGE_PATH / "known_workers.yml"
).expanduser()
BITFOUNT_LOGS_DIR: Path = env.path(
    # NOTE: The default here is a relative path of "bitfount_logs"
    "BITFOUNT_LOGS_DIR",
    default=Path("bitfount_logs"),
).expanduser()
BITFOUNT_OUTPUT_DIR: Path = env.path(
    # NOTE: The default here is current working directory
    "BITFOUNT_OUTPUT_DIR",
    default=Path("."),
).expanduser()
BITFOUNT_CACHE_DIR: Path = env.path(
    "BITFOUNT_CACHE_DIR",
    default=BITFOUNT_STORAGE_PATH / "cache",
).expanduser()
# Compatibility/extras options
BITFOUNT_USE_MPS: bool = env.bool("BITFOUNT_USE_MPS", default=False)
BITFOUNT_PROXY_SUPPORT: bool = env.bool("BITFOUNT_PROXY_SUPPORT", default=False)
BITFOUNT_DEFAULT_TORCH_DEVICE: Optional[str] = env.str(
    "BITFOUNT_DEFAULT_TORCH_DEVICE", default=None, validate=_validate_torch_device
)

# Message Service
BITFOUNT_ONLINE_CHECK_SOFT_LIMIT: int = env.int(
    "BITFOUNT_ONLINE_CHECK_SOFT_LIMIT", default=180, validate=lambda n: n > 0
)
BITFOUNT_ONLINE_CHECK_HARD_LIMIT: int = env.int(
    "BITFOUNT_ONLINE_CHECK_HARD_LIMIT", default=180, validate=lambda n: n > 0
)

# Logging/Error Handling
_BITFOUNT_LIMIT_LOGS: bool = env.bool("BITFOUNT_LIMIT_LOGS", default=False)
BITFOUNT_LOG_TO_FILE: bool = env.bool("BITFOUNT_LOG_TO_FILE", default=True)
_BITFOUNT_TB_LIMIT: int = env.int("BITFOUNT_TB_LIMIT", default=3)
_BITFOUNT_MULTITHREADING_DEBUG: bool = env.bool(
    "BITFOUNT_MULTITHREADING_DEBUG", default=False
)

# Task environment variables
# This is used by the pod to determine how many batches to split a task into
# if the modeller has requested batched execution
BITFOUNT_TASK_BATCH_SIZE: int = env.int(
    "BITFOUNT_TASK_BATCH_SIZE", default=100, validate=lambda n: n > 0
)
# For easier control of the batched execution in the app
BITFOUNT_DEFAULT_BATCHED_EXECUTION: bool = env.bool(
    "BITFOUNT_DEFAULT_BATCHED_EXECUTION", default=False
)
##############################################
# End of Public Config/Environment Variables #
##############################################

########################################
# Private Config/Environment Variables #
########################################
_BITFOUNT_CLI_MODE: bool = False
_PRODUCTION_ENVIRONMENT: Final[str] = "production"
_STAGING_ENVIRONMENT: Final[str] = "staging"
_DEVELOPMENT_ENVIRONMENT: Final[str] = "dev"
_SANDBOX_ENVIRONMENT: Final[str] = "sandbox"
_ENVIRONMENT_CANDIDATES: Tuple[str, ...] = (
    _PRODUCTION_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _DEVELOPMENT_ENVIRONMENT,
    _SANDBOX_ENVIRONMENT,
)


def _get_compatible_yaml_versions() -> Optional[List[str]]:
    """Get the compatible yaml versions.

    If plugins are used, they need to contain the compatible
    version in the plugins directory in a __version__.py file.
    Else we use the version defined in __version__.py
    """
    # check if __version__.py exists in the plugins directory
    if os.path.exists(BITFOUNT_PLUGIN_PATH / "__version__.py"):
        spec = util.spec_from_file_location(
            "__version__", BITFOUNT_PLUGIN_PATH / "__version__.py"
        )
        spec = cast(
            ModuleSpec, spec
        )  # safe to cast as the version module is always present
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr] # reason: this should not be None as the module always exists # noqa: B950
        plugin_yaml_version: Optional[List[str]] = None
        try:
            plugin_yaml_version = mod.__yaml__versions__
        except AttributeError:
            logger.debug(
                "No yaml versioning found in the plugins directory, "
                "using yaml versioning from the bitfount package."
            )
        return plugin_yaml_version
    else:
        logger.debug(
            "The current plugins directory is not versioned, "
            "using yaml versioning from the bitfount package."
        )
        return None


plugin_versions = _get_compatible_yaml_versions()
_BITFOUNT_COMPATIBLE_YAML_VERSIONS: List[str] = (
    plugin_versions if plugin_versions is not None else yaml_versions
)


@lru_cache(maxsize=1)
def _get_environment() -> str:
    """Returns bitfount environment to be used from BITFOUNT_ENVIRONMENT variable.

    The result is cached to avoid multiple warning messages. This means that changes to
    the `BITFOUNT_ENVIRONMENT` environment variable will not be detected whilst the
    library is running.

    Returns:
        str: PRODUCTION_ENVIRONMENT, STAGING_ENVIRONMENT, DEVELOPMENT_ENVIRONMENT or
            SANDBOX_ENVIRONMENT

    """
    BITFOUNT_ENVIRONMENT = os.getenv("BITFOUNT_ENVIRONMENT", _PRODUCTION_ENVIRONMENT)
    if BITFOUNT_ENVIRONMENT not in _ENVIRONMENT_CANDIDATES:
        raise ValueError(
            f"The environment specified by the environment variable "
            f"BITFOUNT_ENVIRONMENT ({BITFOUNT_ENVIRONMENT}) is not in the supported "
            f"list of environments ({_ENVIRONMENT_CANDIDATES})"
        )
    if BITFOUNT_ENVIRONMENT == _STAGING_ENVIRONMENT:
        logger.warning(
            "Using the staging environment. "
            + "This will only work for Bitfount employees."
        )
    if BITFOUNT_ENVIRONMENT == _DEVELOPMENT_ENVIRONMENT:
        logger.warning(
            "Using the development environment. "
            + "This will only work if you have all Bitfount services running locally."
        )
    if BITFOUNT_ENVIRONMENT == _SANDBOX_ENVIRONMENT:
        logger.warning(
            "Using the sandbox environment. "
            + "This will only work for Bitfount employees."
        )
    return BITFOUNT_ENVIRONMENT


###############################################
# End of Private Config/Environment Variables #
###############################################

##################
# Backend Engine #
##################
_PYTORCH_ENGINE: Final[str] = "pytorch"
_BASIC_ENGINE: Final[str] = "basic"
_ENGINE_CANDIDATES: Tuple[str, ...] = (
    _BASIC_ENGINE,
    _PYTORCH_ENGINE,
)

# Set BITFOUNT_ENGINE, defaulting to PYTORCH_ENGINE or BASIC_ENGINE
# Start with BASIC_ENGINE as default
BITFOUNT_ENGINE: str = _BASIC_ENGINE
try:
    # Use the type specified by envvar if present
    BITFOUNT_ENGINE = os.environ["BITFOUNT_ENGINE"]
    # Check that the engine option is a valid one
    if BITFOUNT_ENGINE not in _ENGINE_CANDIDATES:
        raise ValueError(
            f"The backend engine specified by the environment variable "
            f"BITFOUNT_ENGINE ({BITFOUNT_ENGINE}) is not in the supported list of "
            f"backends ({_ENGINE_CANDIDATES})"
        )
except KeyError:
    # Otherwise, if PyTorch is installed use PYTORCH_ENGINE
    try:
        import torch  # noqa: F401

        BITFOUNT_ENGINE = _PYTORCH_ENGINE
    except ImportError:
        pass
#########################
# End of Backend Engine #
#########################

##############
# DP Support #
##############
DP_AVAILABLE: bool
try:
    import opacus  # noqa: F401

    DP_AVAILABLE = True
except ImportError:
    logger.warning("Differential Privacy requirements not installed.")
    DP_AVAILABLE = False
#####################
# End of DP Support #
#####################


#############################
# GPU information retrieval #
#############################
def _get_gpu_metadata_gputil() -> Tuple[Optional[str], int]:
    """Returns gpu metadata from GPUtil.

    Uses the name of the first GPU thereby assuming that there is only 1 type of GPU
    attached to the machine.

    Returns:
        Tuple[Optional[str], int]: name of gpu and how many there are
    """
    gpus = GPUtil.getGPUs()
    if gpus:
        return gpus[0].name, len(gpus)
    # nvidia-smi installed, but no GPU available
    return None, 0


def _get_gpu_metadata_pytorch() -> Tuple[Optional[str], int]:
    """Return gpu metadata from pytorch.

    Returns:
        Tuple[Optional[str], int]: name of gpu and how many there are
    """
    import torch.cuda as cuda

    if cuda.is_available():
        # Devices without CUDA can still use pytorch,
        # but this will throw an exception
        return cuda.get_device_name(), cuda.device_count()
    else:
        raise Exception("CUDA not available.")


_GPU_COUNT_FUNCTION_LOOKUP: Dict[str, Callable[..., Tuple[Optional[str], int]]] = {
    _BASIC_ENGINE: _get_gpu_metadata_gputil,
    _PYTORCH_ENGINE: _get_gpu_metadata_pytorch,
}


def get_gpu_metadata() -> Tuple[Optional[str], int]:
    """Retrieve details about GPUs if available.

    Uses tools available in the appropriate backend,
    to find GPUs that are usable by the backend.

    Returns: a tuple of GPU name and count.
    """
    # noinspection PyBroadException
    try:
        return _GPU_COUNT_FUNCTION_LOOKUP[BITFOUNT_ENGINE]()
    except Exception as ex:
        # Broad exception handling here as libraries may throw various exceptions
        # But if anything is raised we can assume we don't have GPU access
        logger.warning(f"Encountered exception whilst gathering GPU information: {ex}")
        logger.warning("No GPU info will be used.")
        return None, 0


####################################
# End of GPU information retrieval #
####################################
