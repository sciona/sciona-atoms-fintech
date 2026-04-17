"""Provider-reviewed GLFT hftbacktest atom wrappers."""

from __future__ import annotations

import math

import numpy as np

import icontract
from sciona.ghost.registry import register_atom

from .witnesses import (
    witness_evaluate_spread_conditions,
    witness_initialize_glft_state,
    witness_update_glft_coefficients,
)


def _is_finite_real(value: object) -> bool:
    return (
        isinstance(value, (float, int, np.number))
        and not isinstance(value, bool)
        and bool(np.isfinite(value))
    )


def _is_positive_real(value: object) -> bool:
    return _is_finite_real(value) and float(value) > 0.0


def _is_non_negative_real(value: object) -> bool:
    return _is_finite_real(value) and float(value) >= 0.0


@register_atom(witness_initialize_glft_state)
@icontract.require(
    lambda _trigger: _trigger is None,
    "_trigger must be None for the state initializer sentinel",
)
@icontract.ensure(
    lambda result: len(result) == 2 and all(_is_finite_real(r) for r in result),
    "initialize_glft_state must return two finite coefficients",
)
def initialize_glft_state(_trigger: None = None) -> tuple[float, float]:
    """Initialize the GLFT coefficient state.

    Args:
        _trigger: Optional sentinel input used to align the callable signature
            with the audited zero-parameter CDG entry.

    Returns:
        The initial `(c1, c2)` state used before the first closed-form update.
    """
    return (0.0, 0.0)


@register_atom(witness_update_glft_coefficients)
@icontract.require(lambda last_c1: _is_finite_real(last_c1), "last_c1 must be finite")
@icontract.require(lambda last_c2: _is_finite_real(last_c2), "last_c2 must be finite")
@icontract.require(lambda xi: _is_positive_real(xi), "xi must be > 0")
@icontract.require(lambda gamma: _is_positive_real(gamma), "gamma must be > 0")
@icontract.require(lambda delta: _is_positive_real(delta), "delta must be > 0")
@icontract.require(lambda A: _is_positive_real(A), "A must be > 0")
@icontract.require(lambda k: _is_positive_real(k), "k must be > 0")
@icontract.ensure(
    lambda result: len(result) == 2 and all(_is_finite_real(r) and float(r) > 0.0 for r in result),
    "update_glft_coefficients must return two positive finite coefficients",
)
def update_glft_coefficients(
    last_c1: float,
    last_c2: float,
    xi: float,
    gamma: float,
    delta: float,
    A: float,
    k: float,
) -> tuple[float, float]:
    """Recompute the GLFT coefficients from the current model parameters.

    The upstream `hftbacktest_glft.py` closed-form update does not consume the
    previous coefficient values, but the parameters remain in the public
    signature for pipeline compatibility.
    """
    _ = last_c1, last_c2
    xi_delta = xi * delta
    base = 1.0 + xi_delta / k
    c1 = (1.0 / xi_delta) * math.log(base)
    c2 = math.sqrt(gamma / (2.0 * A * delta * k) * (base ** (k / xi_delta + 1.0)))
    return (c1, c2)


@register_atom(witness_evaluate_spread_conditions)
@icontract.require(lambda c1: _is_finite_real(c1), "c1 must be finite")
@icontract.require(lambda c2: _is_finite_real(c2), "c2 must be finite")
@icontract.require(lambda delta: _is_positive_real(delta), "delta must be > 0")
@icontract.require(lambda volatility: _is_non_negative_real(volatility), "volatility must be >= 0")
@icontract.require(lambda adj1: _is_finite_real(adj1), "adj1 must be finite")
@icontract.require(lambda threshold: _is_positive_real(threshold), "threshold must be > 0")
@icontract.ensure(
    lambda result: len(result) == 2 and _is_finite_real(result[0]) and isinstance(result[1], bool),
    "evaluate_spread_conditions must return a finite half-spread and boolean flag",
)
def evaluate_spread_conditions(c1: float, c2: float, delta: float, volatility: float, adj1: float, threshold: float) -> tuple[float, bool]:
    """Compute the GLFT half-spread and apply the upstream ratio heuristic."""
    half_spread = (c1 + (delta / 2.0) * c2 * volatility) * adj1
    is_valid = False if c1 == 0 else (half_spread / c1) < threshold
    return (half_spread, is_valid)
