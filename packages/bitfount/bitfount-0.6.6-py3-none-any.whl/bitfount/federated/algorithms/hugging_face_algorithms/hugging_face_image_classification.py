"""Hugging Face Image Classification Algorithm."""
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
import pandas as pd
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    pipeline,
    set_seed,
)

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import (
    HuggingFaceImageClassificationInferenceDefaultReturnType,
)
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import DEFAULT_SEED, delegates

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig


logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the HuggingFaceImageClassificationInference algorithm."""

    def initialise(self, task_id: Optional[str] = None, **kwargs: Any) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any], log: bool = False) -> Dict[str, Any]:
        """Simply returns results and optionally logs them."""
        if log:
            for pod_name, response in results.items():
                for _, response_ in enumerate(response):
                    logger.info(f"{pod_name}: {response_['image_classification']}")

        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the HuggingFaceImageClassificationInference algorithm."""

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        seed: int = DEFAULT_SEED,
        batch_size: int = 1,
        class_outputs: Optional[List[str]] = None,
        top_k: int = 5,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.batch_size = batch_size
        self.top_k = top_k
        self.seed = seed
        self.class_outputs = class_outputs
        self.image_column_name = image_column_name

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the model and tokenizer."""
        # TODO: [BIT-3097] Resolve initialise without DP
        if pod_dp:
            logger.warning("The use of DP is not supported, ignoring set `pod_dp`.")
        self.initialise_data(datasource=datasource)
        set_seed(self.seed)
        self.image_processor = AutoImageProcessor.from_pretrained(self.model_id)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_id)
        self.pipe = pipeline(
            "image-classification",
            model=self.model,
            image_processor=self.image_processor,
        )

    def run(
        self,
    ) -> Union[
        pd.DataFrame,
        HuggingFaceImageClassificationInferenceDefaultReturnType,
        Dict[str, Any],
    ]:
        """Runs the pipeline to generate text."""
        preds = self.pipe(
            self.datasource.get_column(self.image_column_name).tolist(),
            batch_size=self.batch_size,
            top_k=self.top_k,
        )
        # Predictions from the above pipeline are returned as a nested
        # list of dictionaries. Each list of dictionaries corresponds
        # to the scores and different labels for a specific datapoint.

        predictions = cast(
            HuggingFaceImageClassificationInferenceDefaultReturnType, preds
        )
        if self.class_outputs:
            if len(predictions[0]) == len(self.class_outputs):
                # this is how all built in models return prediction outputs.
                return pd.DataFrame(data=predictions, columns=self.class_outputs)
            elif len(predictions) == len(self.class_outputs):
                # we can only return dataframe if all arrays have 1d dimension
                dim_check = len([item for item in predictions if len(item) > 1])
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
                    f"the model predictions are a list of {len(predictions[0])}. "
                    "Outputting predictions as a list of numpy arrays."
                )
                return predictions
        else:
            return predictions


@delegates()
class HuggingFaceImageClassificationInference(BaseAlgorithmFactory):
    """Inference for pre-trained Hugging Face image classification models.

    Args:
        model_id: The model id to use for image classification inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        image_column_name: The image column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        top_k: The number of top labels that will be returned by the pipeline.
            If the provided number is higher than the number of labels available
            in the model configuration, it will default to the number of labels.
            Defaults to 5.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.

    Attributes:
        model_id: The model id to use for image classification inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        image_column_name: The image column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        top_k: The number of top labels that will be returned by the pipeline.
            If the provided number is higher than the number of labels available
            in the model configuration, it will default to the number of labels.
            Defaults to 5.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.
    """

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        seed: int = DEFAULT_SEED,
        batch_size: int = 1,
        class_outputs: Optional[List[str]] = None,
        top_k: int = 5,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.image_column_name = image_column_name
        self.batch_size = batch_size
        self.top_k = top_k
        self.class_outputs = class_outputs
        self.seed = seed

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "image_column_name": fields.Str(required=True),
        "batch_size": fields.Int(required=False),
        "top_k": fields.Int(required=False),
        "class_outputs": fields.List(fields.String(), allow_none=True),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the HuggingFaceImageClassificationInference algorithm."""  # noqa: B950
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the HuggingFaceImageClassification algorithm."""
        return _WorkerSide(
            model_id=self.model_id,
            class_outputs=self.class_outputs,
            image_column_name=self.image_column_name,
            top_k=self.top_k,
            batch_size=self.batch_size,
            seed=self.seed,
            **kwargs,
        )
