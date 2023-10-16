"""Pods for responding to tasks."""
import asyncio
from contextlib import nullcontext
from dataclasses import dataclass
import os
import threading
from typing import (
    Any,
    Callable,
    ContextManager,
    Coroutine,
    Dict,
    Iterable,
    List,
    MutableMapping,
    MutableSequence,
    Optional,
    Tuple,
    Union,
    cast,
)
import warnings

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import pandas as pd
from requests import HTTPError, RequestException

from bitfount.config import BITFOUNT_DEFAULT_BATCHED_EXECUTION, BITFOUNT_STORAGE_PATH
from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
    MultiTableSource,
)
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.views import SQLViewConfig, ViewDatasourceConfig
from bitfount.data.exceptions import DataSourceError
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import _ForceStypeValue, _SemanticTypeValue
from bitfount.federated.aggregators.secure import _is_secure_share_task_request
from bitfount.federated.authorisation_checkers import (
    _IDENTITY_VERIFICATION_METHODS_MAP,
    IdentityVerificationMethod,
    _AuthorisationChecker,
    _OIDCAuthorisationCode,
    _OIDCDeviceCode,
    _SAMLAuthorisation,
    _SignatureBasedAuthorisation,
    check_identity_verification_method,
)
from bitfount.federated.exceptions import (
    BitfountTaskStartError,
    PodNameError,
    PodRegistrationError,
    PodViewDatabaseError,
    PodViewError,
)
from bitfount.federated.helper import (
    POD_NAME_REGEX,
    _check_and_update_pod_ids,
    _create_and_connect_pod_mailbox,
)
from bitfount.federated.keys_setup import RSAKeyPair, _get_pod_keys
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.monitoring import task_monitor_context
from bitfount.federated.pod_db_utils import (
    _add_data_to_pod_db,
    _add_file_iterable_datasource_to_db,
)
from bitfount.federated.pod_response_message import _PodResponseMessage
from bitfount.federated.pod_vitals import _PodVitals, _PodVitalsHandler
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.task_requests import (
    _SignedEncryptedTaskRequest,
    _TaskRequestMessage,
)
from bitfount.federated.transport.base_transport import _run_func_and_listen_to_mailbox
from bitfount.federated.transport.config import MessageServiceConfig
from bitfount.federated.transport.message_service import (
    _BitfountMessage,
    _BitfountMessageType,
)
from bitfount.federated.transport.pod_transport import _PodMailbox
from bitfount.federated.transport.worker_transport import (
    _InterPodWorkerMailbox,
    _WorkerMailbox,
)
from bitfount.federated.types import (
    AggregatorType,
    SerializedAlgorithm,
    SerializedProtocol,
    _PodResponseType,
)
from bitfount.federated.worker import _Worker
from bitfount.hooks import HookType, get_hooks, on_pod_init_error, on_pod_startup_error
from bitfount.hub.api import BitfountAM, BitfountHub, PodPublicMetadata
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.authentication_handlers import _DEFAULT_USERNAME
from bitfount.hub.exceptions import SchemaUploadError
from bitfount.hub.helper import (
    _create_access_manager,
    _create_bitfounthub,
    _get_pod_public_keys,
)
from bitfount.runners.config_schemas import (
    JWT,
    APIKeys,
    PodDataConfig,
    PodDetailsConfig,
)
from bitfount.transformations.dataset_operations import (
    CleanDataTransformation,
    NormalizeDataTransformation,
)
from bitfount.transformations.processor import TransformationProcessor
from bitfount.utils import _handle_fatal_error, is_notebook

logger = _get_federated_logger(__name__)


class _StoppableThead(threading.Thread):
    """Stoppable thread by using a stop `threading.Event`.

    Args:
        stop_event: This is a `threading.Event` which when set, should stop the thread.
            The function that is being executed in the thread is required to regularly
            check the status of this event.
        **kwargs: Keyword arguments passed to parent constructor.
    """

    def __init__(self, stop_event: threading.Event, **kwargs: Any):
        self._stop_event = stop_event
        super().__init__(**kwargs)

    @property
    def stopped(self) -> bool:
        """Returns whether or not the stop event has been set."""
        return self._stop_event.is_set()

    def stop(self) -> None:
        """Sets the stop event."""
        self._stop_event.set()


@dataclass
class DatasourceContainerConfig:
    """Contains a datasource and maybe some data related to it.

    This represents a datasource configuration _pre_-data-loading/configuration and
    so the data config and schema are not required.
    """

    name: str
    datasource_details: PodDetailsConfig
    datasource: Union[BaseSource, ViewDatasourceConfig]
    data_config: Optional[PodDataConfig] = None
    schema: Optional[Union[str, os.PathLike, BitfountSchema]] = None


@dataclass
class DatasourceContainer:
    """Contains a datasource and all the data related to it.

    This represents a datasource configuration _post_-data-loading/configuration and
    so the data config and schema must be present.
    """

    name: str
    datasource_details: PodDetailsConfig
    datasource: Union[BaseSource, ViewDatasourceConfig]
    data_config: PodDataConfig
    schema: BitfountSchema


