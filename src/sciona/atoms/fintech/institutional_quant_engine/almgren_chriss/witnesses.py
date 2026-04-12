from __future__ import annotations

from ageoa.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_computeoptimaltrajectory(
    total_shares: AbstractScalar, days: AbstractScalar, risk_aversion: AbstractScalar
) -> AbstractArray:
    """Shape-and-type check for compute optimal trajectory. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=total_shares.shape,
        dtype="float64",
    )

    return result
