"""Contains courtesy classes and functions for making pod running easier."""
import importlib
import logging
import os
from os import PathLike
from pathlib import Path
from typing import Optional, Type, Union

import desert
from envyaml import EnvYAML

from bitfount.data import ViewDatasourceConfig
from bitfount.data.datasources.views import DataView
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.types import DatasourceType
from bitfount.federated.keys_setup import _get_pod_keys
from bitfount.federated.pod import BaseSource, DatasourceContainerConfig, Pod
from bitfount.hub.helper import _create_access_manager, _create_bitfounthub
from bitfount.runners.config_schemas import (
    DatasourceConfig,
    PodConfig,
    PodDetailsConfig,
)

logger = logging.getLogger(__name__)


def setup_pod_from_config_file(path_to_config_yaml: Union[str, PathLike]) -> Pod:
    """Creates a pod from a YAML config file.

    Args:
        path_to_config_yaml: The path to the config file.

    Returns:
        The created pod.
    """
    path_to_config_yaml = Path(path_to_config_yaml)
    logger.debug(f"Loading pod config from: {path_to_config_yaml}")

    # This double-underscore staticmethod access is not desirable but the additional
    # functionality in the class __init__ produces undesirable other inclusions.
    # This method allows us to just utilise the parsing aspect whilst performing
    # the envvar replacement.
    # TODO: [BIT-2202] Revisit double-underscore method usage.
    config_yaml = EnvYAML._EnvYAML__read_yaml_file(  # type: ignore[attr-defined] # Reason: see comment # noqa: B950
        path_to_config_yaml, os.environ, strict=True
    )

    pod_config_schema = desert.schema(PodConfig)
    pod_config_schema.context["config_path"] = path_to_config_yaml

    config = pod_config_schema.load(config_yaml)
    return setup_pod_from_config(config)


def setup_pod_from_config(config: PodConfig) -> Pod:
    """Creates a pod from a loaded config.

    Args:
        config: The configuration as a PodConfig instance.

    Returns:
        The created pod.
    """
    bitfount_hub = _create_bitfounthub(config.username, config.hub.url, config.secrets)
    access_manager = _create_access_manager(
        bitfount_hub.session, config.access_manager.url
    )

    # Load Pod Keys
    pod_directory = bitfount_hub.user_storage_path / "pods" / config.name
    pod_keys = _get_pod_keys(pod_directory)

    if config.datasource is not None and config.data_config is not None:
        # This handles the old-style datasource format where datasource and
        # data_config are top-level arguments in the schema. In this case there
        # is only a single datasource in the pod and so we can use the
        # pod name/details.
        datasources = [
            setup_datasource(
                DatasourceConfig(
                    datasource=config.datasource,
                    data_config=config.data_config,
                    # Dataset has the same name as the pod for the old config case
                    name=config.name,
                    # datasource_details_config also has the same details
                    datasource_details_config=config.pod_details_config,
                    schema=config.schema,
                ),
                fallback_name=config.name,
                fallback_details=config.pod_details_config,
            )
        ]
    elif config.datasources is not None and len(config.datasources) == 1:
        # This handles the new-style datasource format (with `datasources` as the
        # top-level argument in the schema) but where there is still only a single
        # datasource and so we can fallback to the pod name/details if specifics
        # are not provided.
        datasources = [
            setup_datasource(
                ds,
                fallback_name=config.name,
                fallback_details=config.pod_details_config,
            )
            for ds in config.datasources
        ]
    elif config.datasources is not None:
        # This handles the new-style datasources format with multiple datasources.
        # There is no fallback functionality for this, the datasource configs must
        # provide names/details.
        datasources = [setup_datasource(ds) for ds in config.datasources]
    else:
        raise ValueError("No valid datasource config found")

    return Pod(
        name=config.name,
        datasources=datasources,
        pod_details_config=config.pod_details_config,
        hub=bitfount_hub,
        message_service=config.message_service,
        access_manager=access_manager,
        pod_keys=pod_keys,
        approved_pods=config.approved_pods,
        differential_privacy=config.differential_privacy,
        update_schema=config.update_schema,
        pod_db=config.pod_db,
    )


