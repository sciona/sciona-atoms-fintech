from __future__ import annotations

import math

import pytest
from icontract.errors import ViolationError

from sciona.atoms.fintech.hftbacktest.atoms import (
    evaluate_spread_conditions,
    initialize_glft_state,
    update_glft_coefficients,
)
from sciona.atoms.fintech.hftbacktest.witnesses import (
    witness_evaluate_spread_conditions,
    witness_initialize_glft_state,
    witness_update_glft_coefficients,
)
from sciona.ghost.abstract import AbstractScalar


def test_initialize_glft_state_returns_zeroed_coefficients() -> None:
    assert initialize_glft_state() == (0.0, 0.0)
    assert initialize_glft_state(None) == (0.0, 0.0)


def test_initialize_glft_state_rejects_non_none_trigger() -> None:
    with pytest.raises(ViolationError, match="_trigger must be None"):
        initialize_glft_state("unexpected")  # type: ignore[arg-type]


def test_update_glft_coefficients_matches_vendored_hftbacktest_formula() -> None:
    xi = 0.25
    gamma = 0.1
    delta = 1.5
    A = 2.0
    k = 0.4

    c1, c2 = update_glft_coefficients(7.0, 11.0, xi, gamma, delta, A, k)

    xi_delta = xi * delta
    expected_c1 = (1.0 / xi_delta) * math.log(1.0 + xi_delta / k)
    expected_c2 = math.sqrt(
        gamma / (2.0 * A * delta * k) * (1.0 + xi_delta / k) ** (k / xi_delta + 1.0)
    )

    assert c1 == pytest.approx(expected_c1)
    assert c2 == pytest.approx(expected_c2)


def test_update_glft_coefficients_rejects_non_positive_parameters() -> None:
    with pytest.raises(ViolationError, match="xi must be > 0"):
        update_glft_coefficients(0.0, 0.0, 0.0, 0.1, 1.0, 2.0, 0.4)


def test_evaluate_spread_conditions_matches_vendored_hftbacktest_formula() -> None:
    half_spread, is_valid = evaluate_spread_conditions(
        c1=0.4,
        c2=1.2,
        delta=2.0,
        volatility=0.5,
        adj1=0.75,
        threshold=2.0,
    )

    expected_half_spread = (0.4 + (2.0 / 2.0) * 1.2 * 0.5) * 0.75
    assert half_spread == pytest.approx(expected_half_spread)
    assert is_valid is ((expected_half_spread / 0.4) < 2.0)


def test_evaluate_spread_conditions_preserves_signed_ratio_heuristic() -> None:
    half_spread, is_valid = evaluate_spread_conditions(
        c1=-1.0,
        c2=2.0,
        delta=2.0,
        volatility=1.0,
        adj1=1.0,
        threshold=0.5,
    )

    assert half_spread == pytest.approx(1.0)
    assert is_valid is True


def test_hftbacktest_witnesses_return_scalar_tuple_metadata() -> None:
    init_c1, init_c2 = witness_initialize_glft_state()
    next_c1, next_c2 = witness_update_glft_coefficients(*([AbstractScalar(dtype="float64")] * 7))
    half_spread, is_valid = witness_evaluate_spread_conditions(
        *([AbstractScalar(dtype="float64")] * 6)
    )

    assert isinstance(init_c1, AbstractScalar)
    assert isinstance(init_c2, AbstractScalar)
    assert isinstance(next_c1, AbstractScalar)
    assert isinstance(next_c2, AbstractScalar)
    assert isinstance(half_spread, AbstractScalar)
    assert isinstance(is_valid, AbstractScalar)
    assert is_valid.dtype == "bool"
