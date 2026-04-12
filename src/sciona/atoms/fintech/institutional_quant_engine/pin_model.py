from __future__ import annotations

from collections.abc import Sequence

import numpy as np

import icontract
from ageoa.ghost.registry import register_atom
from .pin_model_witnesses import witness_pinlikelihoodevaluation

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_pinlikelihoodevaluation)  # type: ignore[untyped-decorator,name-defined]
@icontract.require(lambda params: params is not None, "params cannot be None")
@icontract.require(lambda B: B is not None, "B cannot be None")
@icontract.require(lambda S: S is not None, "S cannot be None")
@icontract.ensure(lambda result: result is not None, "PinLikelihoodEvaluation output must not be None")
def pinlikelihoodevaluation(
    params: Sequence[float] | np.ndarray,
    B: float | np.ndarray,
    S: float | np.ndarray,
) -> float:
    """Computes the likelihood of observed inputs under the provided parameterization.

    Args:
        params: Input data.
        B: Input data.
        S: Input data.

    Returns:
        Result data.
    """
    # PIN likelihood: params = [alpha, delta, mu, epsilon]
    alpha, delta, mu, epsilon = np.array(params, dtype=float)
    B = np.asarray(B, dtype=float)
    S = np.asarray(S, dtype=float)
    # Expected buys and sells under the model
    expected_B = alpha * delta * mu + epsilon
    expected_S = alpha * (1 - delta) * mu + epsilon
    # Sum of squared errors
    return float(np.sum((B - expected_B) ** 2 + (S - expected_S) ** 2))

import numpy as np

import icontract
from ageoa.ghost.registry import register_atom
from .pin_model_witnesses import witness_pinlikelihoodevaluator


@register_atom(witness_pinlikelihoodevaluator)
@icontract.require(lambda params: isinstance(params, dict), "params must be a dict")
@icontract.require(lambda B: isinstance(B, (float, int, np.number, np.ndarray)), "B must be numeric or an array")
@icontract.require(lambda S: isinstance(S, (float, int, np.number, np.ndarray)), "S must be numeric or an array")
@icontract.ensure(lambda result: isinstance(result, (float, int, np.number, np.floating)), "pinlikelihoodevaluator must return a numeric scalar")
def pinlikelihoodevaluator(params: dict[str, float], B: float | np.ndarray, S: float | np.ndarray) -> float:
    """Evaluates the log-likelihood (or likelihood) of observed data given model parameters and sufficient statistics B and S. This is a stateless, pure oracle computation with no side effects or persistent state.

    Args:
        params: must be valid parameter configuration for the Probability of Informed Trading (PIN) model
        B: buy order counts or volumes; non-negative
        S: sell order counts or volumes; non-negative

    Returns:
        real-valued likelihood score; -inf indicates zero likelihood"""
    alpha = float(params.get("alpha", 0))
    delta = float(params.get("delta", 0))
    mu = float(params.get("mu", 0))
    epsilon = float(params.get("epsilon", 0))
    B = np.asarray(B, dtype=float)
    S = np.asarray(S, dtype=float)
    expected_B = alpha * delta * mu + epsilon
    expected_S = alpha * (1 - delta) * mu + epsilon
    return float(np.sum((B - expected_B) ** 2 + (S - expected_S) ** 2))
