from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractScalar, AbstractDistribution, AbstractSignal


def witness_functional_monte_carlo(data: AbstractArray) -> AbstractArray:
    """Shape-and-type check for functional monte carlo. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=data.shape,
        dtype="float64",
    )
    return result


def witness_volatility_surface_modeling(data: AbstractArray) -> AbstractArray:
    """Shape-and-type check for volatility surface modeling. Returns output metadata without running the real computation."""
    return AbstractArray(shape=data.shape, dtype=data.dtype)


def witness_run_simulation(
    model: object,
    claim: object,
    seed: int,
    trials: int,
    anti: bool,
    simulator_name: str,
) -> AbstractScalar:
    """Witness for run_simulation.

    Validates that trials is positive and seed is non-negative,
    then returns an AbstractScalar representing the simulation result.
    """
    if trials <= 0:
        raise ValueError(f"trials must be positive, got {trials}")
    if seed < 0:
        raise ValueError(f"seed must be non-negative, got {seed}")
    return AbstractScalar(dtype="float64")


def witness_run_simulation_anti(
    model: object,
    claim: object,
    seed: int,
    trials: int,
    simulator_name: str,
) -> AbstractScalar:
    """Witness for run_simulation_anti.

    Validates that trials is positive and even, and seed is non-negative,
    then returns an AbstractScalar representing the antithetic simulation result.
    """
    if trials <= 0:
        raise ValueError(f"trials must be positive, got {trials}")
    if trials % 2 != 0:
        raise ValueError(f"trials must be even for antithetic variates, got {trials}")
    if seed < 0:
        raise ValueError(f"seed must be non-negative, got {seed}")
    return AbstractScalar(dtype="float64")


def witness_quick_sim_anti(
    model: object,
    claim: object,
    trials: int,
    simulator_name: str,
) -> AbstractScalar:
    """Witness for quick_sim_anti.

    Validates that trials is positive and even,
    then returns an AbstractScalar representing the simulation result.
    """
    if trials <= 0:
        raise ValueError(f"trials must be positive, got {trials}")
    if trials % 2 != 0:
        raise ValueError(f"trials must be even for antithetic variates, got {trials}")
    return AbstractScalar(dtype="float64")
