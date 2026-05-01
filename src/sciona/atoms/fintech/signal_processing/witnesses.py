"""Ghost witnesses for fintech signal processing atoms."""

from __future__ import annotations

from sciona.ghost.abstract import AbstractArray


def witness_alpha_isolation(
    stock_return: AbstractArray,
    market_return: AbstractArray,
) -> AbstractArray:
    """Ghost witness for alpha isolation."""
    return AbstractArray(shape=stock_return.shape, dtype="float64")


def witness_temporal_date_alignment(
    timestamps: AbstractArray,
    cutoff_hour: int = 22,
) -> AbstractArray:
    """Ghost witness for temporal date alignment."""
    return AbstractArray(shape=timestamps.shape, dtype="float64")
