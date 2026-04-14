from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_fit_gpd_tail(
    returns: AbstractArray,
    threshold: AbstractArray,
) -> AbstractArray:
    """Describe the fitted tail-parameter vector from EVT thresholding."""
    _ = threshold
    result = AbstractArray(
        shape=returns.shape,
        dtype="float64",)
    
    return result
