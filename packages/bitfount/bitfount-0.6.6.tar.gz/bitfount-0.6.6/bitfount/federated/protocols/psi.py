"""Private Set Intersection protocol."""
from __future__ import annotations

import time
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    List,
    Optional,
    Protocol,
    Tuple,
    runtime_checkable,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource
import bitfount.federated.algorithms.base as algorithms
from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.exceptions import PSINoDataSourceError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseCompatibleModellerAlgorithm,
    BaseCompatibleWorkerAlgorithm,
    BaseModellerProtocol,
    BaseProtocolFactory,
    BaseWorkerProtocol,
)
from bitfount.federated.transport.modeller_transport import (
    _get_psi_datasets_from_workers,
    _get_public_key,
    _ModellerMailbox,
    _send_psi_dataset_modeller,
)
from bitfount.federated.transport.worker_transport import (
    _get_psi_dataset,
    _send_psi_dataset_worker,
    _send_public_key,
    _WorkerMailbox,
)
from bitfount.types import T_NESTED_FIELDS
from bitfount.utils import delegates

if TYPE_CHECKING:
    from bitfount.federated.pod_vitals import _PodVitals
    from bitfount.hub.api import BitfountHub


logger = _get_federated_logger(__name__)


@runtime_checkable
class _PSICompatibleModeller(BaseCompatibleModellerAlgorithm, Protocol):
    """Defines modeller-side algorithm compatibility."""

    def get_modeller_set(self, public_key: RSAPublicKey) -> List[int]:
        """Returns the modeller-side set."""
        ...

    def run(self, pod_set: List[int], modeller_set: List[int]) -> pd.DataFrame:
        """Runs the modeller-side algorithm."""
        ...


@runtime_checkable
class _PSICompatibleWorker(BaseCompatibleWorkerAlgorithm, Protocol):
    public_key: RSAPublicKey

    def run(self, modeller_set: List[int]) -> Tuple[List[int], List[int]]:
        """Runs the worker-side algorithm."""
        ...


