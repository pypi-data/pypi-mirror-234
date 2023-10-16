"""Pod communication protocols.

These classes take an algorithm and are responsible for organising the communication
between Pods and Modeller.

Attributes:
    registry: A read-only dictionary of protocol factory names to their
        implementation classes.
"""
from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
import asyncio
from functools import wraps
import inspect
from pathlib import Path
import types
from types import FunctionType, MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Final,
    Generic,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from bitfount.config import BITFOUNT_DEFAULT_BATCHED_EXECUTION, BITFOUNT_TASK_BATCH_SIZE
from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.types import DataSplit
import bitfount.federated.algorithms.base as algorithms
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.exceptions import (
    AlgorithmError,
    BitfountTaskStartError,
    ProtocolError,
)
from bitfount.federated.helper import (
    TaskContext,
    _check_and_update_pod_ids,
    _create_message_service,
    _get_idp_url,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.modeller import _Modeller
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.roles import _RolesMixIn
from bitfount.federated.transport.base_transport import _BaseMailbox
from bitfount.federated.transport.config import MessageServiceConfig
from bitfount.federated.transport.message_service import _MessageService
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.utils import _compute_backoff
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import ProtocolType, SerializedProtocol
from bitfount.hooks import (
    _HOOK_DECORATED_ATTRIBUTE,
    BaseDecoratorMetaClass,
    HookType,
    get_hooks,
)
from bitfount.hub.helper import _default_bitfounthub
from bitfount.schemas.utils import bf_dump
from bitfount.types import (
    T_FIELDS_DICT,
    T_NESTED_FIELDS,
    _BaseSerializableObjectMixIn,
    _StrAnyDict,
)

if TYPE_CHECKING:
    from bitfount.federated.pod_vitals import _PodVitals
    from bitfount.hub.api import BitfountHub
    from bitfount.hub.authentication_flow import BitfountSession


logger = _get_federated_logger(__name__)

MAXIMUM_SLEEP_TIME: Final = 10.0


class ProtocolDecoratorMetaClass(BaseDecoratorMetaClass, type):
    """Decorates the `__init__` and `run` protocol methods."""

    @staticmethod
    def decorator(f: Callable) -> Callable:
        """Hook decorator which logs before and after the hook it decorates."""
        method_name = f.__name__
        if method_name == "__init__":

            @wraps(f)
            def init_wrapper(
                self: _BaseProtocol,
                hook_kwargs: Optional[_StrAnyDict] = None,
                *args: Any,
                **kwargs: Any,
            ) -> None:
                """Wraps __init__ method of protocol.

                Calls relevant hooks before and after the protocol is initialised.

                Args:
                    self: The protocol instance.
                    hook_kwargs: Keyword arguments to pass to the hooks.
                    *args: Positional arguments to pass to the protocol.
                    **kwargs: Keyword arguments to pass to the protocol.
                """
                hook_kwargs = hook_kwargs or {}
                for hook in get_hooks(HookType.PROTOCOL):
                    hook.on_init_start(self, **hook_kwargs)
                logger.debug(f"Calling method {method_name} from protocol")
                f(self, *args, **kwargs)
                for hook in get_hooks(HookType.PROTOCOL):
                    hook.on_init_end(self, **hook_kwargs)

            return init_wrapper

        elif method_name == "run":

            @wraps(f)
            async def run_wrapper(
                self: _BaseProtocol,
                context: Optional[TaskContext] = None,
                batched_execution: Optional[bool] = None,
                hook_kwargs: Optional[_StrAnyDict] = None,
                *args: Any,
                **kwargs: Any,
            ) -> Union[Any, List[Any]]:
                """Wraps run method of protocol.

                Calls hooks before and after the run method is called and also
                orchestrates batched execution if set to True.

                Args:
                    self: Protocol instance.
                    context: Context in which the protocol is being run. Only required
                        if batched_execution is True.
                    batched_execution: Whether to run the protocol in batched mode.
                    hook_kwargs: Keyword arguments to pass to the hooks.
                    *args: Positional arguments to pass to the run method.
                    **kwargs: Keyword arguments to pass to the run method.

                Returns:
                    Return value of the run method. Or a list of return values if
                    batched_execution is True.

                Raises:
                    BitfountTaskStartError: If batched_execution is True but the
                        datasource does not support batched execution.
                    AlgorithmError: This is caught and re-raised.
                    ProtocolError: Any error that is raised in the protocol run that
                        is not an AlgorithmError is raised as a ProtocolError.
                """
                return_values = []
                hook_kwargs = hook_kwargs or {}
                num_batches: int = 1
                datasource: Optional[BaseSource] = None
                mailbox: Union[_WorkerMailbox, _ModellerMailbox]
                hook_kwargs["context"] = context
                if batched_execution is None:
                    batched_execution = BITFOUNT_DEFAULT_BATCHED_EXECUTION
                try:
                    # This should never be raised as the protocol run method is called
                    # by our own worker and modeller classes which always pass the
                    # context
                    if batched_execution and not isinstance(context, TaskContext):
                        raise BitfountTaskStartError(
                            "Context must be provided for batched execution."
                        )
                    if batched_execution and context == TaskContext.WORKER:
                        self = cast(BaseWorkerProtocol, self)
                        try:
                            datasource = self.datasource
                        except Exception as e:
                            raise BitfountTaskStartError(
                                "Protocol has not been initialised with a datasource."
                            ) from e

                        batch_size = BITFOUNT_TASK_BATCH_SIZE
                        data_splitter = datasource.data_splitter or PercentageSplitter()
                        if isinstance(datasource, FileSystemIterableSource):
                            original_selected_test_file_names = (
                                data_splitter.get_filenames(datasource, DataSplit.TEST)
                            )
                            original_selected_file_names_override = (
                                datasource.selected_file_names_override
                            )
                            datasource_len = len(original_selected_test_file_names)
                        elif datasource.iterable:
                            raise BitfountTaskStartError(
                                "Batched execution is not supported for non-filesystem "
                                "iterable sources."
                            )
                        else:
                            if datasource._test_idxs is None:
                                (
                                    datasource._train_idxs,
                                    datasource._validation_idxs,
                                    datasource._test_idxs,
                                ) = data_splitter.create_dataset_splits(datasource.data)
                            assert (
                                datasource._test_idxs is not None
                            )  # nosec assert_used
                            original_test_indices = datasource._test_idxs
                            datasource_len = len(original_test_indices)

                        # Calculate the number of batches in the test set
                        num_batches = datasource_len // batch_size
                        if datasource_len % batch_size != 0:
                            num_batches += 1
                        # Send the total number of batches to the modeller
                        await self.mailbox.send_num_batches_message(num_batches)
                    elif batched_execution and context == TaskContext.MODELLER:
                        # Get the total number of batches from the worker
                        mailbox = cast(_ModellerMailbox, self.mailbox)
                        num_batches = await mailbox.get_num_batches_message()

                    # Loop through the batches of data. If batched_execution is False,
                    # this loop will only run once.
                    final_batch: bool = not batched_execution
                    for batch_num in range(num_batches):
                        logger.info(
                            f"Running batch {batch_num + 1} of {num_batches}..."
                        )
                        if batched_execution and context == TaskContext.WORKER:
                            datasource = cast(BaseSource, datasource)
                            if batch_num == num_batches - 1:
                                final_batch = True
                            start_idx = batch_num * batch_size
                            end_idx = (
                                (batch_num + 1) * batch_size
                                if not final_batch
                                else None
                            )
                            # FileSystemIterableSource and other non-iterable sources
                            # are the only two types of source that are possible at this
                            # point as we will have raised an error already if the
                            # datasource is anything else.
                            if isinstance(datasource, FileSystemIterableSource):
                                datasource.selected_file_names_override = (
                                    original_selected_test_file_names[start_idx:end_idx]
                                )
                            else:
                                datasource._test_idxs = original_test_indices[
                                    start_idx:end_idx
                                ]

                            # Reinitialise the algorithms with the new datasource
                            for algo in self.algorithms:
                                algo = cast(BaseCompatibleWorkerAlgorithm, algo)
                                algo.initialise_data(datasource=datasource)

                        # Call on_run_start hooks
                        hook_kwargs["batch_num"] = batch_num
                        hook_kwargs["num_batches"] = num_batches
                        for hook in get_hooks(HookType.PROTOCOL):
                            hook.on_run_start(self, **hook_kwargs)

                        # Await on the other party/parties being ready before proceeding
                        # with the first batch. This applies regardless of whether
                        # batched_execution is True or False; in the False case we
                        # implicitly just have a single "batch".
                        if batch_num == 0:
                            retry_count = 0
                            await self.mailbox.send_task_start_message()
                            if context == TaskContext.WORKER:
                                mailbox = cast(_WorkerMailbox, self.mailbox)
                                while not mailbox.modeller_ready:
                                    retry_count += 1
                                    await asyncio.sleep(
                                        min(
                                            MAXIMUM_SLEEP_TIME,
                                            _compute_backoff(retry_count),
                                        )
                                    )
                                    logger.info("Waiting for modeller to be ready...")
                                logger.info("Modeller is ready. Starting task...")
                            elif context == TaskContext.MODELLER:
                                mailbox = cast(_ModellerMailbox, self.mailbox)
                                while not mailbox.pods_ready:
                                    retry_count += 1
                                    await asyncio.sleep(
                                        min(
                                            MAXIMUM_SLEEP_TIME,
                                            _compute_backoff(retry_count),
                                        )
                                    )
                                    logger.info("Waiting for pod(s) to be ready...")
                                logger.info("Pod(s) are ready. Starting task...")

                        # Await on the run method of the protocol
                        try:
                            return_val = await f(
                                self, *args, final_batch=final_batch, **kwargs
                            )
                            hook_kwargs["results"] = return_val
                            return_values.append(return_val)
                        except AlgorithmError:
                            raise
                        except Exception as e:
                            raise ProtocolError(
                                f"Protocol {self.__class__.__name__} "
                                f"raised the following exception: {e}"
                            ) from e

                        # Call on_run_end hooks
                        for hook in get_hooks(HookType.PROTOCOL):
                            hook.on_run_end(self, **hook_kwargs)
                except BitfountTaskStartError:
                    # If the task did not start correctly, the datasource was not
                    # modified so it does not need to be reset.
                    raise
                except Exception as e:
                    # Log the exception before re-raising it in case there is
                    # another exception encountered before then
                    logger.exception(e)
                    raise
                finally:
                    # Return datasource to original state
                    if (
                        batched_execution
                        and context == TaskContext.WORKER
                        and datasource is not None
                    ):
                        self = cast(BaseWorkerProtocol, self)
                        if isinstance(datasource, FileSystemIterableSource):
                            datasource.selected_file_names_override = (
                                original_selected_file_names_override
                            )
                        elif not datasource.iterable:
                            datasource._test_idxs = original_test_indices

                        self.datasource = datasource

                if batched_execution:
                    return return_values

                # If batched_execution is False, return the return value of the run. We
                # don't need to return a list of return values as there is only one.
                return return_val

            return run_wrapper

        # This is not expected to ever happen, but if it does, raise an error
        raise ValueError(f"Method {method_name} cannot be decorated.")

    @classmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated.

        Only the __init__ and run methods should be decorated.
        """
        return (
            attr in ("__init__", "run")
            and isinstance(value, FunctionType)
            and getattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
        )


MB = TypeVar("MB", bound=_BaseMailbox)

# The metaclass for the BaseProtocol must also have all the same classes in its own
# inheritance chain so we need to create a thin wrapper around it.
AbstractProtocolDecoratorMetaClass = types.new_class(
    "AbstractProtocolDecoratorMetaClass",
    (Generic[MB], ABCMeta, ProtocolDecoratorMetaClass),
    {},
)


# Mypy doesn't yet support metaclasses with generics
class _BaseProtocol(Generic[MB], ABC, metaclass=AbstractProtocolDecoratorMetaClass):  # type: ignore[misc] # Reason: see above # noqa: B950
    """Blueprint for modeller side or the worker side of BaseProtocolFactory."""

    def __init__(
        self,
        *,
        algorithm: Union[
            BaseCompatibleModellerAlgorithm,
            Sequence[BaseCompatibleModellerAlgorithm],
            BaseCompatibleWorkerAlgorithm,
            Sequence[BaseCompatibleWorkerAlgorithm],
        ],
        mailbox: MB,
        **kwargs: Any,
    ):
        self.algorithm = algorithm
        self.mailbox = mailbox

        super().__init__(**kwargs)

    @property
    def algorithms(
        self,
    ) -> List[Union[BaseCompatibleModellerAlgorithm, BaseCompatibleWorkerAlgorithm]]:
        """Returns the algorithms in the protocol."""
        if isinstance(self.algorithm, Sequence):
            return list(self.algorithm)
        return [self.algorithm]


class BaseCompatibleModellerAlgorithm(Protocol):
    """Protocol defining base modeller-side algorithm compatibility."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the algorithm."""
        pass


class BaseModellerProtocol(_BaseProtocol[_ModellerMailbox], ABC):
    """Modeller side of the protocol.

    Calls the modeller side of the algorithm.
    """

    def __init__(
        self,
        *,
        algorithm: Union[
            BaseCompatibleModellerAlgorithm, Sequence[BaseCompatibleModellerAlgorithm]
        ],
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the component algorithms."""
        for algo in self.algorithms:
            algo.initialise(
                task_id=task_id,
                **kwargs,
            )

    @abstractmethod
    async def run(
        self,
        **kwargs: Any,
    ) -> Any:
        """Runs Modeller side of the protocol."""
        pass


class BaseCompatibleWorkerAlgorithm(Protocol):
    """Protocol defining base worker-side algorithm compatibility."""

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the algorithm."""
        pass

    def initialise_data(self, datasource: BaseSource) -> None:
        """Initialises the data for the algorithm."""
        pass


class BaseWorkerProtocol(_BaseProtocol[_WorkerMailbox], ABC):
    """Worker side of the protocol.

    Calls the worker side of the algorithm.
    """

    datasource: BaseSource
    mailbox: _WorkerMailbox

    def __init__(
        self,
        *,
        algorithm: Union[
            BaseCompatibleWorkerAlgorithm, Sequence[BaseCompatibleWorkerAlgorithm]
        ],
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the component algorithms."""
        self.datasource = datasource
        for algo in self.algorithms:
            algo.initialise(
                datasource=datasource,
                pod_dp=pod_dp,
                pod_identifier=pod_identifier,
                **kwargs,
            )

    @abstractmethod
    async def run(
        self,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> Any:
        """Runs the worker-side of the algorithm."""
        pass


# The mutable underlying dict that holds the registry information
_registry: Dict[str, Type[BaseProtocolFactory]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[str, Type[BaseProtocolFactory]] = MappingProxyType(_registry)


class BaseCompatibleAlgoFactory(Protocol):
    """Protocol defining base algorithm factory compatibility."""

    class_name: str
    fields_dict: ClassVar[T_FIELDS_DICT] = {}
    nested_fields: ClassVar[T_NESTED_FIELDS] = {}


class BaseProtocolFactory(ABC, _RolesMixIn, _BaseSerializableObjectMixIn):
    """Base Protocol from which all other protocols must inherit."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {}
    nested_fields: ClassVar[T_NESTED_FIELDS] = {"algorithm": algorithms.registry}

    def __init__(
        self,
        *,
        algorithm: Union[
            BaseCompatibleAlgoFactory, Sequence[BaseCompatibleAlgoFactory]
        ],
        **kwargs: Any,
    ) -> None:
        try:
            self.class_name = ProtocolType[type(self).__name__].value
        except KeyError:
            # Check if the protocol is a plug-in
            self.class_name = type(self).__name__

        super().__init__(**kwargs)
        self.algorithm = algorithm
        for algo in self.algorithms:
            self._validate_algorithm(algo)

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        if not inspect.isabstract(cls):
            logger.debug(f"Adding {cls.__name__}: {cls} to Protocol registry")
            _registry[cls.__name__] = cls

    @property
    def algorithms(self) -> List[BaseCompatibleAlgoFactory]:
        """Returns the algorithms in the protocol."""
        if isinstance(self.algorithm, Sequence):
            return list(self.algorithm)
        return [self.algorithm]

    @classmethod
    @abstractmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Checks that `algorithm` is compatible with the protocol.

        Raises TypeError if `algorithm` is not compatible with the protocol.
        """
        pass

    @abstractmethod
    def modeller(
        self, mailbox: _ModellerMailbox, **kwargs: Any
    ) -> BaseModellerProtocol:
        """Creates an instance of the modeller-side for this protocol."""
        raise NotImplementedError

    @abstractmethod
    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> BaseWorkerProtocol:
        """Creates an instance of the worker-side for this protocol."""
        raise NotImplementedError

    def dump(self) -> SerializedProtocol:
        """Returns the JSON-serializable representation of the protocol."""
        return cast(SerializedProtocol, bf_dump(self))

    def run(
        self,
        pod_identifiers: Collection[str],
        session: Optional[BitfountSession] = None,
        username: Optional[str] = None,
        hub: Optional[BitfountHub] = None,
        ms_config: Optional[MessageServiceConfig] = None,
        message_service: Optional[_MessageService] = None,
        pod_public_key_paths: Optional[Mapping[str, Path]] = None,
        identity_verification_method: IdentityVerificationMethod = IdentityVerificationMethod.DEFAULT,  # noqa: B950
        private_key_or_file: Optional[Union[RSAPrivateKey, Path]] = None,
        idp_url: Optional[str] = None,
        require_all_pods: bool = False,
        run_on_new_data_only: bool = False,
        model_out: Optional[Union[Path, str]] = None,
        project_id: Optional[str] = None,
        batched_execution: Optional[bool] = None,
    ) -> Optional[Any]:
        """Sets up a local Modeller instance and runs the protocol.

        Args:
            pod_identifiers: The BitfountHub pod identifiers to run against.
            session: Optional. Session to use for authenticated requests.
                 Created if needed.
            username: Username to run as. Defaults to logged in user.
            hub: BitfountHub instance. Default: hub.bitfount.com.
            ms_config: Message service config. Default: messaging.bitfount.com.
            message_service: Message service instance, created from ms_config if not
                provided. Defaults to "messaging.bitfount.com".
            pod_public_key_paths: Public keys of pods to be checked against.
            identity_verification_method: The identity verification method to use.
            private_key_or_file: Private key (to be removed).
            idp_url: The IDP URL.
            require_all_pods: If true raise PodResponseError if at least one pod
                identifier specified rejects or fails to respond to a task request.
            run_on_new_data_only: Whether to run the task on new datapoints only.
                Defaults to False.
            batched_execution: Whether to run the task in batched mode. Defaults to
                False.

        Returns:
            Results of the protocol.

        Raises:
            PodResponseError: If require_all_pods is true and at least one pod
                identifier specified rejects or fails to respond to a task request.
            ValueError: If attempting to train on multiple pods, and the
                `DataStructure` table name is given as a string.
        """
        hub = _default_bitfounthub(hub=hub, username=username)
        if batched_execution is None:
            batched_execution = BITFOUNT_DEFAULT_BATCHED_EXECUTION
        if len(pod_identifiers) > 1 and batched_execution:
            logger.warning(
                "Batched execution is only supported for single pod tasks. "
                "Resuming task without batched execution."
            )
            batched_execution = False

        for algo in self.algorithms:
            if isinstance(algo, _BaseModelAlgorithmFactory):
                if (
                    len(pod_identifiers) > 1
                    and hasattr(algo.model.datastructure, "table")
                    and isinstance(algo.model.datastructure.table, str)
                ):
                    raise ValueError(
                        "You are attempting to train on multiple pods, and the "
                        "provided the DataStructure table name is a string. "
                        "Please make sure that the `table` argument to the "
                        "`DataStructure` is a mapping of Pod names to table names. "
                    )
                pod_identifiers = _check_and_update_pod_ids(pod_identifiers, hub)
                datastructure_pod_identifiers = (
                    algo.model.datastructure.get_pod_identifiers()
                )
                if datastructure_pod_identifiers:
                    datastructure_pod_identifiers = _check_and_update_pod_ids(
                        datastructure_pod_identifiers, hub
                    )
                    algo.model.datastructure._update_datastructure_with_hub_identifiers(
                        datastructure_pod_identifiers
                    )
        if not session:
            session = hub.session
        if not idp_url:
            idp_url = _get_idp_url()
        if not message_service:
            message_service = _create_message_service(
                session=session,
                ms_config=ms_config,
            )

        modeller = _Modeller(
            protocol=self,
            message_service=message_service,
            bitfounthub=hub,
            pod_public_key_paths=pod_public_key_paths,
            identity_verification_method=identity_verification_method,
            private_key=private_key_or_file,
            idp_url=idp_url,
        )
        name = type(self).__name__

        logger.info(f"Starting {name} Task...")

        result = modeller.run(
            pod_identifiers,
            require_all_pods=require_all_pods,
            project_id=project_id,
            model_out=model_out,
            run_on_new_data_only=run_on_new_data_only,
            batched_execution=batched_execution,
        )
        logger.info(f"Completed {name} Task.")
        return result
