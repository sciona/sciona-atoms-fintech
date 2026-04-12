"""Deterministic queue-position state transitions."""

from __future__ import annotations

import numpy as np

import icontract
from ageoa.ghost.registry import register_atom

from .state_models import OrderState
from .witnesses import witness_initializeorderstate, witness_updatequeueontrade


def _is_numeric_scalar(value: object) -> bool:
    return isinstance(value, (float, int, np.number))


@register_atom(witness_initializeorderstate)
@icontract.require(lambda my_order_id: isinstance(my_order_id, str) and bool(my_order_id), "my_order_id must be a non-empty string")
@icontract.require(lambda my_qty: _is_numeric_scalar(my_qty) and float(my_qty) >= 0.0, "my_qty must be non-negative")
@icontract.ensure(lambda result: result.my_qty >= 0.0 and result.orders_ahead >= 0.0, "state quantities must remain non-negative")
def initializeorderstate(my_order_id: str, my_qty: float) -> OrderState:
    """Create the initial queue state for a newly submitted order.

    Args:
        my_order_id: Unique identifier for the tracked order.
        my_qty: Remaining quantity resting at this order's price level.

    Returns:
        An immutable ``OrderState`` snapshot for downstream queue updates.
    """

    return OrderState(
        my_order_id=my_order_id,
        my_qty=float(my_qty),
        orders_ahead=10000.0,
        is_filled=float(my_qty) == 0.0,
    )


@register_atom(witness_updatequeueontrade)
@icontract.require(lambda current_order_state: current_order_state is not None, "current_order_state cannot be None")
@icontract.require(lambda trade_qty: _is_numeric_scalar(trade_qty) and float(trade_qty) >= 0.0, "trade_qty must be non-negative")
@icontract.ensure(lambda result: result.my_qty >= 0.0 and result.orders_ahead >= 0.0, "updated state quantities must remain non-negative")
def updatequeueontrade(current_order_state: OrderState, trade_qty: float) -> OrderState:
    """Advance queue state after an executed trade consumes displayed quantity.

    Args:
        current_order_state: Queue state before the trade is applied.
        trade_qty: Executed trade quantity at the tracked order's price level.

    Returns:
        The next immutable ``OrderState`` after consuming queue-ahead volume and,
        if necessary, filling this order with any remaining traded quantity.
    """

    traded = float(trade_qty)
    ahead_before = float(current_order_state.orders_ahead)
    qty_before = float(current_order_state.my_qty)

    consumed_ahead = min(ahead_before, traded)
    remaining_trade = traded - consumed_ahead
    next_orders_ahead = ahead_before - consumed_ahead
    next_my_qty = max(qty_before - remaining_trade, 0.0)

    return OrderState(
        my_order_id=current_order_state.my_order_id,
        my_qty=next_my_qty,
        orders_ahead=next_orders_ahead,
        is_filled=current_order_state.is_filled or next_my_qty == 0.0,
    )
