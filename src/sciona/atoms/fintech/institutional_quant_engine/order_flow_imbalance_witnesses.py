from __future__ import annotations

from ageoa.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_orderflowimbalanceevaluation(row: AbstractArray, prev_row: AbstractArray) -> AbstractArray:
    """Shape-and-type check for order flow imbalance evaluation. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=row.shape,
        dtype="float64",)
    
    return result