class _ModellerSide(BaseModellerProtocol):
    """Modeller side of the PrivateSetIntersection protocol."""

    algorithm: _PSICompatibleModeller
    datasource: BaseSource

    def __init__(
        self,
        *,
        algorithm: _PSICompatibleModeller,
        datasource: Optional[BaseSource] = None,
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        if datasource is None:
            # Datasource is optional to match the parent class signature.
            raise PSINoDataSourceError(
                "You are trying to run a PSI task with no datasource. "
                "Please provide a datasource and try again."
            )
        self.datasource = datasource
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def _send_psi_data_modeller(self, dataset: List[int]) -> None:
        """Sends psi dataset to workers."""
        logger.debug("Sending PSI dataset to the worker.")
        # Change integers to strings so msgpack can handle them.
        str_dataset = [str(item) for item in dataset]
        await _send_psi_dataset_modeller(str_dataset, self.mailbox)

    async def _receive_public_key(self) -> RSAPublicKey:
        """Receives public key from worker."""
        logger.debug("Receiving PSI parameters")
        serialized_keys: List[bytes] = await _get_public_key(self.mailbox)
        # We only support psi with one pod, so get the first key only.
        serialized_key = serialized_keys[0]
        # Cast to RSAPublicKEy, as it is the expected key type.
        return _RSAEncryption.load_public_key(serialized_key)

    async def _receive_psi_datasets_from_workers(self) -> Tuple[List[int], List[int]]:
        """Receives psi datasets from worker."""
        logger.debug("Receiving PSI datasets")
        psi_datasets: List[
            Tuple[List[str], List[str]]
        ] = await _get_psi_datasets_from_workers(self.mailbox)
        # We only support psi with one pod, so get the first item of the list.
        psi_datasets_str = psi_datasets[0]
        # Change dataset to int.
        # The first list of the tuple is the pod set, and the second is the modeller set
        psi_datasets_int = (
            [int(item) for item in psi_datasets_str[0]],
            [int(item) for item in psi_datasets_str[1]],
        )
        return psi_datasets_int

    def initialise(
        self,
        task_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Override base initialise method to pass datasource during initialisation."""
        self.algorithm.initialise(
            datasource=self.datasource,
            task_id=task_id,
            **kwargs,
        )

    async def run(
        self,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Runs Modeller side of the protocol."""
        public_key = await self._receive_public_key()
        modeller_input = self.algorithm.get_modeller_set(public_key)
        await self._send_psi_data_modeller(modeller_input)
        pod_set, modeller_set = await self._receive_psi_datasets_from_workers()
        modeller_results = self.algorithm.run(pod_set, modeller_set)
        return modeller_results


class _WorkerSide(BaseWorkerProtocol):
    """Worker side of the PrivateSetIntersection protocol."""

    algorithm: _PSICompatibleWorker

    def __init__(
        self,
        *,
        algorithm: _PSICompatibleWorker,
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def _receive_modeller_psi_dataset(self) -> List[int]:
        """Receives psi dataset from modeller."""
        logger.debug("Receiving PSI dataset from modeller.")
        str_dataset = await _get_psi_dataset(self.mailbox)
        return [int(item) for item in str_dataset]

    async def _send_public_key_to_modeller(self, public_key: RSAPublicKey) -> None:
        """Sends the public key for psi to modeller."""
        await _send_public_key(public_key, self.mailbox)

    async def _send_psi_data_to_modeller(
        self, dataset: Tuple[List[int], List[int]]
    ) -> None:
        """Sends the psi datasets back to the modeller."""
        # Change integers to strings so msgpack can handle them.
        str_tuple = (
            [str(item) for item in dataset[0]],
            [str(item) for item in dataset[1]],
        )
        await _send_psi_dataset_worker(str_tuple, self.mailbox)

    async def run(
        self,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> None:
        """Runs Worker side of the protocol."""
        if pod_vitals:
            pod_vitals.last_task_execution_time = time.time()
        await self._send_public_key_to_modeller(self.algorithm.public_key)
        modeller_set = await self._receive_modeller_psi_dataset()
        pod_set, hashed_modeller_set = self.algorithm.run(modeller_set)
        await self._send_psi_data_to_modeller((pod_set, hashed_modeller_set))


@runtime_checkable
class _PSICompatibleAlgoFactory_(BaseCompatibleAlgoFactory, Protocol):
    """Defines algo factory compatibility."""

    pod_columns: Optional[List[str]]
    pod_table: Optional[str]

    def modeller(self, **kwargs: Any) -> _PSICompatibleModeller:
        """Creates a modeller-side algorithm."""
        ...

    def worker(self, **kwargs: Any) -> _PSICompatibleWorker:
        """Creates a worker-side algorithm."""
        ...


@delegates()
class PrivateSetIntersection(BaseProtocolFactory):
    """Performs a private set intersection with the provided algorithm.

    For more details, look at the algorithm description to
    understand how the intersection is computed.

    Args:
        algorithm: The algorithm to run.
        datasource: The modeller's datasource.

    Attributes:
        name: The name of the protocol.
        algorithm: The algorithm to run. This must be compatible with the
            `PrivateSetIntersection` protocol.

    Raises:
        TypeError: If the `algorithm` is not compatible with the protocol.
        PSINoDataSourceError: If you are trying to run the protocol without
            a datasource.
    """

    algorithm: _PSICompatibleAlgoFactory_
    nested_fields: ClassVar[T_NESTED_FIELDS] = {"algorithm": algorithms.registry}

    def __init__(
        self,
        *,
        algorithm: _PSICompatibleAlgoFactory_,
        datasource: Optional[BaseSource] = None,
        **kwargs: Any,
    ) -> None:
        self.datasource = datasource
        super().__init__(algorithm=algorithm, **kwargs)

    @classmethod
    def _validate_algorithm(
        cls,
        algorithm: BaseCompatibleAlgoFactory,
    ) -> None:
        """Checks that `algorithm` is compatible with the protocol."""
        if not isinstance(
            algorithm,
            (_PSICompatibleAlgoFactory_,),
        ):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    def modeller(self, mailbox: _ModellerMailbox, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the PrivateSetIntersection protocol."""
        algorithm = self.algorithm.modeller()
        return _ModellerSide(
            algorithm=algorithm,
            datasource=self.datasource,
            mailbox=mailbox,
            **kwargs,
        )

    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> _WorkerSide:
        """Returns the worker side of the PrivateSetIntersection protocol."""
        return _WorkerSide(
            algorithm=self.algorithm.worker(hub=hub),
            mailbox=mailbox,
            **kwargs,
        )
