from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractScalar

def witness_fractional_differentiator(series: AbstractArray, d: AbstractScalar, threshold: AbstractScalar) -> AbstractArray:
    """Shape-and-type check for fractional differentiator. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=series.shape,
        dtype="float64",
    )
    
    return result
