from __future__ import annotations

import numpy as np
import pandas as pd

import icontract
from sciona.ghost.registry import register_atom
from .fractional_diff_witnesses import witness_fractional_differentiator

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_fractional_differentiator)
@icontract.require(lambda series: isinstance(series, pd.Series), "series must be a pandas Series")
@icontract.require(lambda d: isinstance(d, (float, int, np.number)), "d must be numeric")
@icontract.require(lambda d: 0.0 <= float(d) <= 1.0, "d must be in [0, 1]")
@icontract.require(lambda threshold: isinstance(threshold, (float, int, np.number)) and float(threshold) > 0.0, "threshold must be positive")
@icontract.ensure(lambda result: isinstance(result, pd.Series), "fractional_differentiator must return a Series")
@icontract.ensure(lambda result: result.notna().all(), "fractional_differentiator output must not contain NaN")
def fractional_differentiator(series: pd.Series, d: float, threshold: float) -> pd.Series:
    """Return a fixed-width fractional difference of a numeric time series.

    The retained binomial weights are applied to windows that include the
    current observation. With ``d == 0`` this returns the original series,
    preserving the standard identity case.
    """
    values = pd.to_numeric(series, errors="coerce").astype(float)
    if values.empty:
        return pd.Series(index=series.index, dtype="float64")

    w = [1.0]
    order = float(d)
    cutoff = float(threshold)
    for k in range(1, len(values)):
        w_new = -w[-1] / k * (order - k + 1.0)
        if abs(w_new) < cutoff:
            break
        w.append(w_new)

    weights = np.asarray(w[::-1], dtype=np.float64)
    width = len(weights)
    if width > len(values):
        raise ValueError("series is too short for the retained fractional-difference weights")

    result = pd.Series(index=values.index, dtype="float64")
    for i in range(width - 1, len(values)):
        window = values.iloc[i - width + 1 : i + 1].to_numpy(dtype=np.float64)
        result.iloc[i] = float(np.dot(weights, window))
    return result.dropna()
