"""Algorithm to evaluate a model on remote data."""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Union,
    cast,
)

from marshmallow import fields
import numpy as np
import pandas as pd

from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.hub.api import BitfountHub
from bitfount.types import _SerializedWeights
from bitfount.utils import delegates

if TYPE_CHECKING:
    from bitfount.types import (
        T_FIELDS_DICT,
        DistributedModelProtocol,
        _DistributedModelTypeOrReference,
    )

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerModelAlgorithm):
    """Modeller side of the ModelInference algorithm."""

    def run(
        self, results: Mapping[str, Union[List[np.ndarray], pd.DataFrame]]
    ) -> Dict[str, Union[List[np.ndarray], pd.DataFrame]]:
        """Simply returns predictions."""
        return dict(results)


class _WorkerSide(_BaseWorkerModelAlgorithm):
    """Worker side of the ModelInference algorithm."""

    def __init__(
        self,
        *,
        model: DistributedModelProtocol,
        class_outputs: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, **kwargs)
        self.class_outputs = class_outputs

    def run(
        self, model_params: _SerializedWeights, **kwargs: Any
    ) -> Union[List[np.ndarray], pd.DataFrame, Dict[str, np.ndarray]]:
        """Runs evaluation and returns metrics."""
        self.update_params(model_params)
        preds = self.model.predict(self.datasource)
        predictions = cast(List[np.ndarray], preds)
        if self.class_outputs:
            if predictions[0].shape[0] == len(self.class_outputs):
                # this is how all built in models return prediction outputs.
                return pd.DataFrame(data=predictions, columns=self.class_outputs)
            elif len(predictions) == len(self.class_outputs):
                # we can only return dataframe if all arrays have 1d dimension
                dim_check = len([item for item in predictions if item.ndim > 1])
                if dim_check == 0:
                    # we return dataframe
                    return pd.DataFrame(
                        dict(zip(self.class_outputs, predictions)),
                        columns=self.class_outputs,
                    )
                else:
                    # we return dictionary
                    return {
                        output: pred
                        for output, pred in zip(self.class_outputs, predictions)
                    }
            else:
                logger.warning(
                    "Class outputs provided do not match the model prediction output. "
                    f"You provided a list of {len(self.class_outputs)}, and "
                    f"the model predictions are a list of {predictions[0].shape[0]}. "
                    "Outputting predictions as a list of numpy arrays."
                )
                return predictions
        else:
            return predictions


@delegates()
class ModelInference(_BaseModelAlgorithmFactory):
    """Algorithm for running inference on a model and returning the predictions.

    :::danger

    This algorithm could potentially return the data unfiltered so should only be used
    when the other party is trusted.

    :::

    Args:
        model: The model to infer on remote data.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.

    Attributes:
        model: The model to infer on remote data.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "class_outputs": fields.List(fields.String(), allow_none=True)
    }

    def __init__(
        self,
        *,
        model: _DistributedModelTypeOrReference,
        class_outputs: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        self.class_outputs = class_outputs
        super().__init__(model=model, **kwargs)

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ModelInference algorithm."""
        model = self._get_model_from_reference(project_id=self.project_id)
        return _ModellerSide(model=model, **kwargs)

    def worker(self, hub: BitfountHub, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the ModelInference algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
        """
        model = self._get_model_from_reference(hub=hub, project_id=self.project_id)
        return _WorkerSide(model=model, class_outputs=self.class_outputs, **kwargs)
