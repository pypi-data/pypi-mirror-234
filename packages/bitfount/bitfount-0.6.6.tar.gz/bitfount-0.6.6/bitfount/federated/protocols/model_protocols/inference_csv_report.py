"""Protocol for combinging a single model inference and a csv algorithm."""
from __future__ import annotations

import os
import time
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Union,
    cast,
    runtime_checkable,
)

import pandas as pd

from bitfount.federated.algorithms.csv_report_algorithm import (
    _WorkerSide as _CSVWorkerSide,
)
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseCompatibleModellerAlgorithm,
    BaseCompatibleWorkerAlgorithm,
    BaseModellerProtocol,
    BaseProtocolFactory,
    BaseWorkerProtocol,
)
from bitfount.federated.transport.modeller_transport import (
    _ModellerMailbox,
    _send_model_parameters,
)
from bitfount.federated.transport.worker_transport import (
    _get_model_parameters,
    _WorkerMailbox,
)
from bitfount.types import (
    DistributedModelProtocol,
    _SerializedWeights,
    _StrAnyDict,
    _Weights,
)

if TYPE_CHECKING:
    from bitfount.federated.model_reference import BitfountModelReference
    from bitfount.hub.api import BitfountHub

logger = _get_federated_logger("bitfount.federated.protocols" + __name__)


