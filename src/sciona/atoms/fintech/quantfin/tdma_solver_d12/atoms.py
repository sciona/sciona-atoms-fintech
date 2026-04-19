from __future__ import annotations

"""Source-aligned atoms for quantfin tridiagonal utilities."""

from collections.abc import Callable, Sequence
import math

import icontract

from sciona.ghost.registry import register_atom

from .witnesses import witness_cotraverse_vec, witness_tdma_solver


ScalarVector = Sequence[float]
VectorContainer = Sequence[ScalarVector]
SliceAggregator = Callable[[Sequence[float]], float]


def _is_non_empty_numeric_vector(values: ScalarVector) -> bool:
    return len(values) > 0 and all(math.isfinite(float(value)) for value in values)


def _same_length_vectors(*vectors: ScalarVector) -> bool:
    if not vectors:
        return False
    size = len(vectors[0])
    return all(len(vector) == size for vector in vectors)


@register_atom(witness_tdma_solver)
@icontract.require(lambda sub_diagonal: _is_non_empty_numeric_vector(sub_diagonal), "sub_diagonal must be a non-empty finite vector")
@icontract.require(lambda diagonal: _is_non_empty_numeric_vector(diagonal), "diagonal must be a non-empty finite vector")
@icontract.require(lambda super_diagonal: _is_non_empty_numeric_vector(super_diagonal), "super_diagonal must be a non-empty finite vector")
@icontract.require(lambda rhs: _is_non_empty_numeric_vector(rhs), "rhs must be a non-empty finite vector")
@icontract.require(
    lambda sub_diagonal, diagonal, super_diagonal, rhs: _same_length_vectors(
        sub_diagonal,
        diagonal,
        super_diagonal,
        rhs,
    ),
    "all coefficient and right-hand-side vectors must have equal length",
)
@icontract.ensure(lambda result, diagonal: len(result) == len(diagonal), "solution length must match the system size")
@icontract.ensure(lambda result: all(math.isfinite(value) for value in result), "solution entries must be finite")
def tdma_solver(
    sub_diagonal: ScalarVector,
    diagonal: ScalarVector,
    super_diagonal: ScalarVector,
    rhs: ScalarVector,
) -> list[float]:
    """Solve a tridiagonal linear system with the Thomas algorithm.

    This mirrors quantfin's `tdmaSolver aL bL cL dL`: the four inputs are the
    sub-diagonal, main diagonal, super-diagonal, and right-hand-side vectors.
    The first sub-diagonal element and final super-diagonal element are retained
    for source-shape parity but are not used by the tridiagonal solve.
    """
    n = len(diagonal)
    c_prime = [0.0] * n
    d_prime = [0.0] * n

    first_pivot = float(diagonal[0])
    if first_pivot == 0.0:
        raise ValueError("tridiagonal system has a zero first pivot")

    c_prime[0] = float(super_diagonal[0]) / first_pivot
    d_prime[0] = float(rhs[0]) / first_pivot

    for index in range(1, n):
        pivot = float(diagonal[index]) - float(sub_diagonal[index]) * c_prime[index - 1]
        if pivot == 0.0:
            raise ValueError(f"tridiagonal system has a zero pivot at index {index}")
        c_prime[index] = float(super_diagonal[index]) / pivot
        d_prime[index] = (float(rhs[index]) - float(sub_diagonal[index]) * d_prime[index - 1]) / pivot

    solution = [0.0] * n
    solution[-1] = d_prime[-1]
    for index in range(n - 2, -1, -1):
        solution[index] = d_prime[index] - c_prime[index] * solution[index + 1]

    return solution


def _vectors_cover_length(vectors: VectorContainer, length: int) -> bool:
    return len(vectors) > 0 and all(len(vector) >= length for vector in vectors)


@register_atom(witness_cotraverse_vec)
@icontract.require(lambda aggregator: callable(aggregator), "aggregator must be callable")
@icontract.require(lambda length: isinstance(length, int) and length > 0, "length must be a positive integer")
@icontract.require(lambda vectors, length: _vectors_cover_length(vectors, length), "each input vector must cover the requested length")
@icontract.ensure(lambda result, length: len(result) == length, "result length must match the requested output length")
@icontract.ensure(lambda result: all(math.isfinite(value) for value in result), "aggregated entries must be finite")
def cotraverse_vec(
    aggregator: SliceAggregator,
    length: int,
    vectors: VectorContainer,
) -> list[float]:
    """Aggregate index-aligned slices across a container of vectors.

    This mirrors quantfin's `cotraverseVec f l m`: for each output index in
    `0..length-1`, collect that index from every vector in `vectors`, apply
    `aggregator` to the slice, and return the resulting vector.
    """
    return [
        float(aggregator([float(vector[index]) for vector in vectors]))
        for index in range(length)
    ]
