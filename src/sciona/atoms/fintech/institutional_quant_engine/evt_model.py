from __future__ import annotations

import numpy as np
import icontract
from ageoa.ghost.registry import register_atom
from .evt_model_witnesses import witness_fit_gpd_tail


@register_atom(witness_fit_gpd_tail)
@icontract.require(lambda returns: returns.ndim >= 1, "returns must have at least one dimension")
@icontract.require(lambda returns: returns is not None, "returns cannot be None")
@icontract.require(lambda returns: isinstance(returns, np.ndarray), "returns must be np.ndarray")
@icontract.require(lambda threshold_quantile: threshold_quantile is not None, "threshold_quantile cannot be None")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def fit_gpd_tail(returns: np.ndarray, threshold_quantile: float) -> np.ndarray:
    """Fits a Generalized Pareto Distribution (GPD) to tail losses beyond the given quantile threshold for Extreme Value Theory (EVT) modeling.

    Args:
        returns: 1D array of portfolio returns
        threshold_quantile: Quantile used to select the tail threshold (e.g. 0.05 for 5th percentile)

    Returns:
        Array of [shape, loc, scale] GPD parameters fit to the exceedance tail
    """
    from scipy.stats import genpareto
    losses = -returns  # convert to losses
    threshold = np.quantile(losses, 1 - threshold_quantile)
    exceedances = losses[losses > threshold] - threshold
    if len(exceedances) < 2:
        return np.array([0.0, threshold, 1.0])
    shape, loc, scale = genpareto.fit(exceedances, floc=0)
    return np.array([shape, threshold, scale])
