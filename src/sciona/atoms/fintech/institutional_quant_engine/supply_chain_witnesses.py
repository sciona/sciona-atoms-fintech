from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_propagate_supply_shock(
    adjacency: AbstractArray,
    shock_vector: AbstractArray,
) -> AbstractArray:
    """Describe the propagated node-level shock after network diffusion."""
    _ = shock_vector
    result = AbstractArray(
        shape=adjacency.shape,
        dtype="float64",)
    
    return result
