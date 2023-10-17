from typing import Optional, Union

import numpy as np


class QUBO:
    def __init__(self, matrix: np.ndarray, offset: Optional[float] = None) -> None:
        self.Q = QUBO.quboize(matrix)
        self.offset = 0.0 if offset is None else float(offset)
        self.dimension = self.Q.shape[0]

    def __call__(self, array: np.ndarray) -> np.ndarray:
        """
        Evaluates a QUBO model in given binary vectors.
        Vectors must be defined column-wise.
        """
        if not np.all(np.isin(array, [0, 1])):
            raise ValueError("Expected binary values only.")
        return (
            np.einsum("ij, ji -> i", array.T, self.Q @ array).reshape(-1) + self.offset
        )

    @staticmethod
    def __check_matrix(matrix: np.ndarray):
        if matrix.ndim != 2:
            raise ValueError(
                f"Expected a 2 dimensional array but got {matrix.ndim} dimensions."
            )
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Array must be square.")

    @staticmethod
    def quboize(matrix: np.ndarray) -> np.ndarray:
        QUBO.__check_matrix(matrix)
        return np.triu(matrix + matrix.T - np.diag(np.diag(matrix)))
