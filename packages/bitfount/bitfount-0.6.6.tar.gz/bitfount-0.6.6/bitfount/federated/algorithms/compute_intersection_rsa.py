"""RSA Blinding Private Set intersection.

Order of operations:

1. Modeller sends the task request to the worker, containing
    the columns on which the intersection should be performed.
2. Worker generates an RSA key pair, and sends the public key
    to the modeller, keeping the private key to themself.
3. Worker hashes and uses his private key to encrypt each
    row for the relevant columns, and then hashes again the obtained values.

    Modeller receives the public key from the pod. Then he
    chooses random factors (as many as the size of the rows
    in his data), which he encrypts using the public key.
    He then hashes each row of his input and multiplies it
    with the encrypted random factors, which is referred
    to as blinding.
4. Modeller sends his blinded inputs to the worker.
5. Worker receives the blinded inputs from the modeller.
    He first encrypts the blinded values using his private
    key, and then hashes each of the results. He then sends
    the list of blinded hashed values and the list of
    hashed values from step 3 to the modeller.
6. Modeller receives the two lists from the pod.
    He then can compute the private set intersection.

For more details see: https://eprint.iacr.org/2009/491.pdf
"""
from __future__ import annotations

import secrets
import sys
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Tuple, Union, cast

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.hashes import HashAlgorithm
from marshmallow import fields
import pandas as pd

from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.exceptions import (
    BlindingError,
    OutOfBoundsError,
    PSIMultiTableError,
    PSIUnsupportedDataSourceError,
    UnBlindingError,
)
from bitfount.federated.mixins import _PSIAlgorithmsMixIn
from bitfount.federated.types import _DataLessAlgorithm
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import _powinv, _powmod, delegates

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig


def hash(record: Any, hash_function: HashAlgorithm) -> int:
    """Compute the hash of an individual record.

    Args:
        record: The record to hash.
        hash_function: the hash function to use.

    Returns:
        An integer corresponding to the hashed value of the record.
    """
    # Encode the string to bytes
    encoded_x = str(record).encode()
    # Compute the hash
    digest = hashes.Hash(hash_function)
    digest.update(encoded_x)
    hashed_value = digest.finalize()
    # Return the hash as an integer
    return int.from_bytes(hashed_value, sys.byteorder)


