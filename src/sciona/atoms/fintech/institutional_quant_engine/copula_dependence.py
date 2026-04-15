from __future__ import annotations

import numpy as np
import icontract
from sciona.ghost.registry import register_atom
from .copula_dependence_witnesses import witness_simulate_copula_dependence


@register_atom(witness_simulate_copula_dependence)
@icontract.require(lambda returns: returns.ndim >= 1, "returns must have at least one dimension")
@icontract.require(lambda returns: returns is not None, "returns cannot be None")
@icontract.require(lambda returns: isinstance(returns, np.ndarray), "returns must be np.ndarray")
@icontract.require(lambda rho: rho is not None, "rho cannot be None")
@icontract.require(lambda df: df is not None, "df cannot be None")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def simulate_copula_dependence(returns: np.ndarray, rho: float, df: int) -> np.ndarray:
    """Simulates tail-dependent asset returns via a t-copula calibrated to the given correlation and degrees-of-freedom.

    Args:
        returns: 2D array of asset returns, shape (n_samples, n_assets)
        rho: Correlation parameter for the copula
        df: Degrees of freedom for t-copula tail modelling

    Returns:
        Simulated correlated uniform marginals, shape (n_samples, n_assets)
    """
    from scipy.stats import t as t_dist
    n_samples, n_assets = returns.shape
    # Generate correlated t-distributed samples
    corr_matrix = np.full((n_assets, n_assets), rho)
    np.fill_diagonal(corr_matrix, 1.0)
    L = np.linalg.cholesky(corr_matrix)
    Z = np.random.standard_normal((n_samples, n_assets))
    chi2 = np.random.chisquare(df, size=(n_samples, 1))
    T = (Z @ L.T) / np.sqrt(chi2 / df)
    # Transform to uniform marginals via CDF
    U = t_dist.cdf(T, df)
    return U
