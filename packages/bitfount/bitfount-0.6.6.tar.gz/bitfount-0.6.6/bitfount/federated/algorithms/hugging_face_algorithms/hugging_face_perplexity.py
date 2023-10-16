"""Hugging Face Perplexity Algorithm.

Reference:
https://huggingface.co/docs/transformers/perplexity#example-calculating-perplexity-with-gpt2-in-transformers
"""
from typing import Any, ClassVar, Dict, Mapping, Optional

from marshmallow import fields
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import DEFAULT_SEED, delegates

DEFAULT_STRIDE = 512


logger = _get_federated_logger(__name__)


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the HuggingFacePerplexityEvaluation algorithm."""

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any]) -> Dict[str, Any]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the HuggingFacePerplexityEvaluation algorithm."""

    def __init__(
        self,
        model_id: str,
        text_column_name: str,
        stride: int,
        seed: int,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.stride = stride
        self.seed = seed

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
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, trust_remote_code=True
        )

    def run(self) -> pd.DataFrame:
        """Runs the pipeline to compute perplexities.

        The function calculates perplexity for each prompt in the
        provided data source. Perplexity is the average exponentiated
        loss obtained from the model. To handle fixed-length causal language
        models with a maximum context, we utilize a sliding window strategy.
        This strategy breaks the sequence into subsequences with a sliding
        context window, preventing poor approximation of the fully-factorized
        perplexity. This approach ensures that the model has sufficient
        context when making each prediction, leading to more accurate results.
        """
        perplexities = []
        for prompt in self.datasource.get_column(self.text_column_name).tolist():
            encodings = self.tokenizer(prompt, return_tensors="pt")
            # model's maximum context size (tokens)
            max_length = self.model.config.n_positions
            # The number of tokens as context when calculating conditional likelihood
            # of any one token (see DEFAULT_STRIDE)
            stride = self.stride
            seq_len = encodings.input_ids.size(1)

            nlls = []
            prev_end_loc = 0
            # Sliding window strategy
            for begin_loc in range(0, seq_len, stride):
                end_loc = min(begin_loc + max_length, seq_len)
                trg_len = end_loc - prev_end_loc
                input_ids = encodings.input_ids[:, begin_loc:end_loc]
                target_ids = input_ids.clone()
                # Avoid token overlap from influencing loss
                # by setting to -100.
                target_ids[:, :-trg_len] = -100

                with torch.no_grad():
                    outputs = self.model(input_ids, labels=target_ids)
                    # Loss = trg_len - 1 (internal shift of labels to the left by 1)
                    neg_log_likelihood = outputs.loss

                nlls.append(neg_log_likelihood)

                prev_end_loc = end_loc
                if end_loc == seq_len:
                    break

            ppl = torch.exp(torch.stack(nlls).mean()).item()
            perplexities.append(ppl)

        return pd.DataFrame({"results": perplexities})


@delegates()
class HuggingFacePerplexityEvaluation(BaseAlgorithmFactory):
    """Hugging Face Perplexity Algorithm.

    Args:
        model_id: The model id to use for evaluating its perplexity.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The single column to query against. Should contain
            text for generation.
        stride: Sets the stride of the algorithm. Defaults to 512.
        seed: Sets the seed of the algorithm. For reproducible behaviour
            it defaults to 42.

    Attributes:
        model_id: The model id to use for evaluation.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts models with a causal language
            modeling head.
        text_column_name: The single column to query against. Should contain
            text for generation.
        stride: Sets the stride of the algorithm. Defaults to 512.
        seed: Sets the seed of the algorithm. For reproducible behaviour
            it defaults to 42.
    """

    def __init__(
        self,
        model_id: str,
        text_column_name: str,
        stride: int = DEFAULT_STRIDE,
        seed: int = DEFAULT_SEED,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.text_column_name = text_column_name
        self.stride = stride
        self.seed = seed

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "text_column_name": fields.Str(required=True),
        "stride": fields.Int(required=False, missing=DEFAULT_STRIDE),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the HuggingFacePerplexityEvaluation algorithm."""  # noqa: B950
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the HuggingFacePerplexityEvaluation algorithm."""  # noqa: B950
        return _WorkerSide(
            model_id=self.model_id,
            text_column_name=self.text_column_name,
            stride=self.stride,
            seed=self.seed,
            **kwargs,
        )
