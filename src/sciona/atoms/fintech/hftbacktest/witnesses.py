from __future__ import annotations

from sciona.ghost.abstract import AbstractScalar


def witness_initialize_glft_state() -> tuple[AbstractScalar, AbstractScalar]:
    """Return scalar metadata for the initial GLFT coefficient state."""
    return AbstractScalar(dtype="float64"), AbstractScalar(dtype="float64")


def witness_update_glft_coefficients(
    last_c1: AbstractScalar,
    last_c2: AbstractScalar,
    xi: AbstractScalar,
    gamma: AbstractScalar,
    delta: AbstractScalar,
    A: AbstractScalar,
    k: AbstractScalar,
) -> tuple[AbstractScalar, AbstractScalar]:
    """Return scalar metadata for the GLFT coefficient update."""
    _ = last_c1, last_c2, xi, gamma, delta, A, k
    return (
        AbstractScalar(dtype="float64", min_val=0.0),
        AbstractScalar(dtype="float64", min_val=0.0),
    )


def witness_evaluate_spread_conditions(
    c1: AbstractScalar,
    c2: AbstractScalar,
    delta: AbstractScalar,
    volatility: AbstractScalar,
    adj1: AbstractScalar,
    threshold: AbstractScalar,
) -> tuple[AbstractScalar, AbstractScalar]:
    """Return scalar metadata for the half-spread computation and ratio gate."""
    _ = c1, c2, delta, volatility, adj1, threshold
    return AbstractScalar(dtype="float64"), AbstractScalar(dtype="bool")