def hash_set(
    dataset: Union[pd.DataFrame, List[Any], pd.Series],
    hash_function: HashAlgorithm,
) -> List[int]:
    """Hash the dataset with the given hash function.

    Returns:
        The hashed dataset as a list of integers.
    """
    if isinstance(dataset, pd.DataFrame):
        hashed_list = []
        for _, row in dataset.iterrows():
            # Remove the pd.dataframe index column from each row
            # Each row is a series now, if there is a column 'name'
            # in the series it should not be deleted.
            row.name = None
            hashed_list.append(hash(row, hash_function))
        return hashed_list
    elif isinstance(dataset, (list, pd.Series)):
        return [hash(item, hash_function) for item in dataset]
    else:
        raise TypeError(f"Expected DataFrame, or list or Series. Got: {type(dataset)}")


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the RSABlind algorithm.

    Args:
        columns_to_intersect: The modeller's columns from their datasource
            on which the private set intersection will be computed as a
            list of strings. Defaults to None.
        table: The modeller's table from their datasource,
            if the datasource is multitable, on which the private set
            intersection will be computed as a string. Defaults to None.

    Attributes:
        first_hash_function: The first hash function used in the psi algorithm.
        second_hash_function: The second hash function used in the psi algorithm.
    """

    def __init__(
        self,
        columns_to_intersect: Optional[List[str]] = None,
        table: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.columns_to_intersect = columns_to_intersect
        self.table = table
        self.first_hash_function = hashes.SHA256()
        self.second_hash_function = hashes.SHA512_256()
        self.data: pd.DataFrame

    def initialise(
        self,
        task_id: Optional[str] = None,
        datasource: Optional[BaseSource] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the psi algorithm on the modeller side.

        More specifically, set the public key parameters,
        load and hash the data, generate random factors, and blind the dataset.

        Args:
            datasource: The datasource on which the psi will be performed.

        Raises:
            PSIUnsupportedDataSourceError: If the datasource is an Iterable datasource.
            PSIMultiTableError: If the datasource is multi-table but no table name is
                provided.
        """
        datasource = cast(BaseSource, datasource)
        if datasource.iterable:
            raise PSIUnsupportedDataSourceError(
                "The ComputeIntersectionRSA algorithm does not support "
                "iterable datasources."
            )

        if datasource.multi_table and self.table is None:
            raise PSIMultiTableError(
                "You are trying to perform a PrivateSetIntersection task on a "
                "multitable datasource. Please specify the target table on which "
                "the Private Set Intersection should be performed."
            )
        self.datasource = datasource

    def get_modeller_set(self, public_key: RSAPublicKey) -> List[int]:
        """Get the modeller set.

        Args:
            datasource: The datasource on which the psi will be performed.
            public_key: The public key received from the pod.

        Returns:
            The hashed and blinded set.
        """
        # Public key consists of `n`, the modulus, and `e`, the encryption key.
        self.n, self.e = self._get_public_key_numbers(public_key)

        # Get the data
        if self.table:
            self.datasource.load_data(table_name=self.table)
        else:
            self.datasource.load_data()

        self.data = self.datasource.data

        # Subset the data if needed
        if self.columns_to_intersect:
            self.data = self.data[self.columns_to_intersect]

        # Compute the hashes
        self.hashed_data = hash_set(self.data, self.first_hash_function)
        # Generate random factors for blinding
        self.random_factors = self.generate_random_factors(len(self.data))

        return self.blind_set()

    def _get_public_key_numbers(self, public_key: RSAPublicKey) -> Tuple[int, int]:
        """Get the public key parameters from the RSA public key.

        Returns:
            `n`, the modulus for the public key, and `e`, the public encryption key.
        """
        return public_key.public_numbers().n, public_key.public_numbers().e

    def generate_random_factors(self, n_elements: int) -> List[Tuple[int, int]]:
        """Generate n_elements random factors, then invert and encrypt them.

        Args:
           n_elements: number of random factors to generate.

        Returns:
           A list of tuples, each tuple is composed of the inverse and
           encryption of a random factor.
        """
        random_factors = []
        iteration = 0
        while iteration < n_elements:
            r = secrets.randbelow(self.n)
            try:
                r_inv = _powinv(r, self.n)
            except ValueError:
                # If the random value is not invertible continue and try again
                continue
            r_encrypted = _powmod(r, self.e, self.n)
            iteration += 1
            random_factors.append((r_inv, r_encrypted))
        return random_factors

    def blind(self, record: int, rf_tuple: Tuple[int, int]) -> int:
        """Blind an element using the encryption of a random factor.

        Args:
            record: integer in the range [0, n), where n is the RSA modulus.
            rf_tuple: tuple composed of the inverse and encryption of a random
                factor.

        Returns:
            The blinded version of the element integer x.
        """
        rf_encrypted = rf_tuple[1]
        return (record * rf_encrypted) % self.n

    def unblind(self, integer: int, random_factor_tuple: Tuple[int, int]) -> int:
        """Blind an element using the inverse of a random factor.

        Args:
            integer: integer in the range [0, n), where n is the RSA modulus.
            random_factor_tuple: tuple composed of the inverse and
                encryption of a random factor.

        Returns:
            The unblinded version of the blinded element x.
        """
        rf_inv = random_factor_tuple[0]
        return (integer * rf_inv) % self.n

    def blind_set(self) -> List[int]:
        """Blind a set of elements using the encryption of random factors.

        Returns:
            A list of integers representing the blinded set.
        """
        if len(self.hashed_data) > len(self.random_factors):
            raise BlindingError("There are more elements than random factors")

        blinded_set = []
        for x, rf in zip(self.hashed_data, self.random_factors):
            b = self.blind(x, rf)
            blinded_set.append(b)

        return blinded_set

    def unblind_set(self, dataset: List[int]) -> List[int]:
        """Unblind a set of elements using the inverse of random factors.

        Args:
            dataset: list of integers in the range [0, n), where n is the RSA modulus.

        Returns:
            A list of integers representing the unblinded set X.
        """
        if len(dataset) > len(self.random_factors):
            raise UnBlindingError("There are more elements than random factors")

        unblinded_set = []
        for record, rf_tuple in zip(dataset, self.random_factors):
            unblinded = self.unblind(record, rf_tuple)
            unblinded_set.append(unblinded)
        return unblinded_set

    def intersect(
        self,
        modeller_orig_df: pd.DataFrame,
        blinded_modeller_set: List[int],
        pod_set: List[int],
    ) -> pd.DataFrame:
        """Compute the intersection of the client and server set.

        Args:
            modeller_orig_df: ordered client set.
            blinded_modeller_set: ordered signatures of the client set (unblinded).
            pod_set: signed server set.

        Returns:
            A list of integers representing the intersection of the client and
            server set.
        """
        result = []
        for index in range(len(blinded_modeller_set)):
            if blinded_modeller_set[index] in pod_set:
                result.append(modeller_orig_df.iloc[index])
        return pd.DataFrame(result)

    def run(self, pod_set: List[int], modeller_set: List[int]) -> pd.DataFrame:
        """Runs the modeller side of the algorithm.

        First, it unblinds the modeller set obtained from the worker.
        Then, it hashes the obtained set, and finally performs the intersection.
        """
        unblinded_set = self.unblind_set(modeller_set)
        hashed_modeller_set = hash_set(unblinded_set, self.second_hash_function)
        return self.intersect(self.data, hashed_modeller_set, pod_set)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the RSABlind algorithm.

    Args:
        columns_to_intersect: The pod's columns from their datasource
            on which the private set intersection will be computed as a
            list of strings. Defaults to None.
        table: The pod's table from their datasource,
            if the datasource is multitable, on which the private set
            intersection will be computed as a string. Defaults to None.

    """

    def __init__(
        self,
        columns_to_intersect: Optional[List[str]] = None,
        table: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.columns_to_intersect = columns_to_intersect
        self.table = table
        # Set up hash functions algorithms to use
        self.first_hash_function = hashes.SHA256()
        self.second_hash_function = hashes.SHA512_256()
        # Set up private and public key parameters
        self.private_key, self.public_key = _RSAEncryption.generate_key_pair()
        self.n = self.public_key.public_numbers().n
        self.d = self.private_key.private_numbers().d
        self.data: pd.DataFrame

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the worker-side algorithm.

        Args:
            datasource: The datasource of the worker on which the
                intersection will be performed.
            columns_to_intersect: The columns from the worker datasource
                on which to perform the intersection.

        Returns:
            The pod's double hashed set.

        Raises:
            PSIUnsupportedDataSourceError: If the datasource is an Iterable datasource.
            PSIMultiTableError: If the datasource is multi-table but no table name is
                provided.
        """
        if datasource.iterable:
            raise PSIUnsupportedDataSourceError(
                "The ComputeIntersectionRSA algorithm does not support "
                "iterable datasources."
            )

        if datasource.multi_table and self.table is None:
            raise PSIMultiTableError(
                "You are trying to perform a PrivateSetIntersection task on a "
                "multitable datasource. Please specify the target table on which "
                "the Private Set Intersection should be performed."
            )
        self.initialise_data(datasource=datasource)

    def initialise_data(self, datasource: BaseSource) -> None:
        """Load the data from the datasource according the specified table and columns.

        Sets `self.data` on which the psi will be performed.

        Args:
            datasource: The datasource on which the psi will be performed.
        """
        # Get the data
        if self.table:
            datasource.load_data(table_name=self.table)
        else:
            datasource.load_data()

        self.data = datasource.data

        # Subset the data if needed
        if self.columns_to_intersect:
            self.data = self.data[self.columns_to_intersect]

    def run(self, modeller_set: List[int]) -> Tuple[List[int], List[int]]:
        """Runs the worker-side of the algorithm.

        Args:
            modeller_set: The blinded set received from the modeller.

        Returns:
            A tuple containing the pod's double hashed set and the modeller's
            unblinded set.
        """
        hashed_data = hash_set(self.data, self.first_hash_function)
        decrypted_set = self.decrypt_set(hashed_data)
        pod_set = hash_set(decrypted_set, self.second_hash_function)
        return pod_set, self.decrypt_set(modeller_set)

    def decrypt(self, item: int) -> int:
        """Sign a single element using the RSA private key.

        Args:
            item: integer in the range [0, n), where n is the RSA modulus.

        Returns:
            The signature of item, computed as item^d modulus n.
        """
        if item < 0 or item >= self.n:
            raise OutOfBoundsError(f"x should be in range [0, {self.n})")
        return _powmod(item, self.d, self.n)

    def decrypt_set(self, data: List[int]) -> List[int]:
        """Decrypt a set of elements using the RSA private key.

        Args:
            data: list of integers in the range [0, n), where n is the RSA modulus.

        Returns:
            A list of integers representing the signatures of the set X.
        """
        return [self.decrypt(item) for item in data]


