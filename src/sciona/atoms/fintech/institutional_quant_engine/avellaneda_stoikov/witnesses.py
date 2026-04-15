from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal

def witness_initializemarketmakerstate(s0: AbstractScalar, inventory: AbstractScalar) -> AbstractArray:
    """Shape-and-type check for initialize market maker state. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=s0.shape,
        dtype="float64",)
    
    return result

def witness_computeinventoryadjustedquotes(state_model: AbstractArray) -> AbstractArray:
    """Shape-and-type check for compute inventory adjusted quotes. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=state_model.shape,
        dtype="float64",)
    
    return result