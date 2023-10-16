"""Hook infrastructure for Bitfount."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from functools import partial, wraps
import logging
from types import FunctionType, MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    cast,
    overload,
    runtime_checkable,
)

from bitfount.exceptions import HookError

if TYPE_CHECKING:
    from bitfount.data.datasources.base_source import FileSystemIterableSource
    from bitfount.federated.algorithms.base import _BaseAlgorithm
    from bitfount.federated.helper import TaskContext
    from bitfount.federated.pod import Pod
    from bitfount.federated.protocols.base import _BaseProtocol

__all__: List[str] = [
    "BaseAlgorithmHook",
    "BasePodHook",
    "HookType",
    "get_hooks",
]

logger = logging.getLogger(__name__)

_HOOK_DECORATED_ATTRIBUTE = "_decorate"


class HookType(Enum):
    """Enum for hook types."""

    POD = "POD"
    ALGORITHM = "ALGORITHM"
    PROTOCOL = "PROTOCOL"


@runtime_checkable
class HookProtocol(Protocol):
    """Base Protocol for hooks used just for type annotation."""

    hook_name: str

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        ...

    @property
    def registered(self) -> bool:
        """Return whether the hook is registered."""
        ...

    def register(self) -> None:
        """Register the hook.

        Adds hook to the registry against the hook type.
        """
        ...


@runtime_checkable
class PodHookProtocol(HookProtocol, Protocol):
    """Protocol for Pod hooks."""

    def on_pod_init_start(
        self,
        pod: Pod,
        pod_name: str,
        username: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook at the very start of pod initialisation."""
        ...

    def on_pod_init_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod initialisation."""
        ...

    def on_pod_init_error(
        self, pod: Pod, exception: BaseException, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook if an uncaught exception is raised during pod initialisation."""
        ...

    def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod startup."""
        ...

    def on_pod_startup_error(
        self, pod: Pod, exception: BaseException, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook if an uncaught exception is raised during pod startup."""
        ...

    def on_pod_startup_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod startup."""
        ...

    def on_task_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the start."""
        ...

    def on_task_error(
        self, pod: Pod, exception: BaseException, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook when there is an exception in a task."""
        ...

    def on_task_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the end."""
        ...

    def on_pod_shutdown_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod shutdown."""
        ...

    def on_pod_shutdown_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of pod shutdown."""
        ...

    def on_file_process_start(
        self,
        datasource: FileSystemIterableSource,
        file_num: int,
        total_num_files: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook when a file starts to be processed."""
        ...

    def on_file_process_end(
        self,
        datasource: FileSystemIterableSource,
        file_num: int,
        total_num_files: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook when a file processing ends."""
        ...


@runtime_checkable
class AlgorithmHookProtocol(HookProtocol, Protocol):
    """Protocol for Algorithm hooks."""

    def on_init_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm initialisation."""
        ...

    def on_init_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm initialisation."""
        ...

    def on_run_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm run."""
        ...

    def on_run_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm run."""
        ...


@runtime_checkable
class ProtocolHookProtocol(HookProtocol, Protocol):
    """Protocol for Protocol hooks."""

    def on_init_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol initialisation."""
        ...

    def on_init_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol initialisation."""
        ...

    def on_run_start(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of protocol run."""
        ...

    def on_run_end(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very end of protocol run."""
        ...


HOOK_TYPE_TO_PROTOCOL_MAPPING: Dict[HookType, Type[HookProtocol]] = {
    HookType.POD: PodHookProtocol,
    HookType.ALGORITHM: AlgorithmHookProtocol,
    HookType.PROTOCOL: ProtocolHookProtocol,
}

# The mutable underlying dict that holds the registry information
_registry: Dict[HookType, List[HookProtocol]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[HookType, List[HookProtocol]] = MappingProxyType(_registry)


@overload
def get_hooks(type: Literal[HookType.POD]) -> List[PodHookProtocol]:
    ...


@overload
def get_hooks(type: Literal[HookType.ALGORITHM]) -> List[AlgorithmHookProtocol]:
    ...


@overload
def get_hooks(type: Literal[HookType.PROTOCOL]) -> List[ProtocolHookProtocol]:
    ...


def get_hooks(
    type: HookType,
) -> Union[
    List[AlgorithmHookProtocol], List[PodHookProtocol], List[ProtocolHookProtocol]
]:
    """Get all registered hooks of a particular type.

    Args:
        type: The type of hook to get.

    Returns:
        A list of hooks of the provided type.

    Raises:
        ValueError: If the provided type is not a valid hook type.
    """
    hooks = registry.get(type, [])
    if type == HookType.POD:
        return cast(List[PodHookProtocol], hooks)
    elif type == HookType.ALGORITHM:
        return cast(List[AlgorithmHookProtocol], hooks)
    elif type == HookType.PROTOCOL:
        return cast(List[ProtocolHookProtocol], hooks)

    raise ValueError(f"Unknown hook type {type}")


def ignore_decorator(f: Callable) -> Callable:
    """Decorator to exclude methods from autodecoration."""
    setattr(f, _HOOK_DECORATED_ATTRIBUTE, False)
    return f


def _on_pod_error(hook_name: str, f: Callable) -> Callable:
    """Pod method decorator which catches exceptions in the method.

    If an exception is caught, all registered pod hooks with the provided `hook_name`
    are called.

    Args:
        hook_name: The name of the hook to call if an exception is caught.
        f: The method to decorate.
    """

    @wraps(f)
    def pod_method_wrapper(self: Pod, *args: Any, **kwargs: Any) -> Any:
        """Wraps provided function and calls the relevant hook if there is an exception.

        Re-raises the exception if there are no hooks registered.
        """
        try:
            return_val = f(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in pod {f.__name__}")
            hooks = get_hooks(HookType.POD)
            # Re-raise the exception if there are no hooks registered
            if not hooks:
                raise
            # Otherwise log the exception and call the hooks
            logger.exception(e)
            for hook in hooks:
                try:
                    getattr(hook, hook_name)(self, e)  # Passing pod instance to hook
                # If Pod hooks are registered but do not have the hook, log a warning
                except NotImplementedError:
                    logger.warning(
                        f"{hook.hook_name} has not implemented hook {hook_name}"
                    )
        else:
            return return_val

    return pod_method_wrapper


#: Decorator to be used on Pod.__init__ method.
on_pod_init_error: Callable[[Callable], Callable] = partial(
    _on_pod_error, "on_pod_init_error"
)

#: Decorator to be used on Pod.start method.
on_pod_startup_error: Callable[[Callable], Callable] = partial(
    _on_pod_error, "on_pod_startup_error"
)


class BaseDecoratorMetaClass(type):
    """Base Metaclass for auto-decorating specific methods of a class."""

    @classmethod
    @abstractmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decorator(f: Callable) -> Callable:
        """Returns the decorator to use."""
        raise NotImplementedError

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
    ) -> type:
        """Creates a new class with specific methods decorated.

        The methods to decorate are determined by the `do_decorate` method. The class
        must not be abstract.
        """
        # Only decorate if the class is not a subclass of ABC i.e. not abstract
        if ABC not in bases:
            for attr, value in dct.items():
                if cls.do_decorate(attr, value):
                    setattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
                    dct[attr] = cls.decorator(value)
        return super().__new__(cls, name, bases, dct)

    def __setattr__(self, attr: str, value: Any) -> None:
        if self.do_decorate(attr, value):
            value = self.decorator(value)
        super().__setattr__(attr, value)


class HookDecoratorMetaClass(BaseDecoratorMetaClass, type):
    """Decorate all instance methods (unless excluded) with the same decorator."""

    @staticmethod
    def decorator(f: Callable) -> Callable:
        """Hook decorator which logs before and after the hook it decorates.

        The decorator also catches any exceptions in the hook so that a hook can never
        be the cause of an error.
        """

        @wraps(f)
        def wrapper(self: BaseHook, *args: Any, **kwargs: Any) -> Any:
            """Wraps provided function and prints before and after."""
            logger.debug(f"Calling hook {f.__name__} from {self.hook_name}")
            try:
                return_val = f(self, *args, **kwargs)
            # NotImplementedError is re-raised as this is unrelated to the behaviour
            # of the hook and is re-caught elsewhere if necessary
            except NotImplementedError:
                raise
            except Exception as e:
                logger.error(f"Exception in hook {f.__name__} from {self.hook_name}")
                logger.exception(e)
            else:
                logger.debug(f"Called hook {f.__name__} from {self.hook_name}")
                return return_val

        return wrapper

    @classmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated.

        Private methods beginning with an underscore are not decorated.
        """
        return (
            "__" not in attr
            and not attr.startswith("_")
            and isinstance(value, FunctionType)
            and getattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
        )


class BaseHook(metaclass=HookDecoratorMetaClass):
    """Base hook class."""

    def __init__(self) -> None:
        """Initialise the hook."""
        self.hook_name = type(self).__name__

    @property
    @abstractmethod
    def type(self) -> HookType:
        """Return the hook type."""
        raise NotImplementedError

    @property
    def registered(self) -> bool:
        """Return whether the hook is registered."""
        return self.hook_name in [h.hook_name for h in _registry.get(self.type, [])]

    @ignore_decorator
    def register(self) -> None:
        """Register the hook.

        Adds hook to the registry against the hook type.
        """
        if not isinstance(self, HOOK_TYPE_TO_PROTOCOL_MAPPING[self.type]):
            raise HookError("Hook does not implement the specified protocol")

        if self.registered:
            logger.info(f"{self.hook_name} hook already registered")
            return

        logger.debug(f"Adding {self.hook_name} to Hooks registry")
        existing_hooks = _registry.get(self.type, [])
        existing_hooks.append(self)
        _registry[self.type] = existing_hooks
        logger.info(f"Added {self.hook_name} to Hooks registry")


class BasePodHook(BaseHook):
    """Base pod hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.POD

    def on_pod_init_start(
        self,
        pod: Pod,
        pod_name: str,
        username: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook at the very start of pod initialisation."""
        pass

    def on_pod_init_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod initialisation."""
        pass

    def on_pod_init_error(
        self, pod: Pod, exception: Exception, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook if an uncaught exception is raised during pod initialisation.

        Raises:
            NotImplementedError: If the hook is not implemented. This is to ensure that
                underlying exceptions are not swallowed if the hook is not implemented.
                This error is caught further up the chain and the underlying exception
                is raised instead.
        """
        raise NotImplementedError()

    def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod startup."""
        pass

    def on_pod_startup_error(
        self, pod: Pod, exception: Exception, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook if an uncaught exception is raised during pod startup.

        Raises:
            NotImplementedError: If the hook is not implemented. This is to ensure that
                underlying exceptions are not swallowed if the hook is not implemented.
                This error is caught further up the chain and the underlying exception
                is raised instead.
        """
        raise NotImplementedError()

    def on_pod_startup_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod startup."""
        pass

    def on_task_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the start."""
        pass

    def on_task_error(
        self, pod: Pod, exception: BaseException, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook when there is an exception in a task."""
        pass

    def on_task_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the end."""
        pass

    def on_pod_shutdown_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod shutdown."""
        pass

    def on_pod_shutdown_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of pod shutdown."""
        pass

    def on_file_process_start(
        self,
        datasource: FileSystemIterableSource,
        file_num: int,
        total_num_files: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook when a file starts to be processed."""
        pass

    def on_file_process_end(
        self,
        datasource: FileSystemIterableSource,
        file_num: int,
        total_num_files: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the hook when a file processing ends."""
        pass


class BaseAlgorithmHook(BaseHook):
    """Base algorithm hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.ALGORITHM

    def on_init_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm initialisation."""
        pass

    def on_init_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm initialisation."""
        pass

    def on_run_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm run."""
        pass

    def on_run_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm run."""
        pass


class BaseProtocolHook(BaseHook):
    """Base protocol hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.PROTOCOL

    def on_init_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol initialisation."""
        pass

    def on_init_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol initialisation."""
        pass

    def on_run_start(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of protocol run."""
        pass

    def on_run_end(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very end of protocol run."""
        pass
