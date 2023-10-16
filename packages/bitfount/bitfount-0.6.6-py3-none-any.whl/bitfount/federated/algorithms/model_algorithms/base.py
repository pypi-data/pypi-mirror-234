"""Base classes for all model-based algorithms.

Attributes:
    registry: A read-only dictionary of model algorithm factory names to their
        implementation classes.
"""
from __future__ import annotations

from abc import ABC
import inspect
import os
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Generic,
    Mapping,
    Optional,
    Type,
    Union,
    cast,
)

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
    _BaseAlgorithm,
)
from bitfount.federated.helper import TaskContext
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.models.base_models import MAIN_MODEL_REGISTRY
from bitfount.schemas.utils import bf_dump
from bitfount.types import (
    T_DTYPE,
    T_FIELDS_DICT,
    T_NESTED_FIELDS,
    DistributedModelProtocol,
    _BaseSerializableObjectMixIn,
    _SerializedWeights,
    _StrAnyDict,
)

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub
    from bitfount.types import _DistributedModelTypeOrReference


logger = _get_federated_logger(__name__)


class _BaseModelAlgorithm(Generic[T_DTYPE], _BaseAlgorithm, ABC):
    """Blueprint for either the modeller side or the worker side of ModelAlgorithm."""

    def __init__(
        self,
        *,
        model: DistributedModelProtocol[T_DTYPE],
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model = model
        self.pretrained_file = pretrained_file

    @property
    def tensor_precision(self) -> T_DTYPE:
        """Returns model tensor precision."""
        return cast(T_DTYPE, self.model.tensor_precision())


class _BaseModellerModelAlgorithm(_BaseModelAlgorithm, BaseModellerAlgorithm, ABC):
    """Modeller side of the algorithm."""

    def __init__(
        self,
        *,
        model: DistributedModelProtocol,
        modeller_checkpointing: bool = True,
        checkpoint_filename: Optional[str] = None,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, pretrained_file=pretrained_file, **kwargs)
        self.modeller_checkpointing = modeller_checkpointing
        self.checkpoint_filename = checkpoint_filename

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the algorithm as required."""
        if not self.model.initialised:
            self.model.initialise_model(context=TaskContext.MODELLER)
        if not self.checkpoint_filename:
            self.checkpoint_filename = task_id
        # This needs to occur AFTER model initialization so the model is correctly
        # created. deserialize() may cause initialization but we can not rely on it
        # in this instance because we need to pass in context information.
        # This should be reviewed as part of [BIT-536].
        if self.pretrained_file is not None:
            logger.info(f"Deserializing model from {self.pretrained_file}.")
            self.model.deserialize(self.pretrained_file, **kwargs)


class _BaseWorkerModelAlgorithm(_BaseModelAlgorithm, BaseWorkerAlgorithm, ABC):
    """Worker side of the algorithm."""

    def __init__(self, *, model: DistributedModelProtocol, **kwargs: Any):
        super().__init__(model=model, **kwargs)

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the algorithm as required."""
        # Apply pod DP settings if needed. Needs to occur before model
        # initialization so the right DP settings are applied during initialization.
        self._apply_pod_dp(pod_dp)
        self.initialise_data(datasource=datasource)

    def initialise_data(self, datasource: BaseSource) -> None:
        """Initialises the data for the algorithm.

        Args:
            datasource: The datasource to initialise the data from.
        """
        self.datasource = datasource
        self.model.initialise_model(data=self.datasource, context=TaskContext.WORKER)

    def update_params(self, params: _SerializedWeights) -> None:
        """Updates model parameters."""
        model_params = self.model.deserialize_params(params)
        self.model.update_params(model_params)

    def _apply_pod_dp(self, pod_dp: Optional[DPPodConfig]) -> None:
        """Applies pod-level Differential Privacy constraints if supported.

        The model must inherit from `DifferentiallyPrivate` for DP to be supported.

        Args:
            pod_dp: The pod DP constraints to apply or None if no constraints.
        """
        try:
            # only applied if model supports DP so can ignore attr-defined
            self.model.apply_pod_dp(pod_dp)  # type: ignore[attr-defined]  # Reason: caught by try-except  # noqa: B950
        except AttributeError:
            pass


# The mutable underlying dict that holds the registry information
_registry: Dict[str, Type[_BaseModelAlgorithmFactory]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[str, Type[_BaseModelAlgorithmFactory]] = MappingProxyType(_registry)


class _BaseModelAlgorithmFactory(BaseAlgorithmFactory, ABC):
    """Base factory for algorithms involving an underlying model.

    Args:
        model: The model for the federated algorithm.
        pretrained_file: A file path or a string containing a
            pre-trained model. Defaults to None.

    Attributes:
        model: The model for the federated algorithm.
        pretrained_file: A file path or a string containing a
            pre-trained model. Defaults to None.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {}
    nested_fields: ClassVar[T_NESTED_FIELDS] = {"model": MAIN_MODEL_REGISTRY}

    def __init__(
        self,
        *,
        model: _DistributedModelTypeOrReference,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        project_id: Optional[str] = None,
        **kwargs: Any,
    ):
        # TODO: [NO_TICKET: Consideration only] Consider if project_id is required
        #       on the algorithm or if it should be something inherent on the
        #       model_reference (which is all it's currently used for).
        super().__init__(**kwargs)
        self.model = model
        self.pretrained_file = pretrained_file
        self.project_id = project_id

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            logger.debug(f"Adding {cls.__name__}: {cls} to Model Algorithm registry")
            _registry[cls.__name__] = cls

    @property
    def model_schema(self) -> _StrAnyDict:
        """Returns underlying model Schema."""
        # Assertion for mypy since DistributedModelProtocol is a protocol rather than
        # a concrete class.
        assert isinstance(self.model, _BaseSerializableObjectMixIn)  # nosec assert_used
        return bf_dump(self.model)

    def _get_model_from_reference(
        self, hub: Optional[BitfountHub] = None, project_id: Optional[str] = None
    ) -> DistributedModelProtocol:
        """Returns underlying model if BitfountModelReference.

        If not, just returns self.model.
        """
        # TODO: [BIT-890] perhaps move this logic one level higher so that the algorithm
        # factory always takes a DistributedModelProtocol
        if isinstance(self.model, BitfountModelReference):
            if hub is not None:
                self.model.hub = hub
            model_cls = self.model.get_model(project_id=project_id)
            model = model_cls(
                datastructure=self.model.datastructure,
                schema=self.model.schema,
                **self.model.hyperparameters,
            )
            # If there is a weights file associated with the model then
            # initialise the model with these weights
            # TODO: [BIT-3019] Getting the weights here should not be called on both
            # modeller and worker sides
            if self.model.model_version:
                if weights_bytes := self.model.get_weights(project_id=project_id):
                    logger.info("Applying weights..")
                    model.deserialize(weights_bytes)
            self.model = cast(DistributedModelProtocol, model)
            return self.model
        else:
            return self.model
