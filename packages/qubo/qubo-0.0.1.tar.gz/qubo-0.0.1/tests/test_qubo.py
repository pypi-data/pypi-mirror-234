import numpy as np
import pytest

from src.qubo import QUBO


def test_qubo():
    Q = np.array([[1, 2], [3, 4]])
    qubo = QUBO(Q)
    assert np.all(np.array([[1, 5], [0, 4]]) == qubo.Q)
    assert 0.0 == qubo.offset
    assert 2 == qubo.dimension


def test_qubo_with_already_upper_triangular_matrix():
    Q = np.array([[1, 2], [0, 3]])
    qubo = QUBO(Q)
    assert np.all(Q == qubo.Q)
    assert 0.0 == qubo.offset
    assert 2 == qubo.dimension


def test_qubo_with_offset():
    Q = np.array([[1, 2], [0, 3]])
    qubo = QUBO(Q, 1.0)
    assert np.all(Q == qubo.Q)
    assert 1.0 == qubo.offset
    assert 2 == qubo.dimension


def test_try_define_qubo_with_3d_array():
    with pytest.raises(
        ValueError, match="Expected a 2 dimensional array but got 3 dimensions."
    ):
        QUBO(np.zeros((2, 2, 2)))


def test_try_define_qubo_with_non_quare_array():
    with pytest.raises(ValueError, match="Array must be square."):
        QUBO(np.zeros((2, 3)))


def test_evaulate_qubo():
    Q = np.array([[1, 2], [0, 3]])
    qubo = QUBO(Q, 2)
    binaries = np.array([[0, 0, 1, 1], [0, 1, 0, 1]])
    assert np.all(np.array([2, 5, 3, 8]) == qubo(binaries))


def test_evaluate_qubo_with_non_binary_array():
    Q = np.array([[1, 2], [0, 3]])
    qubo = QUBO(Q)
    array = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    with pytest.raises(ValueError, match="Expected binary values only."):
        qubo(array)
