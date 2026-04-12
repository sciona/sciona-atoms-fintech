from __future__ import annotations
from ageoa.ghost.abstract import AbstractArray, AbstractScalar, AbstractDistribution, AbstractSignal


def witness_execute_pov(trade_qty: AbstractScalar, state: AbstractSignal) -> tuple[None, AbstractSignal]:
    """Shape-and-type check for proportional participation execution. Returns output metadata without running the real computation."""
    return None, state


def witness_execute_passive(trade_qty: AbstractScalar, state: AbstractSignal) -> tuple[None, AbstractSignal]:
    """Shape-and-type check for queue-priority execution. Returns output metadata without running the real computation."""
    return None, state


def witness_calculate_ofi(bid_px: AbstractScalar, bid_qty: AbstractScalar, ask_px: AbstractScalar, ask_qty: AbstractScalar, trade_qty: AbstractScalar, state: AbstractSignal) -> tuple[AbstractScalar, AbstractSignal]:
    """Shape-and-type check for order flow imbalance calculation. Returns output metadata without running the real computation."""
    ofi = AbstractScalar(dtype="float64")
    return ofi, state


def witness_execute_vwap(trade_qty: AbstractScalar, state: AbstractSignal) -> tuple[None, AbstractSignal]:
    """Shape-and-type check for vwap execution. Returns output metadata without running the real computation."""
    return None, state
