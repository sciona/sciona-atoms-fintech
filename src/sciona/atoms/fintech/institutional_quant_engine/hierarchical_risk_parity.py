from __future__ import annotations

import numpy as np
import icontract
from ageoa.ghost.registry import register_atom
from .hierarchical_risk_parity_witnesses import witness_compute_hrp_weights


@register_atom(witness_compute_hrp_weights)
@icontract.require(lambda returns: returns.ndim >= 1, "returns must have at least one dimension")
@icontract.require(lambda returns: returns is not None, "returns cannot be None")
@icontract.require(lambda returns: isinstance(returns, np.ndarray), "returns must be np.ndarray")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def compute_hrp_weights(returns: np.ndarray) -> np.ndarray:
    """Computes Hierarchical Risk Parity portfolio weights by clustering assets and recursively bisecting risk along the dendrogram.

Args:
    returns: 2D array of asset returns, shape (n_samples, n_assets)

Returns:
    Hierarchical Risk Parity (HRP) portfolio weights, shape (n_assets,), summing to 1.0"""
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import squareform
    # Correlation-based distance and hierarchical clustering
    cov = np.cov(returns, rowvar=False)
    std = np.sqrt(np.diag(cov))
    corr = cov / np.outer(std, std)
    corr = np.clip(corr, -1, 1)
    dist = np.sqrt(0.5 * (1 - corr))
    np.fill_diagonal(dist, 0)
    link = linkage(squareform(dist), method='single')
    n = returns.shape[1]
    # Recursive bisection
    sort_ix = _get_quasi_diag(link, n)
    weights = np.ones(n)
    clusters = [sort_ix]
    while clusters:
        new_clusters = []
        for cluster in clusters:
            if len(cluster) <= 1:
                continue
            mid = len(cluster) // 2
            left, right = cluster[:mid], cluster[mid:]
            lvar = np.var(returns[:, left].sum(axis=1))
            rvar = np.var(returns[:, right].sum(axis=1))
            alpha = 1 - lvar / (lvar + rvar) if (lvar + rvar) > 0 else 0.5
            weights[left] *= alpha
            weights[right] *= (1 - alpha)
            new_clusters.extend([left, right])
        clusters = new_clusters
    return weights / weights.sum()


def _get_quasi_diag(link, n):
    """Extract quasi-diagonal order from linkage matrix."""
    sort_ix = [n]  # seed with a dummy
    sort_ix = list(range(n))
    # Use dendrogram leaf ordering
    from scipy.cluster.hierarchy import leaves_list
    return list(leaves_list(link))

import numpy as np
import pandas as pd

import icontract
from ageoa.ghost.registry import register_atom
from .hierarchical_risk_parity_witnesses import witness_hrppipelinerun


@register_atom(witness_hrppipelinerun)
@icontract.require(lambda data: isinstance(data, pd.DataFrame), "data must be a pandas DataFrame")
@icontract.require(lambda data: data.shape[1] >= 2, "data must have at least 2 asset columns")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "hrppipelinerun must return a numpy array")
def hrppipelinerun(data: pd.DataFrame) -> np.ndarray:
    """Executes the full Hierarchical Risk Parity pipeline: ingests asset return data, constructs a hierarchical clustering structure via a correlation/distance matrix, applies recursive bisection to allocate risk, and emits final portfolio weights.

    Args:
        data: asset returns DataFrame; no NaN values; N >= 2 columns; T > N rows recommended for stable covariance estimation

    Returns:
        Linkage matrix or portfolio weight array; all weights in [0, 1]; sum == 1.0
    """
    from scipy.cluster.hierarchy import linkage, leaves_list
    from scipy.spatial.distance import squareform
    returns = data.values
    cov = np.cov(returns, rowvar=False)
    std = np.sqrt(np.diag(cov))
    corr = cov / np.outer(std, std)
    corr = np.clip(corr, -1, 1)
    dist = np.sqrt(0.5 * (1 - corr))
    np.fill_diagonal(dist, 0)
    link = linkage(squareform(dist), method='single')
    n = returns.shape[1]
    sort_ix = list(leaves_list(link))
    weights = np.ones(n)
    clusters = [sort_ix]
    while clusters:
        new_clusters = []
        for cluster in clusters:
            if len(cluster) <= 1:
                continue
            mid = len(cluster) // 2
            left, right = cluster[:mid], cluster[mid:]
            lvar = np.var(returns[:, left].sum(axis=1))
            rvar = np.var(returns[:, right].sum(axis=1))
            alpha = 1 - lvar / (lvar + rvar) if (lvar + rvar) > 0 else 0.5
            weights[left] *= alpha
            weights[right] *= (1 - alpha)
            new_clusters.extend([left, right])
        clusters = new_clusters
    return weights / weights.sum()
