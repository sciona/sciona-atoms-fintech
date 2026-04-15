from __future__ import annotations

import numpy as np
import pandas as pd

import icontract
from sciona.ghost.registry import register_atom
from .fractional_diff_witnesses import witness_fractional_differentiator

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_fractional_differentiator)
@icontract.require(lambda d: isinstance(d, (float, int, np.number)), "d must be numeric")
@icontract.require(lambda threshold: isinstance(threshold, (float, int, np.number)), "threshold must be numeric")
@icontract.ensure(lambda result: result is not None, "fractional_differentiator output must not be None")
def fractional_differentiator(series: pd.Series, d: float, threshold: float) -> pd.Series:
    """Computes the fractional differentiation of a time series. It first calculates the necessary weights based on the differentiation order 'd' and then applies them to the series, dropping terms below a specified threshold.

    Args:
        series: Input time series data.
        d: The order of differentiation, where 0 <= d <= 1.
        threshold: Threshold for dropping small weights to control memory usage. A smaller value means more terms are kept.

    Returns:
        The fractionally differentiated series.
    """
    # Compute fractional differentiation weights
    w = [1.0]
    for k in range(1, len(series)):
        w_new = -w[-1] / k * (d - k + 1)
        if abs(w_new) < threshold:
            break
        w.append(w_new)
    weights = np.array(w[::-1])
    width = len(weights)
    df_fd = pd.Series(index=series.index, dtype='float64')
    for i in range(width, len(series)):
        window = series.iloc[i - width:i].values
        df_fd.iloc[i] = np.dot(weights, window)
    return df_fd.dropna()