@delegates()
class ComputeIntersectionRSA(
    BaseAlgorithmFactory, _PSIAlgorithmsMixIn, _DataLessAlgorithm
):
    """Algorithm for computing the private set intersection with RSA blinding.

    :::caution

    This algorithm does not work with iterable datasources such as multi-table
    databases.

    :::

    Args:
        datasource_columns: The modeller's columns from their datasource
            on which the private set intersection will be computed as a
            list of strings. Defaults to None.
        datasource_table: The modeller's table from their datasource,
            if the datasource is multitable, on which the private set
            intersection will be computed as a string. Defaults to None.
        pod_columns: The pod's columns from their datasource
            on which the private set intersection will be computed as a
            list of strings. Defaults to None.
        pod_table: The pod's table from their datasource,
            if the datasource is multitable, on which the private set
            intersection will be computed as a string. Defaults to None.

    Attributes:
        pod_columns: The pod's columns from their datasource
            on which the private set intersection will be computed as a
            list of strings. Defaults to None.
        pod_table: The pod's table from their datasource,
            if the datasource is multitable, on which the private set
            intersection will be computed as a string. Defaults to None.

    """

    # We only need to serialize the pod columns & table
    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "pod_columns": fields.List(fields.String(default=None), allow_none=True),
        "pod_table": fields.String(allow_none=True),
    }

    def __init__(
        self,
        datasource_columns: Optional[List[str]] = None,
        datasource_table: Optional[str] = None,
        pod_columns: Optional[List[str]] = None,
        pod_table: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._modeller_cols = datasource_columns
        self._modeller_table = datasource_table
        self.pod_columns = pod_columns
        self.pod_table = pod_table

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the SqlQuery algorithm."""
        return _ModellerSide(
            columns_to_intersect=self._modeller_cols,
            table=self._modeller_table,
            **kwargs,
        )

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the SqlQuery algorithm."""
        return _WorkerSide(
            columns_to_intersect=self.pod_columns, table=self.pod_table, **kwargs
        )
