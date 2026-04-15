from __future__ import annotations
"""Stateless atoms for Institutional Quant Engine."""


from typing import Tuple

import icontract

from sciona.ghost.registry import register_atom
from .witnesses import witness_calculate_ofi, witness_execute_passive, witness_execute_pov, witness_execute_vwap
from sciona.atoms.fintech.quant_engine.state_models import LimitQueueState
from sciona.atoms.fintech.quant_engine.witnesses import (
    witness_calculate_ofi,
    witness_execute_passive,
    witness_execute_pov,
    witness_execute_vwap,
)


def _non_negative(value: int) -> int:
    return max(0, int(value))


@register_atom(witness_calculate_ofi)
@icontract.require(lambda bid_qty, ask_qty: bid_qty >= 0 and ask_qty >= 0, "Quantities must be non-negative")
@icontract.ensure(lambda result: result is not None and len(result) == 2, "calculate_ofi must return a (float, state) tuple")
def calculate_ofi(
    bid_px: float,
    bid_qty: int,
    ask_px: float,
    ask_qty: int,
    trade_qty: int,
    state: LimitQueueState,
) -> Tuple[float, LimitQueueState]:
    """Calculate Order Flow Imbalance (OFI), the net directional pressure from competing bid/ask flow levels, and append to state stream.

    Args:
        bid_px: Best bid price.
        bid_qty: Bid quantity (non-negative).
        ask_px: Best ask price.
        ask_qty: Ask quantity (non-negative).
        trade_qty: Trade quantity.
        state: Current LimitQueueState.

    Returns:
        Tuple of (ofi_value, new_state) where ofi_value is the computed
        order flow imbalance and new_state has the updated ofi_stream.
    """
    ofi = float(bid_qty - ask_qty) * 0.5

    current_stream = state.ofi_stream or []
    new_stream = current_stream + [ofi]

    new_state = state.model_copy(update={"ofi_stream": new_stream})
    return ofi, new_state


@register_atom(witness_execute_vwap)
@icontract.require(lambda trade_qty: trade_qty > 0, "Trade quantity must be positive")
@icontract.ensure(lambda result: (result[1].my_qty or 0) >= 0, "Inventory must remain non-negative")
def execute_vwap(trade_qty: int, state: LimitQueueState) -> Tuple[None, LimitQueueState]:
    """Volume-Weighted Average Price (VWAP) execution strategy logic.

    Args:
        trade_qty: Trade quantity (must be positive).
        state: Current LimitQueueState.

    Returns:
        Tuple of (None, new_state) with updated inventory.
    """
    participation_rate = 0.1
    current_qty = _non_negative(state.my_qty or 0)
    fill = min(current_qty, int(trade_qty * participation_rate))
    new_qty = current_qty - fill

    new_state = state.model_copy(update={"my_qty": new_qty})
    return None, new_state


@register_atom(witness_execute_pov)
@icontract.require(lambda trade_qty: trade_qty > 0, "Trade quantity must be positive")
@icontract.ensure(lambda result: (result[1].my_qty or 0) >= 0, "Inventory must remain non-negative")
@icontract.ensure(lambda result: (result[1].orders_ahead or 0) >= 0, "orders_ahead must remain non-negative")
def execute_pov(trade_qty: int, state: LimitQueueState) -> Tuple[None, LimitQueueState]:
    """Percentage of Volume (POV) proportional participation execution strategy logic.

    Args:
        trade_qty: Trade quantity (must be positive).
        state: Current LimitQueueState.

    Returns:
        Tuple of (None, new_state) with updated inventory and queue position.
    """
    orders_ahead = _non_negative(state.orders_ahead or 0)
    my_qty = _non_negative(state.my_qty or 0)

    if orders_ahead > 0:
        filled_against_queue = max(0, trade_qty - orders_ahead)
        orders_ahead = max(0, orders_ahead - trade_qty)
        my_qty = max(0, my_qty - filled_against_queue)
    else:
        my_qty = max(0, my_qty - trade_qty)

    new_state = state.model_copy(update={
        "orders_ahead": orders_ahead,
        "my_qty": my_qty,
    })
    return None, new_state


@register_atom(witness_execute_passive)
@icontract.require(lambda trade_qty: trade_qty > 0, "Trade quantity must be positive")
@icontract.ensure(lambda result: (result[1].my_qty or 0) >= 0, "Inventory must remain non-negative")
@icontract.ensure(lambda result: (result[1].orders_ahead or 0) >= 0, "orders_ahead must remain non-negative")
def execute_passive(trade_qty: int, state: LimitQueueState) -> Tuple[None, LimitQueueState]:
    """Default queue-priority execution logic.

    Args:
        trade_qty: Trade quantity (must be positive).
        state: Current LimitQueueState.

    Returns:
        Tuple of (None, new_state) with updated inventory and queue position.
    """
    orders_ahead = _non_negative(state.orders_ahead or 0)
    my_qty = _non_negative(state.my_qty or 0)

    if orders_ahead > 0:
        orders_ahead = max(0, orders_ahead - trade_qty)
        queue_overflow = max(0, trade_qty - (state.orders_ahead or 0))
        my_qty = max(0, my_qty - queue_overflow)
    else:
        my_qty = max(0, my_qty - trade_qty)

    new_state = state.model_copy(update={
        "orders_ahead": orders_ahead,
        "my_qty": my_qty,
    })
    return None, new_state
