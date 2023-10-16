"""Conversation protocol."""
from __future__ import annotations

import time
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    List,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from bitfount.federated.algorithms.base import registry as algorithms_registry
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
    _get_model_responses_from_workers,
    _ModellerMailbox,
    _send_prompt,
)
from bitfount.federated.transport.worker_transport import (
    _get_model_prompt,
    _WorkerMailbox,
)
from bitfount.federated.types import TextGenerationDefaultReturnType
from bitfount.types import T_NESTED_FIELDS, _StrAnyDict
from bitfount.utils import delegates

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub

logger = _get_federated_logger(__name__)


@runtime_checkable
class _ConversationCompatibleModellerAlgorithm(
    BaseCompatibleModellerAlgorithm, Protocol
):
    """Defines modeller-side algorithm compatibility."""

    def run(self, results: Mapping[str, Any], log: bool = False) -> _StrAnyDict:
        """Runs the modeller-side algorithm."""
        ...


@runtime_checkable
class _ConversationCompatibleWorkerAlgorithm(BaseCompatibleWorkerAlgorithm, Protocol):
    """Defines worker-side algorithm compatibility."""

    def run(self, prompt: str) -> TextGenerationDefaultReturnType:
        """Runs the worker-side algorithm."""
        ...


class _ModellerSide(BaseModellerProtocol):
    """Modeller side of the Conversation protocol."""

    algorithm: _ConversationCompatibleModellerAlgorithm

    def __init__(
        self,
        *,
        algorithm: _ConversationCompatibleModellerAlgorithm,
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def run(
        self,
        **kwargs: Any,
    ) -> List[Any]:
        """Runs Modeller side of the protocol."""
        modeller_results: List[Any] = []
        while True:
            prompt = input("Please enter your prompt: ")
            await _send_prompt(prompt, self.mailbox)
            if not prompt:
                break
            logger.info("Sent prompt to pod(s), waiting for response...")
            model_responses = await _get_model_responses_from_workers(self.mailbox)
            modeller_results.append(model_responses)
            self.algorithm.run(model_responses, log=True)

        return modeller_results


class _WorkerSide(BaseWorkerProtocol):
    """Worker side of the Conversation protocol."""

    algorithm: _ConversationCompatibleWorkerAlgorithm

    def __init__(
        self,
        *,
        algorithm: _ConversationCompatibleWorkerAlgorithm,
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def run(
        self,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> Any:
        """Runs Worker side of the protocol."""

        # Pass model_params to initialise where we update the parameters
        while True:
            if pod_vitals:
                pod_vitals.last_task_execution_time = time.time()

            prompt = await _get_model_prompt(self.mailbox)
            if not prompt:
                break
            response = self.algorithm.run(prompt)
            await self.mailbox.send_model_response(response)


@runtime_checkable
class _ConversationCompatibleAlgoFactory(BaseCompatibleAlgoFactory, Protocol):
    """Defines algo factory compatibility."""

    def modeller(self, **kwargs: Any) -> _ConversationCompatibleModellerAlgorithm:
        """Create a modeller-side algorithm."""
        ...

    def worker(self, **kwargs: Any) -> _ConversationCompatibleWorkerAlgorithm:
        """Create a worker-side algorithm."""
        ...


@delegates()
class Conversation(BaseProtocolFactory):
    """Conversation protocol.

    This protocol is used for a conversation between a modeller and a pod. The pod
    does not remember the previous prompts and responses.
    """

    algorithm: _ConversationCompatibleAlgoFactory
    nested_fields: ClassVar[T_NESTED_FIELDS] = {
        "algorithm": algorithms_registry,
    }

    def __init__(
        self,
        *,
        algorithm: _ConversationCompatibleAlgoFactory,
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, **kwargs)

    @classmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Checks that `algorithm` is compatible with the protocol.

        Raises TypeError if `algorithm` is not compatible with the protocol.
        """
        if not isinstance(
            algorithm,
            _ConversationCompatibleAlgoFactory,
        ):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    def modeller(self, mailbox: _ModellerMailbox, **kwargs: Any) -> _ModellerSide:
        """Creates a modeller-side protocol instance."""
        return _ModellerSide(
            algorithm=self.algorithm.modeller(),
            mailbox=mailbox,
            **kwargs,
        )

    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> _WorkerSide:
        """Creates a worker-side protocol instance."""
        return _WorkerSide(
            algorithm=self.algorithm.worker(hub=hub),
            mailbox=mailbox,
            **kwargs,
        )
