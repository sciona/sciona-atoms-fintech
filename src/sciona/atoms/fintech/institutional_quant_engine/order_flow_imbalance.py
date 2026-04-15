from __future__ import annotations

from collections.abc import Mapping

import numpy as np

import icontract
from sciona.ghost.registry import register_atom
from .order_flow_imbalance_witnesses import witness_orderflowimbalanceevaluation

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_orderflowimbalanceevaluation)  # type: ignore[untyped-decorator, name-defined]
@icontract.require(lambda row: row is not None, "row cannot be None")
@icontract.require(lambda prev_row: prev_row is not None, "prev_row cannot be None")
@icontract.ensure(lambda result: result is not None, "OrderFlowImbalanceEvaluation output must not be None")
def orderflowimbalanceevaluation(row: Mapping[str, float], prev_row: Mapping[str, float]) -> float:
    """Computes the order flow imbalance signal for the current observation relative to the previous observation as a pure, stateless transformation.

Args:
    row: Must contain the fields required for Order Flow Imbalance (OFI) computation.
    prev_row: Represents the immediately preceding row; schema-compatible with row.

Returns:
    Deterministic scalar derived only from row and prev_row."""
    # OFI: track bid/ask price and quantity changes
    row_d = dict(row) if not isinstance(row, dict) else row
    prev_d = dict(prev_row) if not isinstance(prev_row, dict) else prev_row
    bid_p, bid_q = float(row_d.get("bid_price", 0)), float(row_d.get("bid_size", 0))
    prev_bid_p, prev_bid_q = float(prev_d.get("bid_price", 0)), float(prev_d.get("bid_size", 0))
    ask_p, ask_q = float(row_d.get("ask_price", 0)), float(row_d.get("ask_size", 0))
    prev_ask_p, prev_ask_q = float(prev_d.get("ask_price", 0)), float(prev_d.get("ask_size", 0))
    # Buy pressure
    if bid_p > prev_bid_p:
        buy_pressure = bid_q
    elif bid_p == prev_bid_p:
        buy_pressure = bid_q - prev_bid_q
    else:
        buy_pressure = 0.0
    # Sell pressure
    if ask_p < prev_ask_p:
        sell_pressure = ask_q
    elif ask_p == prev_ask_p:
        sell_pressure = ask_q - prev_ask_q
    else:
        sell_pressure = 0.0
    return buy_pressure - sell_pressure
