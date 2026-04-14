from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_compute_hrp_weights(
    returns: AbstractArray,
    covariance: AbstractArray,
) -> AbstractArray:
    """Describe the portfolio-weight vector computed by HRP."""
    _ = covariance
    result = AbstractArray(
        shape=returns.shape,
        dtype="float64",)
    
    return result

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_hrppipelinerun(data: AbstractArray) -> AbstractArray:
    """Shape-and-type check for hrp pipeline run. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=data.shape,
        dtype="float64",)
    
    return result