class Pod:
    """Makes data and computation available remotely and responds to tasks.

    The basic component of the Bitfount network is the `Pod` (Processor of Data). Pods
    are co-located with data, check users are authorized to do given operations on the
    data and then do any approved computation. Creating a `Pod` will register the pod
    with Bitfount Hub.

    ```python title="Example usage:"
    import bitfount as bf

    pod = bf.Pod(
        name="really_cool_data",
        data="/path/to/data",
    )
    pod.start()
    ```

    :::tip

    Once you start a `Pod`, you can just leave it running in the background. It will
    automatically respond to any tasks without any intervention required.

    :::

    Args:
        name: Name of the pod. This will appear on `Bitfount Hub` and `Bitfount AM`.
            This is also used for the name of the table in a single-table `BaseSource`.
        datasource: (Deprecated, use `datasources` instead) A concrete instance
            of the `BaseSource` object.
        datasources: The list of datasources to be associated and registered with
            this pod. Each will have their own data config and schema (although
            not necessarily present at this point).
        username: Username of the user who is registering the pod. Defaults to None.
        data_config: (Deprecated, use `datasources` instead) Configuration for the
            data. Defaults to None.
        schema: (Deprecated, use `datasources` instead) Schema for the data. This
            can be a `BitfountSchema` object or a Path to a serialized
            `BitfountSchema`. This will be generated automatically if not provided.
            Defaults to None.
        pod_details_config: (Deprecated, use `datasources` instead) Configuration for
            the pod details. Defaults to None.
        hub: Bitfount Hub to register the pod with. Defaults to None.
        message_service: Configuration for the message service. Defaults to None.
        access_manager: Access manager to use for checking access. Defaults to None.
        pod_keys: Keys for the pod. Defaults to None.
        approved_pods: List of other pod identifiers this pod is happy
            to share a training task with. Required if the protocol uses the
            `SecureAggregator` aggregator.
        differential_privacy: Differential privacy configuration for the pod.
            Defaults to None.
        pod_db: Whether the results should be stored in a database. Defaults to False.
            If argument is set to True, then a SQLite database will be created for the
            pod in order to enable results storage for protocols that return them.
            It also keeps track of the pod datapoints so any repeat task is ran
            only on new datapoints.
        show_datapoints_with_results_in_db: Whether the original datapoints should be
            included in the results database. Defaults to True. This argument is ignored
            if pod_db argument is set to False.
        update_schema: Whether the schema needs to be re-generated even if provided.
            Defaults to False.
        secrets: Secrets for authenticating with Bitfount services.
            If not provided then an interactive flow will trigger for authentication.

    Attributes:
        datasources: The set of datasources associated with this pod.
        name: Name of the pod.
        pod_identifier: Identifier of the pod.
        private_key: Private key of the pod.

    Raises:
        PodRegistrationError: If the pod could not be registered for any reason.
        DataSourceError: If the `BaseSource` for the provided datasource has
            not been initialised properly. This can be done by calling
            `super().__init__(**kwargs)` in the `__init__` of the DataSource.
    """

    @on_pod_init_error
    def __init__(
        self,
        name: str,
        datasource: Optional[BaseSource] = None,
        datasources: Optional[Iterable[DatasourceContainerConfig]] = None,
        username: Optional[str] = None,
        data_config: Optional[PodDataConfig] = None,
        schema: Optional[Union[str, os.PathLike, BitfountSchema]] = None,
        pod_details_config: Optional[PodDetailsConfig] = None,
        hub: Optional[BitfountHub] = None,
        message_service: Optional[MessageServiceConfig] = None,
        access_manager: Optional[BitfountAM] = None,
        pod_keys: Optional[RSAKeyPair] = None,
        approved_pods: Optional[List[str]] = None,
        differential_privacy: Optional[DPPodConfig] = None,
        pod_db: bool = False,
        show_datapoints_with_results_in_db: bool = True,
        update_schema: bool = False,
        secrets: Optional[Union[APIKeys, JWT]] = None,
    ):
        for hook in get_hooks(HookType.POD):
            hook.on_pod_init_start(self, pod_name=name, username=username)

        self.name = name

        self._pod_details_config = (
            pod_details_config
            if pod_details_config is not None
            else self._get_default_pod_details_config()
        )
        self.pod_db = pod_db

        datasources_: List[DatasourceContainerConfig] = self._process_datasource_args(
            datasources=datasources,
            datasource=datasource,
            pod_name=name,
            datasource_details=self._pod_details_config,
            data_config=data_config,
            schema=schema,
        )

        # Check for the presence of any uninitialised datasources
        maybe_uninitialised_datasource = next(
            (
                dsc
                for dsc in datasources_
                if isinstance(dsc.datasource, BaseSource)
                and not dsc.datasource.is_initialised
            ),
            None,
        )
        if maybe_uninitialised_datasource is not None:
            raise DataSourceError(
                f"The {maybe_uninitialised_datasource} datasource provided has not "
                "initialised the BaseSource parent class. Please make sure "
                "that you call `super().__init__(**kwargs)` in your child method."
            )

        # Load schemas if necessary and save ready to use datasources
        self.base_datasources: Dict[str, DatasourceContainer] = {
            ds.name: self._load_basesource_schema_if_necessary(ds, update_schema)
            for ds in datasources_
            if isinstance(ds.datasource, BaseSource)
        }
        # Setup Pod DB
        # Check if any of the datasources are database-related,
        # as cannot use these with pod_db
        if any(
            isinstance(dsc.datasource, DatabaseSource)
            for dsc in self.base_datasources.values()
        ):
            self.pod_db = False
            logger.warning(
                "Pod database not supported for DatabaseSource. "
                "Starting pod without database."
            )
        else:
            self.pod_db = pod_db
        if self.pod_db:
            for ds in self.base_datasources.values():
                # self.base_datasources has only base sources, so it's safe to cast
                self._update_pod_db(ds.name, cast(BaseSource, ds.datasource))

        self.view_datasources: Dict[str, DatasourceContainer] = {
            ds.name: self._load_view_schema_if_necessary(ds, update_schema)
            for ds in datasources_
            if isinstance(ds.datasource, ViewDatasourceConfig)
        }
        self.datasources: Dict[str, DatasourceContainer] = {
            **self.base_datasources,
            **self.view_datasources,
        }

        self.show_datapoints_with_results_in_db = (
            show_datapoints_with_results_in_db if self.pod_db else False
        )

        # Establish Bitfount Hub and access manager connection details
        self._hub = (
            hub
            if hub is not None
            else _create_bitfounthub(username=username, secrets=secrets)
        )
        self._session = self._hub.session
        self._access_manager = (
            access_manager
            if access_manager is not None
            else _create_access_manager(self._session)
        )
        self._access_manager_public_key = self._access_manager.get_access_manager_key()

        # Get RSA keys for pod
        self.private_key, self.pod_public_key = self._get_default_pod_keys(pod_keys)

        # Establish identifiers for pod and datasets
        # and ensure these are added to the auto-approved "pods" list
        self.pod_identifier = f"{self._session.username}/{self.name}"  # TODO: [NO_TICKET: Temporary] maybe need to get rid of this, at least inside Workers? # noqa: B950
        dataset_identifiers = [
            f"{self._session.username}/{ds_name}" for ds_name in self.datasources.keys()
        ]
        if approved_pods is None:
            approved_pods = []
        approved_pods = _check_and_update_pod_ids(
            [*approved_pods, *dataset_identifiers], self._hub
        )
        self.approved_pods = approved_pods

        self._pod_dp = differential_privacy
        self._pod_vitals = _PodVitals()
        # Connecting the pod to the message service must happen AFTER registering
        # it on the hub as the message service uses hub information to verify that
        # the relevant message queue is available.
        try:
            # For now we register the datasources as logical pods
            for ds in self.datasources.values():
                public_metadata = self._get_public_metadata(
                    ds.name, ds.datasource_details, ds.schema
                )
                self._register_pod(public_metadata)
        except PodRegistrationError as pre:
            _handle_fatal_error(pre, logger=logger)

        self._ms_config: Optional[MessageServiceConfig] = message_service
        self._mailbox: Optional[_PodMailbox] = None

        # Marker for when initialization is complete
        self._initialised: bool = False

        for hook in get_hooks(HookType.POD):
            hook.on_pod_init_end(self)

    @property
    def name(self) -> str:
        """Pod name property."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Validate Pod's name matches POD_NAME_REGEX."""
        if _name := POD_NAME_REGEX.fullmatch(name):
            self._name = _name.string
        else:
            raise PodNameError(
                f"Invalid Pod name: {name}. "
                f"Pod names must match: {POD_NAME_REGEX.pattern}"
            )

    @property
    def datasource(self) -> Optional[DatasourceContainer]:
        """If there is only a single datasource, this is a shorthand for retrieving it.

        If there is more than one datasource (or no datasources) this will log a
        warning and return None.
        """
        if (num_datasources := len(self.datasources)) > 1:
            logger.warning(
                f"Pod has {num_datasources} datasources;"
                f" unable to extract with Pod.datasource property."
            )
            return None
        elif num_datasources < 1:
            logger.warning(
                "Pod has no datasources configured;"
                " unable to extract with Pod.datasource property."
            )
            return None

        # Otherwise we have exactly one datasource
        return list(self.datasources.values())[0]

    def _load_basesource_schema_if_necessary(
        self, ds: DatasourceContainerConfig, update_schema: bool = False
    ) -> DatasourceContainer:
        """Load schema for base datasources."""
        ds.datasource = cast(BaseSource, ds.datasource)
        # Extract or generate data config
        if ds.data_config:
            data_config = ds.data_config
        else:
            data_config = PodDataConfig()
        # Load existing schemas if needed
        schema: Optional[BitfountSchema] = None
        if ds.schema:
            if isinstance(ds.schema, BitfountSchema):
                schema = ds.schema
            else:
                schema = BitfountSchema.load_from_file(ds.schema)
        # Validate database connection if exists
        if isinstance(ds.datasource, DatabaseSource):
            ds.datasource.validate()

        # Check if we need to update the provided schema. This may be needed if:
        #   - the datasource is multi-table and references tables not in the schema
        #   - auto-tidy is requested
        #   - the datasource name is not the name of a table in the schema
        if ds.datasource.multi_table and schema is not None:
            # check if all table names are in the schema
            schema_tables = [table.name for table in schema.tables]
            if any(table not in schema_tables for table in ds.datasource.table_names):  # type: ignore[attr-defined] # reason: see below: # noqa: B950
                # mypy ignore - we only check the table names
                # for multi-table the datasources
                logger.info(
                    "Datasource has additional tables to the "
                    "schema provided, re-generating schema."
                )
                update_schema = True
        elif data_config.auto_tidy is True and schema is not None:
            # Auto-tidy is not applied to multi-table datasources,
            # so we only cover the single table case.
            logger.info("Auto-tidying the datasource, schema will be re-generated.")
            update_schema = True
        elif schema is not None and ds.name not in [
            table.name for table in schema.tables
        ]:
            logger.warning(
                "Provided schema table name does not match to datasource name,"
                " you may need to regenerate the schema."
            )
        # Create the schema if it doesn't already exist or an update has
        # been requested
        if update_schema is True or schema is None:
            schema = self._setup_schema(
                datasource_name=ds.name,
                datasource=ds.datasource,
                schema=schema,
                data_config=data_config,
            )
        else:
            logger.info(f"Using user provided schema for datasource {ds.name}.")

        return DatasourceContainer(
            name=ds.name,
            datasource_details=ds.datasource_details,
            datasource=ds.datasource,
            data_config=data_config,
            schema=schema,
        )

    def _load_view_schema_if_necessary(
        self, ds: DatasourceContainerConfig, update_schema: bool = False
    ) -> DatasourceContainer:
        """Load schema for view datasources."""
        # isinstance check before function so safe to cast
        ds.datasource = cast(ViewDatasourceConfig, ds.datasource)
        # Extract or generate data config
        if ds.data_config:
            data_config = ds.data_config
        else:
            data_config = PodDataConfig()

        # Load existing schemas if needed
        schema: Optional[BitfountSchema] = None
        if ds.schema is not None:
            if isinstance(ds.schema, BitfountSchema):
                schema = ds.schema
            else:
                schema = BitfountSchema.load_from_file(ds.schema)

        force_stypes: Optional[
            MutableMapping[Union[_ForceStypeValue, _SemanticTypeValue], List[str]]
        ]
        # Create the schema if it doesn't already exist or an update has
        # been requested
        if update_schema is True or schema is None:
            source_dataset = self.base_datasources[ds.datasource.source_dataset_name]
            if ds.data_config is None or ds.data_config.force_stypes is None:
                # Take the force_stypes from the source dataset
                if (
                    source_dataset.data_config.force_stypes is not None
                    and source_dataset.name
                    in source_dataset.data_config.force_stypes.keys()
                ):
                    force_stypes = source_dataset.data_config.force_stypes[
                        source_dataset.name
                    ]
                else:
                    force_stypes = None
            else:
                # take the force_stypes defined in the view data config
                force_stypes = ds.data_config.force_stypes[ds.name]
            # Generate the schema for the views
            ds.schema = ds.datasource.generate_schema(
                name=ds.name,
                underlying_datasource=source_dataset.datasource,
                force_stypes=force_stypes,
            )
        # schema is set by this point so it's safe to cast
        return DatasourceContainer(
            name=ds.name,
            datasource_details=ds.datasource_details,
            datasource=ds.datasource,
            data_config=data_config,
            schema=cast(BitfountSchema, ds.schema),
        )

    @staticmethod
    def _setup_schema(
        datasource_name: str,
        datasource: BaseSource,
        data_config: PodDataConfig,
        schema: Optional[BitfountSchema] = None,
    ) -> BitfountSchema:
        """Generate pod schema."""
        datasource.load_data()
        logger.info("Generating the schema...")
        # Create schema if not provided
        if not schema:
            schema = BitfountSchema()

        # Add BaseSource to schema
        schema.add_datasource_tables(
            datasource=datasource,
            table_name=datasource_name,
            ignore_cols=data_config.ignore_cols,
            force_stypes=data_config.force_stypes,
        )

        if data_config.auto_tidy and datasource.multi_table:
            logger.warning("Can't autotidy multi-table data.")
        elif data_config.auto_tidy:
            clean_data = CleanDataTransformation()
            # Normalization is applied to all float columns if `auto-tidy` is true
            normalize = NormalizeDataTransformation()
            processor = TransformationProcessor(
                [clean_data, normalize],
                schema.get_table_schema(datasource_name),
            )
            datasource.data = processor.transform(datasource.data)

            # Add BaseSource to schema again because features will have changed by
            # auto-tidying
            schema.add_datasource_tables(
                datasource=datasource,
                table_name=datasource_name,
                ignore_cols=data_config.ignore_cols,
                force_stypes=data_config.force_stypes,
            )

        # Freeze schema
        schema.freeze()
        return schema

    def _update_pod_db(self, datasource_name: str, datasource: BaseSource) -> None:
        """Creates and updates the pod database.

        This is a static database on the pod with the datapoint hashes so we only
        compute them once. For each datapoint row in the datasource, a hash value
        is computed. Then the data from (each table of) the datasource,
        together with the hash value, are written to the database.


        :::caution

        Does not work for multi-table `DatabaseSource`s as we cannot load the data into
        memory.

        :::
        """
        # To avoid name clashes with tables of the same name in other datasources
        # we need to modify the table names in multi-table to add the datasource name.
        if datasource.multi_table:
            datasource = cast(MultiTableSource, datasource)
            for table in datasource.table_names:
                # if table name is given as an arg to get_data
                # then it will always return a df, so we can cast
                new_data = cast(
                    pd.DataFrame, datasource.get_data(table_name=table)
                ).copy()
                _add_data_to_pod_db(
                    pod_name=self.name,
                    data=new_data,
                    table_name=f"{datasource_name}_{table}",
                )
        # If the datasource is a FileSystemIterableSource,
        elif isinstance(datasource, FileSystemIterableSource):
            _add_file_iterable_datasource_to_db(
                pod_name=self.name,
                datasource=datasource,
                table_name=datasource_name,
            )
        # If there's only one table in the datasource we can just use the datasource
        # name directly.
        else:
            # This works regardless of whether or not the datasource is iterable
            datasource.load_data()
            _add_data_to_pod_db(
                pod_name=self.name,
                data=datasource.data.copy(),
                table_name=datasource_name,
            )

    def _get_default_pod_details_config(self) -> PodDetailsConfig:
        """Get default pod details config."""
        return PodDetailsConfig(display_name=self.name, description=self.name)

    @staticmethod
    def _get_public_metadata(
        name: str, pod_details_config: PodDetailsConfig, schema: BitfountSchema
    ) -> PodPublicMetadata:
        """Get PodPublicMetadata."""
        return PodPublicMetadata(
            name,
            pod_details_config.display_name,
            pod_details_config.description,
            schema.to_json(),
        )

    def _get_default_pod_keys(
        self, pod_keys: Optional[RSAKeyPair]
    ) -> Tuple[RSAPrivateKey, RSAPublicKey]:
        """Get default pod keys."""
        if pod_keys is None:
            user_storage_path = BITFOUNT_STORAGE_PATH / _DEFAULT_USERNAME
            pod_directory = user_storage_path / "pods" / self.name
            pod_keys = _get_pod_keys(pod_directory)
        return pod_keys.private, pod_keys.public

    def _register_pod(self, public_metadata: PodPublicMetadata) -> None:
        """Register pod with Bitfount Hub.

        If Pod is already registered, will update pod details if anything has changed.

        Raises:
            PodRegistrationError: if registration fails for any reason
        """
        try:
            logger.info("Registering/Updating details on Bitfount Hub.")
            self._hub.register_pod(
                public_metadata,
                self.pod_public_key,
                self._access_manager_public_key,
            )
        except (HTTPError, SchemaUploadError) as ex:
            logger.critical(f"Failed to register with hub: {ex}")
            raise PodRegistrationError("Failed to register with hub") from ex
        except RequestException as ex:
            logger.critical(f"Could not connect to hub: {ex}")
            raise PodRegistrationError("Could not connect to hub") from ex

    async def _initialise(self) -> None:
        """Initialises the pod.

        Sets any attributes that could not be created at creation time.
        """
        if not self._initialised:
            # `Optional` as may be set to `None` further down
            dataset_names: Optional[List[str]] = list(self.datasources.keys())
            # If there's only one dataset with the same name as the pod
            # then we register it as a plain old pod
            if (
                dataset_names is not None  # to assuage mypy
                and len(dataset_names) == 1
                and dataset_names[0] == self.name
            ):
                dataset_names = None

            # Create mailbox(es). Cannot be done in __init__ due to async nature.
            self._mailbox = await _create_and_connect_pod_mailbox(
                pod_name=self.name,
                session=self._session,
                ms_config=self._ms_config,
                dataset_names=dataset_names,
            )

            # Set initialised state
            self._initialised = True
        else:
            logger.warning("Pod._initialise() called twice. This is not allowed.")

    def _secure_aggregation_other_workers_response(
        self, other_worker_names: MutableSequence[str]
    ) -> Optional[List[str]]:
        """Checks if secure aggregation can be performed with given other workers.

        Args:
            other_worker_names (List[str]): list of other worker names

        Returns:
            Optional[List[str]]:
                unapproved workers (if they exist in other_worker_names)
        """
        unapproved_pods = [
            worker for worker in other_worker_names if worker not in self.approved_pods
        ]
        logger.debug(
            f"Modeller requested aggregation"
            f" with non-approved pods: {unapproved_pods}"
        )

        if unapproved_pods:
            logger.info(
                "Modeller requested aggregation with"
                " pods that this pod has not approved."
            )
            return unapproved_pods

        logger.debug("All pods requested by modeller for aggregation are approved.")
        return None

    def _check_for_unapproved_pods(
        self,
        pods_involved_in_task: Iterable[str],
        serialized_protocol: SerializedProtocol,
    ) -> Optional[List[str]]:
        """Returns the pods that we're not happy to work with.

        If secure aggregation has been requested then this will
        identify any pods that we've not approved.

        In any other case it returns None, as there's no concern
        around security with other pods.

        Args:
            pods_involved_in_task: A list of other pods that have been contacted by
                the modeller for this task.
            serialized_protocol: The decrypted serialized protocol portion of the task
                request.

        Returns:
            Either a list of unapproved pods or `None` if all are approved or if secure
            aggregation not in use.
        """
        unapproved_workers = None

        # Create mutable version of pods_involved_in_task
        other_pods: List[str] = list(pods_involved_in_task)

        # We don't need to check if we're approved to work with our self.
        try:
            other_pods.remove(self.pod_identifier)
        except ValueError:  # if not in list to remove
            pass

        aggregator = serialized_protocol.get("aggregator")
        if (
            aggregator
            and aggregator["class_name"] == AggregatorType.SecureAggregator.value
        ):
            logger.info(
                "Secure aggregation is in use, checking responses from other pods."
            )
            unapproved_workers = self._secure_aggregation_other_workers_response(
                other_pods
            )

        return unapproved_workers

    async def _new_task_request_handler(self, message: _BitfountMessage) -> None:
        """Called on new task request being received from message service."""
        logger.info(f"Training task request received from '{message.sender}'")
        try:
            await self._create_and_run_worker(message)
        except asyncio.TimeoutError:
            logger.info("Ready for next task...")
            return

    async def _create_and_run_worker(self, message: _BitfountMessage) -> None:
        """Creates and runs a worker instance."""
        # `_initialise` is always called before this method, so we can assume
        # that the mailbox is initialised. Reassuring mypy that this is True.
        assert isinstance(self._mailbox, _PodMailbox)  # nosec assert_used

        # Unpack task details from received message
        logger.info("Unpacking task details from message...")
        task_id = message.task_id
        task_request_message: _TaskRequestMessage = _TaskRequestMessage.deserialize(
            message.body
        )
        try:
            if task_request_message.project_id is None:
                # if there is no project id we set pod_db to False
                # old versions of bitfount don't include the project id
                # in the task request message, so added check for missing attribute
                # TODO: [BIT-2725] future tasks will not mutate this back to true
                self.pod_db = False
        except AttributeError:
            # this check is to ensure backward compatibility for task request messages
            self.pod_db = False

        auth_type: IdentityVerificationMethod = check_identity_verification_method(
            task_request_message.auth_type
        )
        authoriser_cls = _IDENTITY_VERIFICATION_METHODS_MAP[auth_type]
        task_request = authoriser_cls.unpack_task_request(
            message.body, self.private_key
        )

        # This is the "pod identifier" for the logical pod representing the target
        # datasource, i.e. what the modeller will have addressed to hit this
        # datasource.
        # Will be of the form: "<pod_namespace/owner>/<datasource_name>"
        # If the requested datasource is `None` we default to assuming the
        # data_identifier is the same as the pod_identifier by passing `None`
        # through to the worker.
        if (datasource_name := self._extract_requested_datasource(message)) is not None:
            data_identifier = f"{self._session.username}/{datasource_name}"
            target_identifier = data_identifier
        else:
            data_identifier = None
            target_identifier = self.pod_identifier

        # If we are using secure aggregation we check for unapproved workers; if
        # we are not, `unapproved_workers` will be `None`.
        other_pods = [
            pod_id for pod_id in message.pod_mailbox_ids if pod_id != target_identifier
        ]
        unapproved_workers = self._check_for_unapproved_pods(
            other_pods, task_request.serialized_protocol
        )

        # If we are dealing with secure aggregation (and hence need inter-pod
        # communication) we create an appropriate mailbox as long as there are no
        # unapproved workers.
        # If there are, the task will be rejected, so we can just create a normal
        # mailbox (as don't need inter-pod communication to reject the task).
        # Similarly, if we're not using secure aggregation we just create a normal
        # mailbox as inter-pod communication won't be needed.
        worker_mailbox: _WorkerMailbox

        if _is_secure_share_task_request(task_request) and not unapproved_workers:
            logger.debug("Creating mailbox with inter-pod support.")

            other_pod_public_keys = _get_pod_public_keys(other_pods, self._hub)

            worker_mailbox = _InterPodWorkerMailbox(
                pod_public_keys=other_pod_public_keys,
                private_key=self.private_key,
                pod_identifier=target_identifier,
                modeller_mailbox_id=message.sender_mailbox_id,
                modeller_name=message.sender,
                aes_encryption_key=task_request.aes_key,
                message_service=self._mailbox.message_service,
                pod_mailbox_ids=message.pod_mailbox_ids,
                task_id=task_id,
            )
        else:
            logger.debug("Creating modeller<->worker-only mailbox.")
            worker_mailbox = _WorkerMailbox(
                pod_identifier=target_identifier,
                modeller_mailbox_id=message.sender_mailbox_id,
                modeller_name=message.sender,
                aes_encryption_key=task_request.aes_key,
                message_service=self._mailbox.message_service,
                pod_mailbox_ids=message.pod_mailbox_ids,
                task_id=task_id,
            )

        # TODO: [BIT-1045] Move the secure aggregation allowed check to the access
        #       manager once we support configuring or storing it there.
        if unapproved_workers:
            # There are pods we're explicitly not happy to work with (i.e. we're
            # using secure aggregation) we reject the task.
            logger.info(f"Task from '{message.sender}' rejected.")
            authorisation_errors = _PodResponseMessage(
                message.sender, target_identifier
            )
            authorisation_errors.add(
                _PodResponseType.NO_ACCESS,
                unapproved_workers,
            )
            await worker_mailbox.reject_task(authorisation_errors.messages)
            return

        logger.debug("Creating authorisation checker.")
        authorisation_checker = self._create_authorisation_checker(
            task_request_message=task_request_message,
            sender=message.sender,
            worker_mailbox=worker_mailbox,
        )

        logger.debug("Creating worker.")
        if not hasattr(task_request_message, "project_id"):
            task_request_message.project_id = None
        if not hasattr(task_request_message, "run_on_new_data_only"):
            task_request_message.run_on_new_data_only = False
        if not hasattr(task_request_message, "batched_execution"):
            task_request_message.batched_execution = BITFOUNT_DEFAULT_BATCHED_EXECUTION

        # Establish worker datasource and schema
        worker_datasource, worker_schema = self._get_target_datasource_schema(message)
        worker = _Worker(
            datasource=worker_datasource,
            schema=worker_schema,
            mailbox=worker_mailbox,
            bitfounthub=self._hub,
            authorisation=authorisation_checker,
            parent_pod_identifier=self.pod_identifier,
            data_identifier=data_identifier,
            serialized_protocol=task_request.serialized_protocol,
            pod_vitals=self._pod_vitals,
            pod_dp=self._pod_dp,
            pod_db=self.pod_db,
            show_datapoints_in_results_db=self.show_datapoints_with_results_in_db,
            project_id=task_request_message.project_id,
            run_on_new_data_only=task_request_message.run_on_new_data_only,
            batched_execution=task_request_message.batched_execution,
            multi_pod_task=bool(other_pods),
        )

        # If interacting with an older modeller version then task_id won't be supplied
        task_monitor_cm: ContextManager
        if worker_mailbox.task_id:
            task_monitor_cm = task_monitor_context(
                hub=self._hub,
                task_id=worker_mailbox.task_id,
                sender_id=worker_mailbox.mailbox_id,
            )
        else:
            task_monitor_cm = nullcontext()

        with task_monitor_cm:
            # Run pre-task hooks
            for hook in get_hooks(HookType.POD):
                hook.on_task_start(self)

            # Run the worker and the mailbox listening simultaneously
            try:
                await _run_func_and_listen_to_mailbox(worker.run(), worker_mailbox)
            except Exception as e:
                logger.federated_error(e)
                logger.exception(e)
                for hook in get_hooks(HookType.POD):
                    hook.on_task_error(
                        self,
                        e,
                        id=worker_mailbox.task_id or task_request_message.project_id,
                    )

                if worker_mailbox.task_id:
                    logger.error(
                        f"Exception whilst running task {worker_mailbox.task_id}."
                    )
                else:
                    logger.error("Exception whilst running task.")

            # Run post-task hooks
            for hook in get_hooks(HookType.POD):
                hook.on_task_end(self)

        logger.info("Ready for next task...")

    def _create_authorisation_checker(
        self,
        task_request_message: _TaskRequestMessage,
        sender: str,
        worker_mailbox: _WorkerMailbox,
    ) -> _AuthorisationChecker:
        """Create appropriate Authorisation Checker.

        Determines checker to create based on supplied auth_type.

        Args:
            task_request_message: The full task request message.
            sender: The sender (i.e. modeller) of the request.
            worker_mailbox: Worker mailbox for communication with modeller.

        Returns:
            An authorisation checker.
        """
        auth_type: IdentityVerificationMethod = check_identity_verification_method(
            task_request_message.auth_type
        )
        authorisation_checker_cls = _IDENTITY_VERIFICATION_METHODS_MAP[auth_type]

        task_request = authorisation_checker_cls.unpack_task_request(
            task_request_message, self.private_key
        )
        serialized_protocol = task_request.serialized_protocol
        # Remove schema to reduce latency when checking access with the Access Manager
        # since it is the largest task element.
        algorithm = serialized_protocol["algorithm"]
        if not isinstance(serialized_protocol["algorithm"], list):
            algorithm = [cast(SerializedAlgorithm, algorithm)]

        algorithm = cast(List[SerializedAlgorithm], algorithm)
        for algo in algorithm:
            try:
                algo["model"].pop("schema", None)
            except KeyError:
                pass

        pod_response_message = _PodResponseMessage(
            modeller_name=sender,
            pod_identifier=self.pod_identifier,
        )

        authorisation_checker: _AuthorisationChecker

        if auth_type == IdentityVerificationMethod.KEYS:
            # Public Key Signature authorisation
            packed_request: _SignedEncryptedTaskRequest = (
                authorisation_checker_cls.extract_from_task_request_message(
                    task_request_message
                )
            )

            authorisation_checker = _SignatureBasedAuthorisation(
                pod_response_message=pod_response_message,
                access_manager=self._access_manager,
                modeller_name=worker_mailbox.modeller_name,
                encrypted_task_request=packed_request.encrypted_request,
                signature=packed_request.signature,
                serialized_protocol=serialized_protocol,
            )
        elif auth_type == IdentityVerificationMethod.OIDC_ACF_PKCE:
            # OIDC Authorization Code Flow
            auth_env = _get_auth_environment()
            authorisation_checker = _OIDCAuthorisationCode(
                pod_response_message=pod_response_message,
                access_manager=self._access_manager,
                mailbox=worker_mailbox,
                serialized_protocol=serialized_protocol,
                _auth_domain=auth_env.auth_domain,
                _client_id=auth_env.client_id,
            )
        elif auth_type == IdentityVerificationMethod.OIDC_DEVICE_CODE:
            # OIDC Device Code flow
            auth_env = _get_auth_environment()
            authorisation_checker = _OIDCDeviceCode(
                pod_response_message=pod_response_message,
                access_manager=self._access_manager,
                mailbox=worker_mailbox,
                serialized_protocol=serialized_protocol,
                _auth_domain=auth_env.auth_domain,
                _client_id=auth_env.client_id,
            )
        else:
            # Default to SAML Authorisation
            authorisation_checker = _SAMLAuthorisation(
                pod_response_message=pod_response_message,
                access_manager=self._access_manager,
                mailbox=worker_mailbox,
                serialized_protocol=serialized_protocol,
            )
        return authorisation_checker

    def _get_target_datasource_schema(
        self, message: _BitfountMessage
    ) -> Tuple[BaseSource, BitfountSchema]:
        """Extract the datasource config associated with datasource requested."""
        # Retrieve requested datasource details
        requested_datasource = self._extract_requested_datasource(message)
        if requested_datasource is None:
            target_datasource_container = None
        else:
            target_datasource_container = self.datasources.get(requested_datasource)

        # Check it is one that exists
        if target_datasource_container is None:
            logger.error(
                "Failed to start task addressed to recipient_mailbox_id="
                f"'{requested_datasource}'"
            )
            raise BitfountTaskStartError(
                "Failed to start task addressed to recipient_mailbox_id="
                f"'{requested_datasource}'"
            )

        if isinstance(target_datasource_container.datasource, ViewDatasourceConfig):
            # If the target datasource is a view, build it using
            # the "origin or source" datasource
            try:
                base_datasource: Union[BaseSource, ViewDatasourceConfig]
                # We need to split this in multiple cases to account for
                # the different ways of specifying the source dataset in YAML vs API
                if (
                    hasattr(target_datasource_container.data_config, "datasource_args")
                    and "source_dataset"
                    in target_datasource_container.data_config.datasource_args
                ):  # The YAML way of specifying the source dataset
                    base_datasource = self.datasources[
                        target_datasource_container.data_config.datasource_args[
                            "source_dataset"
                        ]
                    ].datasource
                elif hasattr(
                    target_datasource_container.datasource, "source_dataset_name"
                ):
                    # The API way of specifying the source dataset
                    base_datasource = self.datasources[
                        target_datasource_container.datasource.source_dataset_name
                    ].datasource
                else:
                    raise PodViewError(
                        "Failed to find source_dataset for view datasource "
                        f"{target_datasource_container.name}"
                    )
            except KeyError as e:
                raise BitfountTaskStartError(
                    "Failed to find source_dataset for view datasource "
                    f"{target_datasource_container.name}"
                ) from e
            else:
                return (
                    target_datasource_container.datasource.build(base_datasource),
                    target_datasource_container.schema,
                )
        else:
            # Otherwise, if not a view, must be a datasource itself
            return (
                target_datasource_container.datasource,
                target_datasource_container.schema,
            )

    def _extract_requested_datasource(self, message: _BitfountMessage) -> Optional[str]:
        """Extract the requested datasource from task request message.

        Returns `None` if the requested datasource cannot be found,
        otherwise the datasource name.
        """
        # The recipient_mailbox_id (i.e. the "pod name") on the received message will
        # actually be the dataset name as the datasets are viewed as logical pods.
        recipient_mailbox_id = message.recipient_mailbox_id
        if recipient_mailbox_id in self.datasources:
            logger.info(f"Requested datasource was {recipient_mailbox_id}")
            return recipient_mailbox_id
        else:
            logger.warning(
                f"Requested datasource was {recipient_mailbox_id}"
                f" but could not find this in datasources"
            )
            return None

    @staticmethod
    async def _repeat(
        stop_event: threading.Event, interval: int, func: Callable[..., Coroutine]
    ) -> None:
        """Run coroutine func every interval seconds.

        If func has not finished before *interval*, will run again
        immediately when the previous iteration finished.

        Args:
            stop_event: threading.Event to stop the loop
            interval: run interval in seconds
            func: function to call which returns a coroutine to await
        """
        while not stop_event.is_set():
            # Don't need to worry about gather tasks cancellation as func() (in
            # this case _pod_heartbeat()) is short running, so if one of the tasks
            # raises an exception the other won't be left running long.
            await asyncio.gather(func(), asyncio.sleep(interval))

    async def _pod_heartbeat(self) -> None:
        """Makes a pod heartbeat to the hub."""
        for ds_name in self.datasources.keys():
            try:
                self._hub.do_pod_heartbeat(ds_name, self.pod_public_key)
            except HTTPError as ex:
                logger.warning(f"Failed to reach hub for status: {ex}")
            except RequestException as ex:
                logger.warning(f"Could not connect to hub for status: {ex}")

    def _run_pod_heartbeat_task(self, stop_event: threading.Event) -> None:
        """Makes 10-second interval pod heartbeats to the hub."""
        if is_notebook():
            # We need to create a new event loop here for jupyter
            # As it's run in a new thread and can't be patched by nest_asyncio
            asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.run(self._repeat(stop_event, 10, self._pod_heartbeat))

    def _get_pod_heartbeat_thread(self) -> _StoppableThead:
        """Returns pod heartbeat thread."""
        logger.info(f"Starting pod {self.name}...")
        thread_stop_event = threading.Event()
        pod_heartbeat = _StoppableThead(
            stop_event=thread_stop_event,
            target=self._run_pod_heartbeat_task,
            args=(thread_stop_event,),
            name="pod_heartbeat",
        )
        return pod_heartbeat

    def _pod_vitals_server(self, vitals_handler: _PodVitalsHandler) -> None:
        """Run _PodVitals webserver."""
        # The Pod Vitals webserver should run until the
        # pod itself it shut down. asyncio.run would handle
        # the event loop for us however it would also
        # shutdown the loop (and the webserver) on completion
        # so instead we directly interact with the
        # event loop here to ensure it is run_forever.
        pod_vitals_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(pod_vitals_loop)
        vitals_handler.start(pod_vitals_loop)
        pod_vitals_loop.run_forever()

    def _run_pod_vitals_server(self) -> Optional[_PodVitalsHandler]:
        """Create _PodVitalsHandelr and run _PodVitals webserver."""
        # Check that we have not initialized the Pod from a notebook
        if not is_notebook():
            # Setup pod vitals webserver
            vitals_handler = _PodVitalsHandler(
                self._pod_vitals,
                {ds_name: ds.schema for ds_name, ds in self.datasources.items()},
            )
            logger.debug("Starting Pod Vitals interface...")
            threading.Thread(
                daemon=True,
                target=self._pod_vitals_server,
                args=(vitals_handler,),
                name="pod_vitals_interface",
            ).start()
            return vitals_handler
        else:
            return None

    async def start_async(self) -> None:
        """Starts a pod instance, listening for tasks.

        Whenever a task is received, a worker is created to handle it. Runs continuously
        and asynchronously orchestrates training whenever a task arrives i.e. multiple
        tasks can run concurrently.
        """
        for hook in get_hooks(HookType.POD):
            hook.on_pod_startup_start(self)
        # Do post-init initialization work
        await self._initialise()

        # `_initialise` has just been called which sets the mailbox so we can assume
        # that the mailbox is initialised. Reassuring mypy that this is True.
        assert isinstance(self._mailbox, _PodMailbox)  # nosec assert_used

        # Placeholders for elements that need shutdown
        pod_heartbeat: Optional[_StoppableThead] = None
        vitals_handler: Optional[_PodVitalsHandler] = None

        try:
            # Setup heartbeat to hub
            pod_heartbeat = self._get_pod_heartbeat_thread()
            pod_heartbeat.start()

            # Start pod vitals webserver
            vitals_handler = self._run_pod_vitals_server()

            # Attach handler for new tasks
            self._mailbox.register_handler(
                _BitfountMessageType.JOB_REQUEST, self._new_task_request_handler
            )

            for hook in get_hooks(HookType.POD):
                hook.on_pod_startup_end(self)

            # Start pod listening for messages
            logger.info("Pod started... press Ctrl+C to stop")

            # Mark as ready in the pod vitals, even if we're not using the handler
            self._pod_vitals.mark_pod_ready()

            await self._mailbox.listen_indefinitely()
        finally:
            for hook in get_hooks(HookType.POD):
                hook.on_pod_shutdown_start(self)

            logger.info(f"Pod {self.name} stopped.")

            # Shutdown pod heartbeat thread
            if pod_heartbeat:
                pod_heartbeat.stop()
                logger.debug(
                    "Waiting up to 15 seconds for pod heartbeat thread to stop"
                )
                pod_heartbeat.join(15)
                if pod_heartbeat.stopped:
                    logger.debug("Shut down pod heartbeat thread")
                else:
                    logger.error("Unable to shut down pod heartbeat thread")

            # Shutdown pod vitals webserver
            if vitals_handler:
                await vitals_handler.runner.cleanup()
                logger.debug("Shut down vitals handler thread")

            for hook in get_hooks(HookType.POD):
                hook.on_pod_shutdown_end(self)

    @on_pod_startup_error
    def start(self) -> None:
        """Starts a pod instance, listening for tasks.

        Whenever a task is received, a worker is created to handle it. Runs continuously
        and asynchronously orchestrates training whenever a task arrives i.e. multiple
        tasks can run concurrently.
        """
        asyncio.run(self.start_async())

    def _process_datasource_args(
        self,
        *,
        # New-format datasources
        datasources: Optional[Iterable[DatasourceContainerConfig]] = None,
        # Old-format datasource
        datasource: Optional[BaseSource] = None,
        # Old-format datasource: needed
        pod_name: Optional[str] = None,
        datasource_details: Optional[PodDetailsConfig] = None,
        # Old-format datasource: truly optional
        data_config: Optional[PodDataConfig] = None,
        schema: Optional[Union[str, os.PathLike, BitfountSchema]] = None,
        update_schema: bool = False,
    ) -> List[DatasourceContainerConfig]:
        """Load supplied datasources into expected format.

        Handles deprecation and incompatible specifications.
        """
        # Can EITHER have `datasource` or `datasources`, not both
        if datasource and datasources:
            raise ValueError(
                "Only one of `datasource` and `datasources` can be specified."
            )

        # One of `datasource` and `datasources` MUST BE specified
        if not datasource and not datasources:
            raise ValueError("One of `datasource` and `datasources` must be specified.")

        # `data_config` and `schema` are ONLY compatible with `datasources`
        if (data_config or schema) and not datasource:
            raise ValueError(
                "If using `data_config` or `schema`, must supply `datasource`."
            )

        # Old-format datasource _needs_ the pod name and datasource details
        if datasource and not (pod_name and datasource_details):
            raise ValueError(
                "When supplying `datasource`,"
                " `pod_name` and `datasource_details` are required."
            )

        if datasources:
            # Establish subclasses of BaseSource. We to this here even though
            # the `self.base_datasources` is an arg for the class as it is
            # set later in the class init
            base_datasources = {
                ds.name: ds
                for ds in datasources
                if isinstance(ds.datasource, BaseSource)
            }
            # Process the datasources
            for ds in datasources:
                if isinstance(ds.datasource, BaseSource):
                    # We don't need to do anything for BaseSources
                    pass
                else:  # if it is a ViewDatasourceConfig
                    # Make sure the source dataset is present in the base_datasources
                    source_ds: Optional[str] = None
                    if (
                        hasattr(ds.datasource, "source_dataset_name")
                        and ds.datasource.source_dataset_name in base_datasources.keys()
                    ):
                        source_ds = ds.datasource.source_dataset_name
                    elif (
                        hasattr(ds.data_config, "datasource_args")
                        and "source_dataset_name" in ds.data_config.datasource_args  # type: ignore[union-attr] # Reason: hasattr check # noqa: B950
                        and ds.data_config.datasource_args["source_dataset_name"]  # type: ignore[union-attr] # Reason: hasattr check # noqa: B950
                        in base_datasources.keys()
                    ):
                        source_ds = ds.data_config.datasource_args["source_dataset_name"]  # type: ignore[union-attr] # Reason: hasattr check # noqa: B950
                    else:  # if the view has no source dataset configured
                        raise PodViewError(
                            "The view provided does not reference a source datasource "
                            "from which to generate the view. Please check and "
                            "try again."
                        )
                    # Make sure the source dataset is part of the base_datasources
                    if source_ds not in base_datasources.keys():
                        raise PodViewError(
                            "The view provided references a datasource not "
                            "available for this pod. Please check and try again."
                        )
                    # SQLViewConfig is only supported for pods that have pod_db enabled.
                    if isinstance(ds.datasource, SQLViewConfig):
                        if self.pod_db is False:
                            raise PodViewDatabaseError(
                                "SQLViews are only supported with pods that "
                                "have the pod database enabled."
                            )
                        else:
                            # Pass pod name to the SQLViewConfig
                            ds.datasource.initialize(self.name)
            return list(datasources)
        else:  # if datasource
            warnings.warn(
                "Single `datasource` specification will be replaced"
                " with `datasources` in future versions",
                DeprecationWarning,
                stacklevel=2,
            )

            # Logic above should capture the need for these to be not `None` if
            # using singular `datasource`, these are primarily to mass persuade
            # mypy that this is the case
            assert datasource is not None  # nosec assert_used
            assert pod_name is not None  # nosec assert_used
            assert datasource_details is not None  # nosec assert_used

            # Create wrapper DataSourceContainer object around direct datasource
            # Uses pod name as datasource name.
            return [
                DatasourceContainerConfig(
                    name=pod_name,
                    datasource_details=datasource_details,
                    datasource=datasource,
                    data_config=data_config,
                    schema=schema,
                )
            ]
