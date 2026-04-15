from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_fractional_differentiator(series: AbstractArray, d: AbstractScalar, threshold: AbstractScalar) -> AbstractArray:
    """Shape-and-type check for fractional differentiator. Returns output metadata without running the real computation."""
    result = AbstractSignal(
        shape=series.shape,
        dtype="float64",
        sampling_rate=getattr(series, 'sampling_rate', 44100.0),
        domain="time",)
    
    return result
