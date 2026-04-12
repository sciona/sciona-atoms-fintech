from __future__ import annotations

from ageoa.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_compute_hrp_weights(returns: AbstractArray, *args, **kwargs) -> AbstractArray:
    result = AbstractArray(
        shape=returns.shape,
        dtype="float64",)
    
    return result

from ageoa.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_hrppipelinerun(data: AbstractArray) -> AbstractArray:
    """Shape-and-type check for hrp pipeline run. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=data.shape,
        dtype="float64",)
    
    return result
