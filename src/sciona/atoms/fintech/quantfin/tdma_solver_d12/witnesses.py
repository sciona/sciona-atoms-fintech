from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractScalar


def witness_tdma_solver(
    sub_diagonal: AbstractArray,
    diagonal: AbstractArray,
    super_diagonal: AbstractArray,
    rhs: AbstractArray,
) -> AbstractArray:
    """Return solution-vector metadata for a tridiagonal system solve."""
    del sub_diagonal, super_diagonal, rhs
    return AbstractArray(shape=diagonal.shape, dtype="float64")


def witness_cotraverse_vec(
    aggregator: AbstractScalar,
    length: AbstractScalar,
    vectors: AbstractArray,
) -> AbstractArray:
    """Return output-vector metadata for index-wise vector co-traversal."""
    del aggregator, length
    return AbstractArray(shape=vectors.shape[:1], dtype="float64")
