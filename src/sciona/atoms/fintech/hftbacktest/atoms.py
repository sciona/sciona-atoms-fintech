"""Auto-generated atom wrappers following the ageoa pattern."""

from __future__ import annotations

import numpy as np

import icontract
from ageoa.ghost.registry import register_atom


from .witnesses import (
    witness_initialize_glft_state,
    witness_update_glft_coefficients,
    witness_evaluate_spread_conditions,
)
@register_atom(witness_initialize_glft_state)
@icontract.require(lambda: True, "no preconditions for zero-parameter initializer")
@icontract.ensure(lambda result: all(r is not None for r in result), "initialize_glft_state all outputs must not be None")
def initialize_glft_state() -> tuple[float, float]:
    """Initializes the state for the Gueant-Lehalle-Fernandez-Tapia (GLFT) High-Frequency Trading (HFT) market-making model coefficients.

    Returns:
        initial_c1: Initial value of the first state variable.
        initial_c2: Initial value of the second state variable.
    """
    return (0.0, 0.0)

@register_atom(witness_update_glft_coefficients)
@icontract.require(lambda last_c1: isinstance(last_c1, (float, int, np.number)), "last_c1 must be numeric")
@icontract.require(lambda last_c2: isinstance(last_c2, (float, int, np.number)), "last_c2 must be numeric")
@icontract.require(lambda xi: isinstance(xi, (float, int, np.number)), "xi must be numeric")
@icontract.require(lambda gamma: isinstance(gamma, (float, int, np.number)), "gamma must be numeric")
@icontract.require(lambda delta: isinstance(delta, (float, int, np.number)), "delta must be numeric")
@icontract.require(lambda A: isinstance(A, (float, int, np.number)), "A must be numeric")
@icontract.require(lambda k: isinstance(k, (float, int, np.number)), "k must be numeric")
@icontract.ensure(lambda result: all(r is not None for r in result), "update_glft_coefficients all outputs must not be None")
def update_glft_coefficients(last_c1: float, last_c2: float, xi: float, gamma: float, delta: float, A: float, k: float) -> tuple[float, float]:
    """Updates the Gueant-Lehalle-Fernandez-Tapia (GLFT) model coefficients based on market parameters and the previous state.

    Args:
        last_c1: The previous state of the 'c1' coefficient.
        last_c2: The previous state of the 'c2' coefficient.
        xi: Risk aversion parameter; must be > 0.
        gamma: Inventory risk parameter; must be > 0.
        delta: Order size; must be > 0.
        A: Trading intensity parameter A; must be > 0.
        k: Trading intensity parameter k; must be > 0.

    Returns:
        next_c1: The updated state of the 'c1' coefficient.
        next_c2: The updated state of the 'c2' coefficient.
    """
    # GLFT coefficient update: c1 = γσ²/2k, c2 = (1/k)ln(1 + k/A)
    import math
    c1 = gamma * (xi ** 2) / (2.0 * k)
    c2 = (1.0 / k) * math.log(1.0 + k / A)
    return (c1, c2)

@register_atom(witness_evaluate_spread_conditions)
@icontract.require(lambda c1: isinstance(c1, (float, int, np.number)), "c1 must be numeric")
@icontract.require(lambda c2: isinstance(c2, (float, int, np.number)), "c2 must be numeric")
@icontract.require(lambda delta: isinstance(delta, (float, int, np.number)), "delta must be numeric")
@icontract.require(lambda volatility: isinstance(volatility, (float, int, np.number)), "volatility must be numeric")
@icontract.require(lambda adj1: isinstance(adj1, (float, int, np.number)), "adj1 must be numeric")
@icontract.require(lambda threshold: isinstance(threshold, (float, int, np.number)), "threshold must be numeric")
@icontract.ensure(lambda result: all(r is not None for r in result), "evaluate_spread_conditions all outputs must not be None")
def evaluate_spread_conditions(c1: float, c2: float, delta: float, volatility: float, adj1: float, threshold: float) -> tuple[float, bool]:
    """Computes the half-spread from the current state and checks if it meets a validity condition against the c1 coefficient.

    Args:
        c1: Current value of the 'c1' coefficient.
        c2: Current value of the 'c2' coefficient.
        delta: Order size; must be > 0.
        volatility: Market volatility (sigma); must be >= 0.
        adj1: Adjustment factor for half spread.
        threshold: Ratio threshold for validity check; must be > 0.

    Returns:
        half_spread: Computed half-spread value.
        is_valid_ratio: True if half_spread / c1 ratio is within the threshold.
    """
    half_spread = c2 + delta * volatility * adj1
    is_valid = abs(half_spread / c1) <= threshold if c1 != 0 else False
    return (half_spread, is_valid)