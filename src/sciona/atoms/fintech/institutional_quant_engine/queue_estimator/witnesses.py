"""Ghost witnesses for queue estimator atoms."""

from __future__ import annotations

from ageoa.ghost.abstract import AbstractArray, AbstractScalar


def witness_initializeorderstate(
    my_order_id: AbstractScalar,
    my_qty: AbstractScalar,
) -> AbstractArray:
    """Initialization produces a small fixed-shape queue state record."""

    return AbstractArray(shape=(3,), dtype="float64")


def witness_updatequeueontrade(
    current_order_state: AbstractArray,
    trade_qty: AbstractScalar,
) -> AbstractArray:
    """Queue updates preserve the compact queue-state record shape."""

    return AbstractArray(shape=current_order_state.shape, dtype="float64")
