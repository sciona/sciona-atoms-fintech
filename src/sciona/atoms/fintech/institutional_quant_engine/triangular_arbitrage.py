from __future__ import annotations

import numpy as np
import icontract
from sciona.ghost.registry import register_atom
from .triangular_arbitrage_witnesses import witness_detect_triangular_arbitrage


@register_atom(witness_detect_triangular_arbitrage)
@icontract.require(lambda rates: rates.ndim >= 1, "rates must have at least one dimension")
@icontract.require(lambda rates: rates is not None, "rates cannot be None")
@icontract.require(lambda rates: isinstance(rates, np.ndarray), "rates must be np.ndarray")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def detect_triangular_arbitrage(rates: np.ndarray) -> np.ndarray:
    """Detects triangular arbitrage opportunities in a Foreign Exchange (FX) rate matrix by searching for negative-weight cycles in the log-rate graph.

    Args:
        rates: Exchange rate matrix, shape (n_currencies, n_currencies), where rates[i,j] is the rate from currency i to j

    Returns:
        Array of cycle profit factors; values > 1.0 indicate arbitrage opportunities
    """
    n = rates.shape[0]
    log_rates = -np.log(rates + 1e-15)
    # Find all 3-node cycles and compute profit factors
    profits = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for k in range(n):
                if k == i or k == j:
                    continue
                cycle_profit = rates[i, j] * rates[j, k] * rates[k, i]
                if cycle_profit > 1.0:
                    profits.append(cycle_profit)
    return np.array(profits) if profits else np.array([])
