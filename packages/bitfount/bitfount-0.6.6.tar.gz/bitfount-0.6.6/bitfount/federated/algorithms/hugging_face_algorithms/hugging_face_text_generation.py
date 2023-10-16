"""Hugging Face Text Generation Algorithm."""
from __future__ import annotations

from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Literal,
    Mapping,
    Optional,
    Union,
    overload,
)

from marshmallow import fields
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

from bitfount.config import BITFOUNT_DEFAULT_TORCH_DEVICE
from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import TextGenerationDefaultReturnType
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import DEFAULT_SEED, delegates

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig

# This is currently semi-duplicated from `bitfount.backends.pytorch.utils` as it is not
# possible to import it from there without creating a circular dependency.
_TORCH_DTYPES: Dict[str, torch.dtype] = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
    "float64": torch.float64,
}

DEFAULT_MAX_LENGTH = 50
DEFAULT_NUM_RETURN_SEQUENCES = 1
DEFAULT_MIN_NEW_TOKENS = 1
DEFAULT_REPETITION_PENALTY = 1.0
DEFAULT_NUM_BEAMS = 1

logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the HuggingFaceTextGenerationInference algorithm."""

    def initialise(self, task_id: Optional[str] = None, **kwargs: Any) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any], log: bool = False) -> Dict[str, Any]:
        """Simply returns results and optionally logs them."""
        if log:
            for pod_name, response in results.items():
                for _, response_ in enumerate(response):
                    logger.info(f"{pod_name}: {response_['generated_text']}")

        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the HuggingFaceTextGenerationInference algorithm."""

    def __init__(
        self,
        model_id: str,
        text_column_name: Optional[str],
        prompt_format: Optional[str],
        max_length: int,
        num_return_sequences: int,
        seed: int,
        min_new_tokens: int,
        repetition_penalty: float,
        num_beams: int,
        early_stopping: bool,
        pad_token_id: Optional[int],
        eos_token_id: Optional[int],
        device: Optional[str],
        torch_dtype: Literal["bfloat16", "float16", "float32", "float64"],
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.prompt_format = prompt_format
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences
        self.seed = seed
        self.min_new_tokens = min_new_tokens
        self.repetition_penalty = repetition_penalty
        self.num_beams = num_beams
        self.early_stopping = early_stopping
        self.pad_token_id = pad_token_id
        self.eos_token_id = eos_token_id
        self.torch_dtype = torch_dtype

        # Modeller-supplied device takes precedence over environment variable.
        # If neither are set, defaults to "cpu".
        self.device = device or BITFOUNT_DEFAULT_TORCH_DEVICE or "cpu"

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
        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.eos_token_id = self.eos_token_id or tokenizer.eos_token_id
        self.pad_token_id = self.pad_token_id or tokenizer.pad_token_id
        self.generator = pipeline(
            "text-generation",
            model=model,
            pad_token_id=self.pad_token_id,
            device=self.device,
            tokenizer=tokenizer,
            return_full_text=False,
            torch_dtype=_TORCH_DTYPES[self.torch_dtype],
        )

    @overload
    def run(self, prompt: str) -> TextGenerationDefaultReturnType:
        ...

    @overload
    def run(self) -> pd.DataFrame:
        ...

    def run(
        self, prompt: Optional[str] = None
    ) -> Union[TextGenerationDefaultReturnType, pd.DataFrame]:
        """Runs the pipeline to generate text."""
        generator = partial(
            self.generator,
            max_length=self.max_length,
            num_return_sequences=self.num_return_sequences,
            min_new_tokens=self.min_new_tokens,
            repetition_penalty=self.repetition_penalty,
            num_beams=self.num_beams,
            early_stopping=self.early_stopping,
            eos_token_id=self.eos_token_id,
        )
        results: TextGenerationDefaultReturnType
        if prompt and self.text_column_name:
            raise ValueError(
                "Cannot provide both `prompt` and `text_column_name` to `run`."
            )
        elif self.text_column_name:
            text_column = self.datasource.get_column(self.text_column_name).tolist()
            if self.prompt_format:
                text_column = [
                    self.prompt_format.format_map({"context": text})
                    for text in text_column
                ]
            results = generator(text_column)
            results_list = []
            for result in results:
                results_list.append(result[0]["generated_text"])
            return pd.DataFrame({"results": results_list})
        elif prompt:
            results = generator(prompt)
            return results

        raise ValueError("Must provide either `prompt` or `text_column_name`.")


@delegates()
class HuggingFaceTextGenerationInference(BaseAlgorithmFactory):
    """Hugging Face Text Generation Algorithm.

    Args:
        model_id: The model id to use for text generation.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The single column to query against. Should contain
            text for generation. If not provided, the algorithm must be used with a
            protocol which dynamically provides the text to be used for prompting.
        prompt_format: The format of the prompt as a string with a single
            `{context}` placeholder which is where the pod's input will be inserted.
            For example, "You are a Language Model. This is the context: {context}.
            Please summarize it.". This only applies if `text_column_name` is
            provided, it is not used for dynamic prompting. Defaults to None.
        max_length: The maximum length of the sequence to be generated. Defaults to 50.
        num_return_sequences: The number of sequence candidates to return
            for each input. Defaults to 1.
        seed: Sets the seed of the algorithm. For reproducible behaviour
            it defaults to 42.
        min_new_tokens: The minimum number of new tokens to add to the
            prompt. Defaults to 1.
        repetition_penalty: The parameter for repetition penalty. 1.0 means
            no penalty. Defaults to 1.0.
        num_beams: Number of beams for beam search. 1 means no beam search.
            Defaults to 1.
        early_stopping: Whether to stop the generation as soon as there are `num_beams`
            complete candidates. Defaults to True.
        pad_token_id: The id of the token to use as padding token. If None (default),
            it will default to the pad_token_id of the tokenizer.
        eos_token_id: The id of the token to use as the last token for each
            sequence. If None (default), it will default to the eos_token_id of the
            tokenizer.
        device: The device to use for the model. Defaults to None. On the worker side,
            will be set to the environment variable `BITFOUNT_DEFAULT_TORCH_DEVICE`
            if specified, otherwise "cpu".
        torch_dtype: The torch dtype to use for the model. Defaults to "float32".

    Attributes:
        model_id: The model id to use for text generation.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The single column to query against. Should contain
            text for generation. If not provided, the algorithm must be used with a
            protocol which dynamically provides the text to be used for prompting.
        prompt_format: The format of the prompt as a string with a single
            `{context}` placeholder which is where the pod's input will be inserted.
            For example, "You are a Language Model. This is the context: {context}.
            Please summarize it.". This only applies if `text_column_name` is
            provided, it is not used for dynamic prompting. Defaults to None.
        max_length: The maximum length of the sequence to be generated. Defaults to 50.
        num_return_sequences: The number of sequence candidates to return
            for each input. Defaults to 1.
        seed: Sets the seed of the algorithm. For reproducible behaviour
            it defaults to 42.
        min_new_tokens: The minimum number of new tokens to add to the
            prompt. Defaults to 1.
        repetition_penalty: The parameter for repetition penalty. 1.0 means
            no penalty. Defaults to 1.0.
        num_beams: Number of beams for beam search. 1 means no beam search.
            Defaults to 1.
        early_stopping: Whether to stop the generation as soon as there are `num_beams`
            complete candidates. Defaults to True.
        pad_token_id: The id of the token to use as padding token. If None (default),
            it will default to the pad_token_id of the tokenizer.
        eos_token_id: The id of the token to use as the last token for each
            sequence. If None (default), it will default to the eos_token_id of the
            tokenizer.
        device: The device to use for the model. Defaults to None. On the worker side,
            will be set to the environment variable `BITFOUNT_DEFAULT_TORCH_DEVICE`
            if specified, otherwise "cpu".
        torch_dtype: The torch dtype to use for the model. Defaults to "float32".

    Raises:
        ValueError: If `prompt_format` is provided without `text_column_name`.
        ValueError: If `prompt_format` does not contain a single `{context}`
            placeholder.
    """

    def __init__(
        self,
        model_id: str,
        text_column_name: Optional[str] = None,
        prompt_format: Optional[str] = None,
        max_length: int = DEFAULT_MAX_LENGTH,
        num_return_sequences: int = DEFAULT_NUM_RETURN_SEQUENCES,
        seed: int = DEFAULT_SEED,
        min_new_tokens: int = DEFAULT_MIN_NEW_TOKENS,
        repetition_penalty: float = DEFAULT_REPETITION_PENALTY,
        num_beams: int = DEFAULT_NUM_BEAMS,
        early_stopping: bool = True,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[int] = None,
        device: Optional[str] = None,
        torch_dtype: Literal["bfloat16", "float16", "float32", "float64"] = "float32",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.prompt_format = prompt_format
        self.max_length = max_length
        self.num_return_sequences = num_return_sequences
        self.seed = seed
        self.min_new_tokens = min_new_tokens
        self.repetition_penalty = repetition_penalty
        self.num_beams = num_beams
        self.early_stopping = early_stopping
        self.pad_token_id = pad_token_id
        self.eos_token_id = eos_token_id
        self.device = device
        self.torch_dtype = torch_dtype

        if self.prompt_format and not self.text_column_name:
            raise ValueError(
                "Cannot provide `prompt_format` without `text_column_name`."
            )
        elif self.prompt_format and self.text_column_name:
            if "{context}" not in self.prompt_format:
                raise ValueError(
                    "`prompt_format` must contain a single `{context}` placeholder."
                )

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "text_column_name": fields.Str(required=False, missing=None),
        "prompt_format": fields.Str(required=False, missing=None),
        "max_length": fields.Int(required=False, missing=DEFAULT_MAX_LENGTH),
        "num_return_sequences": fields.Int(
            required=False, missing=DEFAULT_NUM_RETURN_SEQUENCES
        ),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
        "min_new_tokens": fields.Int(required=False, missing=DEFAULT_MIN_NEW_TOKENS),
        "repetition_penalty": fields.Float(
            required=False, missing=DEFAULT_REPETITION_PENALTY
        ),
        "num_beams": fields.Int(required=False, missing=DEFAULT_NUM_BEAMS),
        "early_stopping": fields.Bool(required=False, missing=True),
        "pad_token_id": fields.Int(required=False, missing=None),
        "eos_token_id": fields.Int(required=False, missing=None),
        "device": fields.Str(required=False, missing=None),
        "torch_dtype": fields.Str(required=False, missing="float32"),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the HuggingFaceTextGenerationInference algorithm."""  # noqa: B950
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the HuggingFaceTextGenerationInference algorithm."""  # noqa: B950
        return _WorkerSide(
            model_id=self.model_id,
            text_column_name=self.text_column_name,
            prompt_format=self.prompt_format,
            max_length=self.max_length,
            num_return_sequences=self.num_return_sequences,
            seed=self.seed,
            min_new_tokens=self.min_new_tokens,
            repetition_penalty=self.repetition_penalty,
            num_beams=self.num_beams,
            early_stopping=self.early_stopping,
            pad_token_id=self.pad_token_id,
            eos_token_id=self.eos_token_id,
            device=self.device,
            torch_dtype=self.torch_dtype,
            **kwargs,
        )