@runtime_checkable
class _InferenceAndCSVReportCompatibleModellerAlgorithm(
    BaseCompatibleModellerAlgorithm, Protocol
):
    """Defines modeller-side algorithm compatibility."""

    def run(self, results: Mapping[str, Any]) -> _StrAnyDict:
        """Runs the modeller-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportCompatibleWorkerAlgorithm(
    BaseCompatibleWorkerAlgorithm, Protocol
):
    """Defines worker-side algorithm compatibility."""

    pass


@runtime_checkable
class _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm(
    _InferenceAndCSVReportCompatibleWorkerAlgorithm, Protocol
):
    """Defines worker-side algorithm compatibility without model params."""

    def run(self) -> Any:
        """Runs the worker-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportModelCompatibleWorkerAlgorithm(
    _InferenceAndCSVReportCompatibleWorkerAlgorithm, Protocol
):
    """Defines worker-side algorithm compatibility with model params needed."""

    def run(
        self,
        model_params: _SerializedWeights,
    ) -> Any:
        """Runs the worker-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportCSVCompatibleWorkerAlgorithm(
    _InferenceAndCSVReportCompatibleWorkerAlgorithm, Protocol
):
    """Defines worker-side algorithm compatibility for CSV algorithm."""

    def run(
        self,
        results_df: Union[pd.DataFrame, List[pd.DataFrame]],
        task_id: Optional[str] = None,
    ) -> pd.DataFrame:
        """Runs the worker-side algorithm."""
        ...


class _ModellerSide(BaseModellerProtocol):
    """Modeller side of the protocol.

    Args:
        algorithm: A list of algorithms to be run by the protocol. This should be
            a list of two algorithms, the first being the model inference algorithm
            and the second being the csv report algorithm.
        mailbox: The mailbox to use for communication with the Workers.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[_InferenceAndCSVReportCompatibleModellerAlgorithm]

    def __init__(
        self,
        *,
        algorithm: Sequence[_InferenceAndCSVReportCompatibleModellerAlgorithm],
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def _send_parameters(self, new_parameters: _SerializedWeights) -> None:
        """Sends central model parameters to workers."""
        logger.debug("Sending global parameters to workers")
        await _send_model_parameters(new_parameters, self.mailbox)

    async def run(
        self,
        iteration: int = 0,
        **kwargs: Any,
    ) -> None:
        """Runs Modeller side of the protocol.

        This just sends the model parameters to the workers and then tells
        the workers when the protocol is finished.
        """
        for algo in self.algorithm:
            if isinstance(algo, _BaseModellerModelAlgorithm):
                initial_parameters: _Weights = algo.model.get_param_states()
                serialized_params = algo.model.serialize_params(initial_parameters)
                await self._send_parameters(serialized_params)
                break

        await self.mailbox.get_evaluation_results_from_workers()
        return None


class _WorkerSide(BaseWorkerProtocol):
    """Worker side of the protocol.

    Args:
        algorithm: A list of algorithms to be run by the protocol. This should be
            a list of two algorithms, the first being the model inference algorithm
            and the second being the csv report algorithm.
        mailbox: The mailbox to use for communication with the Modeller.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        Union[
            _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
            _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
            _InferenceAndCSVReportCSVCompatibleWorkerAlgorithm,
        ]
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            Union[
                _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
                _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
                _InferenceAndCSVReportCSVCompatibleWorkerAlgorithm,
            ]
        ],
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def _receive_parameters(self) -> _SerializedWeights:
        """Receives new global model parameters."""
        logger.debug("Receiving global parameters")
        return await _get_model_parameters(self.mailbox)

    async def run(
        self,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> None:
        """Runs the algorithm on worker side."""
        # Unpack the algorithm into the two algorithms
        model_inference_algo, csv_report_algo = self.algorithm

        if pod_vitals:
            pod_vitals.last_task_execution_time = time.time()
        # Run Inference Algorithm
        if isinstance(model_inference_algo, _BaseWorkerModelAlgorithm):
            model_params = await self._receive_parameters()
            model_inference_algo = cast(
                _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
                model_inference_algo,
            )
            model_predictions = model_inference_algo.run(model_params=model_params)
        else:
            assert not isinstance(  # nosec[assert_used]
                model_inference_algo, _CSVWorkerSide
            )
            model_inference_algo = cast(
                _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
                model_inference_algo,
            )
            results = model_inference_algo.run()
            if not isinstance(results, pd.DataFrame):
                logger.error(
                    "The model output did not return "
                    "a dataframe, so we cannot output "
                    "the predictions to a csv file."
                )
            else:
                model_predictions = results
        model_predictions = cast(pd.DataFrame, model_predictions)

        csv_report_algo = cast(_CSVWorkerSide, csv_report_algo)
        csv_report_algo.run(
            results_df=model_predictions,
            task_id=self.mailbox._task_id,
        )
        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results({})


@runtime_checkable
class _InferenceAndCSVReportCompatibleAlgoFactory(BaseCompatibleAlgoFactory, Protocol):
    """Defines algo factory compatibility."""

    def modeller(
        self, **kwargs: Any
    ) -> _InferenceAndCSVReportCompatibleModellerAlgorithm:
        """Create a modeller-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportCompatibleAlgoFactory_(
    _InferenceAndCSVReportCompatibleAlgoFactory, Protocol
):
    """Defines algo factory compatibility."""

    def worker(
        self, **kwargs: Any
    ) -> Union[
        _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
        _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
    ]:
        """Create a worker-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory(
    _InferenceAndCSVReportCompatibleAlgoFactory, Protocol
):
    """Defines algo factory compatibility."""

    model_id: str

    def worker(
        self, hub: BitfountHub, **kwargs: Any
    ) -> Union[
        _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
        _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
    ]:
        """Create a worker-side algorithm."""
        ...


@runtime_checkable
class _InferenceAndCSVReportCompatibleModelAlgoFactory(
    _InferenceAndCSVReportCompatibleAlgoFactory, Protocol
):
    """Defines algo factory compatibility."""

    model: Union[DistributedModelProtocol, BitfountModelReference]
    pretrained_file: Optional[Union[str, os.PathLike]] = None

    def worker(
        self, hub: BitfountHub, **kwargs: Any
    ) -> Union[
        _InferenceAndCSVReportModelIncompatibleWorkerAlgorithm,
        _InferenceAndCSVReportModelCompatibleWorkerAlgorithm,
    ]:
        """Create a worker-side algorithm."""
        ...


class InferenceAndCSVReport(BaseProtocolFactory):
    """Protocol for running a model inference generating a csv report."""

    def __init__(
        self,
        *,
        algorithm: Sequence[
            Union[
                _InferenceAndCSVReportCompatibleAlgoFactory_,
                _InferenceAndCSVReportCompatibleModelAlgoFactory,
                _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
            ]
        ],
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, **kwargs)

    @classmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Validates the algorithm."""
        if algorithm.class_name not in (
            "bitfount.ModelInference",
            "bitfount.HuggingFaceImageClassificationInference",
            "bitfount.HuggingFaceImageSegmentationInference",
            "bitfount.HuggingFaceTextClassificationInference",
            "bitfount.HuggingFaceTextGenerationInference",
            "bitfount.HuggingFacePerplexityEvaluation",
            "bitfount.CSVReportAlgorithm",
        ):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    def modeller(self, mailbox: _ModellerMailbox, **kwargs: Any) -> _ModellerSide:
        """Returns the Modeller side of the protocol."""
        algorithms = cast(
            Sequence[
                Union[
                    _InferenceAndCSVReportCompatibleAlgoFactory_,
                    _InferenceAndCSVReportCompatibleModelAlgoFactory,
                    _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
                ]
            ],
            self.algorithms,
        )
        modeller_algos = []
        for algo in algorithms:
            if hasattr(algo, "pretrained_file"):
                modeller_algos.append(
                    algo.modeller(pretrained_file=algo.pretrained_file)
                )
            else:
                modeller_algos.append(algo.modeller())
        return _ModellerSide(
            algorithm=modeller_algos,
            mailbox=mailbox,
            **kwargs,
        )

    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> _WorkerSide:
        """Returns worker side of the protocol."""
        algorithms = cast(
            Sequence[
                Union[
                    _InferenceAndCSVReportCompatibleAlgoFactory_,
                    _InferenceAndCSVReportCompatibleModelAlgoFactory,
                    _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
                ]
            ],
            self.algorithms,
        )
        return _WorkerSide(
            algorithm=[algo.worker(hub=hub) for algo in algorithms],
            mailbox=mailbox,
            **kwargs,
        )
