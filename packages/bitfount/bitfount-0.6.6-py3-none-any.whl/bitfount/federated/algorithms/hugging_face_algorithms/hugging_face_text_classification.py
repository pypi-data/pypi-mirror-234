"""Hugging Face Text Classification Algorithm."""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
    cast,
)

from marshmallow import fields
import pandas as pd
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
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
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import DEFAULT_SEED, delegates

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig


logger = _get_federated_logger(__name__)
_FunctionToApply = Literal["sigmoid", "softmax", "none"]


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the HuggingFaceTextClassificationInference algorithm."""

    def initialise(self, task_id: Optional[str] = None, **kwargs: Any) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any], log: bool = False) -> Dict[str, Any]:
        """Simply returns results and optionally logs them."""
        if log:
            for pod_name, response in results.items():
                for _, response_ in enumerate(response):
                    logger.info(f"{pod_name}: {response_['text_classification']}")

        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the HuggingFaceTextClassificationInference algorithm."""

    def __init__(
        self,
        model_id: str,
        target_column_name: str,
        batch_size: int = 1,
        class_outputs: Optional[List[str]] = None,
        function_to_apply: Optional[_FunctionToApply] = None,
        seed: int = DEFAULT_SEED,
        top_k: int = 1,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.target_column_name = target_column_name
        self.batch_size = batch_size
        self.class_outputs = class_outputs
        self.function_to_apply = function_to_apply
        self.seed = seed
        self.top_k = top_k

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
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            batch_size=self.batch_size,
            top_k=self.top_k,
            function_to_apply=self.function_to_apply,
        )

    def run(
        self,
    ) -> Union[pd.DataFrame, List[List[Dict[str, Union[str, float]]]], Dict[str, Any]]:
        """Runs the pipeline to generate text."""
        preds = self.pipe(
            self.datasource.get_column(self.target_column_name).tolist(),
            batch_size=self.batch_size,
            top_k=self.top_k,
        )
        # Predictions from the above pipeline are returned as a nested
        # list of dictionaries. Each list of dictionaries corresponds
        # to the scores and different labels for a specific datapoint.
        predictions = cast(list, preds)
        if not self.class_outputs:
            return predictions

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


@delegates()
class HuggingFaceTextClassificationInference(BaseAlgorithmFactory):
    """Inference for pre-trained Hugging Face text classification models.

    Args:
        model_id: The model id to use for text classification inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        target_column_name: The target column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.
        function_to_apply: The function to apply to the model outputs in order
            to retrieve the scores. Accepts four different values: if this argument
            is not specified, then it will apply the following functions according
            to the number of labels - if the model has a single label, will apply
            the `sigmoid` function on the output; if the model has several labels,
            will apply the `softmax` function on the output. Possible values are:
            "sigmoid": Applies the sigmoid function on the output.
            "softmax": Applies the softmax function on the output.
            "none": Does not apply any function on the output. Default to None.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        top_k: The number of top labels that will be returned by the pipeline.
            Defaults to 1.

    Attributes:
        model_id: The model id to use for text classification inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        target_column_name: The target column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        function_to_apply: The function to apply to the model outputs in order
            to retrieve the scores. Accepts four different values: if this argument
            is not specified, then it will apply the following functions according
            to the number of labels - if the model has a single label, will apply
            the `sigmoid` function on the output; if the model has several labels,
            will apply the `softmax` function on the output. Possible values are:
            "sigmoid": Applies the sigmoid function on the output.
            "softmax": Applies the softmax function on the output.
            "none": Does not apply any function on the output. Default to None.
        class_outputs: A list of strings corresponding to prediction outputs.
            If provided, the model will return a dataframe of results with the
            class outputs list elements as columns. Defaults to None.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        top_k: The number of top labels that will be returned by the pipeline.
            Defaults to 1.
    """

    def __init__(
        self,
        model_id: str,
        target_column_name: str,
        batch_size: int = 1,
        class_outputs: Optional[List[str]] = None,
        function_to_apply: Optional[_FunctionToApply] = None,
        seed: int = DEFAULT_SEED,
        top_k: int = 1,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.target_column_name = target_column_name
        self.batch_size = batch_size
        self.class_outputs = class_outputs
        self.function_to_apply = function_to_apply
        self.seed = seed
        self.top_k = top_k

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "target_column_name": fields.Str(required=True),
        "batch_size": fields.Int(required=False),
        "class_outputs": fields.List(fields.String(), allow_none=True),
        "function_to_apply": fields.Str(required=False, allow_none=True),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
        "top_k": fields.Int(required=False),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the HuggingFaceTextClassificationInference algorithm."""  # noqa: B950
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the HuggingFaceTextClassificationInference algorithm."""  # noqa: B950
        return _WorkerSide(
            model_id=self.model_id,
            target_column_name=self.target_column_name,
            batch_size=self.batch_size,
            class_outputs=self.class_outputs,
            function_to_apply=self.function_to_apply,
            seed=self.seed,
            top_k=self.top_k,
            **kwargs,
        )