def setup_datasource(
    datasource_config: DatasourceConfig,
    fallback_name: Optional[str] = None,
    fallback_details: Optional[PodDetailsConfig] = None,
) -> DatasourceContainerConfig:
    """Creates a BaseSource from a DatasourceConfig.

    Args:
        datasource_config: The configuration as a DatasourceConfig instance.
        fallback_name: The name to use for the datasource if one is not explicitly
            provided.
        fallback_details: The details to use for the datasource if one is not
            explicitly provided.

    Returns:
        The created DatasourceContainerConfig.
    """
    # Ensure we have imported the desired datasource class
    try:
        # First we see if it is a built-in algorithm class
        datasource_name = DatasourceType(datasource_config.datasource).name
    except ValueError:
        # If datasource_name is not in DatasourceType then we see if it is a plugin
        datasource_name = datasource_config.datasource
        logger.debug(
            f"Could not find {datasource_config.datasource} in built-in datasource "
            "classes. Trying to load as plugin..."
        )
    try:
        datasource_cls: Union[Type[BaseSource], Type[ViewDatasourceConfig]] = getattr(
            importlib.import_module("bitfount.data"), datasource_name
        )
    except AttributeError as e:
        raise ImportError(
            f"Unable to import {datasource_config.datasource} from bitfount."
        ) from e
    # Check we're not trying to load a data view directly rather than from config
    if issubclass(datasource_cls, DataView):
        raise TypeError(
            f"{datasource_cls.__name__} is a data view and should not be"
            f" instantiated directly. Instead, specify the corresponding view"
            f" configuration class."
        )

    # Create datasource instance
    datasource: Union[BaseSource, ViewDatasourceConfig]
    if issubclass(datasource_cls, ViewDatasourceConfig):
        logger.debug(
            f"Loading view-based datasource config for {datasource_cls.__name__}"
        )
        datasource = _setup_view_datasource(datasource_cls, datasource_config)
    else:
        logger.debug(f"Loading datasource config for {datasource_cls.__name__}")
        datasource = _setup_direct_datasource(datasource_cls, datasource_config)

    # Establish datasource name (using fallback name if needed)
    name = datasource_config.name
    if name is None:
        if fallback_name is not None:
            name = fallback_name
        else:
            raise ValueError(
                f"The configured datasource {datasource_config.datasource} doesn't"
                f" have a name defined and cannot adopt the pod's name"
            )

    # Establish datasource details (using fallback details if needed)
    details = datasource_config.datasource_details_config
    if details is None:
        if fallback_details is not None:
            details = fallback_details
        else:
            raise ValueError(
                f"The configured datasource {datasource_config.datasource}"
                f" doesn't have details defined and cannot adopt the pod's details"
            )

    # Wrap the datasource in a container config instance
    return DatasourceContainerConfig(
        name=name,
        datasource_details=details,
        datasource=datasource,
        data_config=datasource_config.data_config,
        schema=datasource_config.schema,
    )


def _setup_view_datasource(
    datasource_cls: Type[ViewDatasourceConfig], datasource_config: DatasourceConfig
) -> ViewDatasourceConfig:
    view = datasource_cls(**datasource_config.data_config.datasource_args)
    return view


def _setup_direct_datasource(
    datasource_cls: Type[BaseSource], datasource_config: DatasourceConfig
) -> BaseSource:
    # Get data split info
    data_split_config = datasource_config.data_config.data_split
    data_splitter = DatasetSplitter.create(
        data_split_config.data_splitter, **data_split_config.args
    )

    # Create datasource instance
    datasource = datasource_cls(
        data_splitter=data_splitter, **datasource_config.data_config.datasource_args
    )

    # Check that the instance has correctly instantiated BaseSource
    if not datasource.is_initialised:
        raise ValueError(
            f"The configured datasource {datasource_config.datasource}"
            f" does not extend BaseSource"
        )

    return datasource
