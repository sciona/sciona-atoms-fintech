"""Fintech signal processing primitives in pure numpy.

Implements reusable signal transforms for quantitative finance pipelines:
alpha isolation via market-neutral returns and temporal date alignment
to prevent future data leakage from after-hours events.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

import icontract
from sciona.ghost.registry import register_atom

from .witnesses import (
    witness_alpha_isolation,
    witness_temporal_date_alignment,
)


@register_atom(witness_alpha_isolation)
@icontract.require(
    lambda stock_return, market_return: stock_return.shape == market_return.shape,
    "stock_return and market_return must have the same shape",
)
@icontract.require(
    lambda stock_return: stock_return.ndim == 1,
    "stock_return must be 1-D",
)
@icontract.ensure(
    lambda result, stock_return: result.shape == stock_return.shape,
    "result must preserve shape",
)
@icontract.ensure(lambda result: np.all(np.isfinite(result)), "alpha must be finite")
def alpha_isolation(
    stock_return: NDArray[np.float64],
    market_return: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Isolate stock-specific alpha by subtracting market index return.

    Produces market-neutral returns by removing the systematic market
    component, leaving only the stock-specific alpha signal.
    """
    return stock_return - market_return


@register_atom(witness_temporal_date_alignment)
@icontract.require(
    lambda timestamps: timestamps.ndim == 1,
    "timestamps must be 1-D",
)
@icontract.require(
    lambda cutoff_hour: 0 <= cutoff_hour <= 23,
    "cutoff_hour must be in [0, 23]",
)
@icontract.ensure(
    lambda result, timestamps: result.shape == timestamps.shape,
    "result must preserve shape",
)
def temporal_date_alignment(
    timestamps: NDArray[np.float64],
    cutoff_hour: int = 22,
) -> NDArray[np.float64]:
    """Assign events after cutoff_hour to the next business date.

    Prevents future data leakage by shifting late-arriving events
    (e.g. after-hours news) to the next calendar day. Timestamps
    are assumed to be Unix epoch seconds.
    """
    # Extract hour-of-day from timestamps (Unix epoch seconds)
    hours = (timestamps % 86400) / 3600.0
    # Events after cutoff_hour get shifted forward by one day (86400 seconds)
    shift = np.where(hours >= cutoff_hour, 86400.0, 0.0)
    return timestamps + shift
