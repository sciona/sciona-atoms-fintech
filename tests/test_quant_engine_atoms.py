from __future__ import annotations

import pytest
from icontract.errors import ViolationError

from sciona.atoms.fintech.quant_engine.atoms import (
    calculate_ofi,
    execute_passive,
    execute_pov,
    execute_vwap,
)
from sciona.atoms.fintech.quant_engine.state_models import LimitQueueState
from sciona.atoms.fintech.quant_engine.witnesses import (
    witness_calculate_ofi,
    witness_execute_passive,
    witness_execute_pov,
    witness_execute_vwap,
)
from sciona.ghost.abstract import AbstractScalar


def test_calculate_ofi_appends_ofi_value_to_state_stream() -> None:
    state = LimitQueueState(orders_ahead=5, my_qty=10, ofi_stream=[-1.0])

    ofi, next_state = calculate_ofi(
        bid_px=100.0,
        bid_qty=12,
        ask_px=101.0,
        ask_qty=8,
        trade_qty=3,
        state=state,
    )

    assert ofi == pytest.approx(2.0)
    assert next_state.ofi_stream == [-1.0, 2.0]
    assert next_state.orders_ahead == 5
    assert next_state.my_qty == 10


def test_calculate_ofi_rejects_negative_book_quantities() -> None:
    state = LimitQueueState(ofi_stream=[])

    with pytest.raises(ViolationError, match="Quantities must be non-negative"):
        calculate_ofi(100.0, -1, 101.0, 8, 3, state)


def test_execute_vwap_reduces_inventory_by_ten_percent_of_trade_qty() -> None:
    _, next_state = execute_vwap(trade_qty=40, state=LimitQueueState(my_qty=9))

    assert next_state.my_qty == 5


def test_execute_pov_consumes_queue_before_inventory() -> None:
    _, next_state = execute_pov(
        trade_qty=7,
        state=LimitQueueState(orders_ahead=5, my_qty=10),
    )

    assert next_state.orders_ahead == 0
    assert next_state.my_qty == 8


def test_execute_passive_consumes_queue_before_overflowing_into_inventory() -> None:
    _, next_state = execute_passive(
        trade_qty=7,
        state=LimitQueueState(orders_ahead=5, my_qty=10),
    )

    assert next_state.orders_ahead == 0
    assert next_state.my_qty == 8


def test_execution_atoms_reject_non_positive_trade_qty() -> None:
    state = LimitQueueState(orders_ahead=1, my_qty=1)

    for atom in (execute_vwap, execute_pov, execute_passive):
        with pytest.raises(ViolationError, match="Trade quantity must be positive"):
            atom(0, state)


def test_quant_engine_witnesses_preserve_state_metadata_shape() -> None:
    trade_qty = AbstractScalar(dtype="int64")
    price = AbstractScalar(dtype="float64")
    state = object()

    ofi, next_state = witness_calculate_ofi(price, trade_qty, price, trade_qty, trade_qty, state)
    _, pov_state = witness_execute_pov(trade_qty, state)
    _, passive_state = witness_execute_passive(trade_qty, state)
    _, vwap_state = witness_execute_vwap(trade_qty, state)

    assert isinstance(ofi, AbstractScalar)
    assert ofi.dtype == "float64"
    assert next_state is state
    assert pov_state is state
    assert passive_state is state
    assert vwap_state is state
