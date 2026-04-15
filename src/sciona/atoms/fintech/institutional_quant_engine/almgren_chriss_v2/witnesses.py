from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_riskaversioninit(risk_aversion: AbstractArray) -> AbstractArray:
    """Shape-and-type check for risk aversion init. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=risk_aversion.shape,
        dtype="float64",)
    
    return result

def witness_optimalexecutiontrajectory(risk_aversion: AbstractArray, total_shares: AbstractArray, days: AbstractArray) -> AbstractArray:
    """Shape-and-type check for optimal execution trajectory. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=risk_aversion.shape,
        dtype="float64",)
    
    return result