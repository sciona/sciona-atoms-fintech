from __future__ import annotations
"""Auto-generated atom wrappers following the sciona pattern."""

import numpy as np

import icontract
from sciona.ghost.registry import register_atom
from .witnesses import witness_marketmakerstateinit, witness_optimalquotecalculation


@register_atom(witness_marketmakerstateinit)
@icontract.require(lambda s0: isinstance(s0, (float, int, np.number)), "s0 must be numeric")
@icontract.require(lambda s0: s0 > 0, "s0 must be positive")
@icontract.require(lambda inventory: isinstance(inventory, (float, int, np.number)), "inventory must be numeric")
@icontract.ensure(lambda result: all(r is not None for r in result), "MarketMakerStateInit all outputs must not be None")
def marketmakerstateinit(s0: float, inventory: float) -> tuple[float, float, float, float, float]:
    """Bootstraps the market-maker's immutable parameter state from a supplied initial mid-price and inventory position, materialising the five scalar fields - risk-aversion (gamma), market-depth (k), inventory (q), mid-price (s), and volatility (sigma) - that all downstream computations consume as pure inputs.

    Args:
        s0: initial mid-price; must be > 0
        inventory: current inventory position; may be negative (short)

    Returns:
        gamma: risk-aversion coefficient; gamma > 0
        k: market-depth parameter; k > 0
        q: inventory level
        s: mid-price; s > 0
        sigma: volatility estimate; sigma > 0
    """
    gamma = 0.1
    k = 1.5
    sigma = 0.02
    return (gamma, k, inventory, s0, sigma)


@register_atom(witness_optimalquotecalculation)
@icontract.require(lambda gamma: isinstance(gamma, (float, int, np.number)), "gamma must be numeric")
@icontract.require(lambda k: isinstance(k, (float, int, np.number)), "k must be numeric")
@icontract.require(lambda q: isinstance(q, (float, int, np.number)), "q must be numeric")
@icontract.require(lambda s: isinstance(s, (float, int, np.number)), "s must be numeric")
@icontract.require(lambda sigma: isinstance(sigma, (float, int, np.number)), "sigma must be numeric")
@icontract.ensure(lambda result: all(r is not None for r in result), "OptimalQuoteCalculation all outputs must not be None")
def optimalquotecalculation(gamma: float, k: float, q: float, s: float, sigma: float) -> tuple[float, float, float, float]:
    """Computes optimal bid and ask quotes using the Avellaneda-Stoikov market-making framework, deriving a reservation price and optimal spread from the current inventory, volatility, and market-depth parameters.

    Args:
        gamma: risk-aversion coefficient; gamma > 0
        k: market-depth parameter; k > 0
        q: current inventory position
        s: current mid-price; s > 0
        sigma: volatility estimate; sigma > 0

    Returns:
        bid_price: optimal bid; bid_price < s when q > 0
        ask_price: optimal ask; ask_price > s when q > 0
        reservation_price: indifference price adjusted for inventory risk
        optimal_spread: distance between ask and bid; optimal_spread > 0
    """
    import math
    reservation_price = s - q * gamma * (sigma ** 2)
    spread = gamma * (sigma ** 2) + (2.0 / gamma) * math.log(1 + gamma / k)
    bid_price = reservation_price - spread / 2.0
    ask_price = reservation_price + spread / 2.0
    return (bid_price, ask_price, reservation_price, spread)
