from __future__ import annotations
from typing import Any, Callable
"""Auto-generated atom wrappers following the sciona pattern."""


import numpy as np

import icontract
from sciona.ghost.registry import register_atom


from .witnesses import witness_computeinventoryadjustedquotes, witness_initializemarketmakerstate

@register_atom(witness_initializemarketmakerstate)
@icontract.require(lambda inventory: isinstance(inventory, (float, int, np.number)), "inventory must be numeric")
@icontract.ensure(lambda result: result is not None, "InitializeMarketMakerState output must not be None")
def initializemarketmakerstate(s0: float, inventory: float) -> dict[str, float]:
    """Construct the immutable market-making state object with model parameters and initial market/inventory values.

    Args:
        s0: Initial reference/mid price.
        inventory: Initial inventory position.

    Returns:
        Immutable state; contains all persistent fields previously stored on self.
    """
    return {"s": s0, "q": inventory, "sigma": 0.02, "gamma": 0.1, "k": 1.5, "T": 1.0, "t": 0.0}

@register_atom(witness_computeinventoryadjustedquotes)
@icontract.require(lambda state_model: isinstance(state_model, dict), "state_model must be a dict")
@icontract.ensure(lambda result: result is not None, "ComputeInventoryAdjustedQuotes output must not be None")
def computeinventoryadjustedquotes(state_model: dict[str, float]) -> dict[str, float]:
    """Compute inventory-adjusted quotes from the state model.

    Args:
        state_model: Read-only input state.

    Returns:
        Pure arithmetic output derived from state_model.
    """
    import math
    s = state_model["s"]
    q = state_model["q"]
    sigma = state_model["sigma"]
    gamma = state_model["gamma"]
    k = state_model["k"]
    T = state_model.get("T", 1.0)
    t = state_model.get("t", 0.0)
    # Reservation price adjusted for inventory
    reservation_price = s - q * gamma * (sigma ** 2) * (T - t)
    # Optimal spread
    spread = gamma * (sigma ** 2) * (T - t) + (2.0 / gamma) * math.log(1 + gamma / k)
    bid = reservation_price - spread / 2.0
    ask = reservation_price + spread / 2.0
    return {"reservation_price": reservation_price, "bid": bid, "ask": ask, "spread": spread}