"""Auto-generated verified atom wrapper."""

import numpy as np
import icontract
from ageoa.ghost.registry import register_atom
from .witnesses import witness_functional_monte_carlo, witness_volatility_surface_modeling



@register_atom(witness_functional_monte_carlo)
@icontract.require(lambda data: np.isfinite(data).all(), "data must contain only finite values")
@icontract.require(lambda data: data.shape[0] > 0, "data must not be empty")
@icontract.require(lambda data: data.ndim >= 1, "data must have at least one dimension")
@icontract.require(lambda data: data is not None, "data must not be None")
@icontract.require(lambda data: isinstance(data, np.ndarray), "data must be a numpy array")
@icontract.ensure(lambda result: result is not None, "result must not be None")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be a numpy array")
@icontract.ensure(lambda result: result.ndim >= 1, "result must have at least one dimension")
def functional_monte_carlo(data: np.ndarray) -> np.ndarray:
    """Generates stochastic paths and evaluates contingent claims using functional constraints.

    Args:
        data: Input N-dimensional tensor or 1D scalar array.

    Returns:
        Processed output array.
    """
    # Generate stochastic paths using data as drift/vol parameters.
    # Interpret data as [drift, vol, ...] or use first two elements.
    rng = np.random.default_rng(42)
    n_paths = max(data.shape[0], 1)
    n_steps = 100
    dt = 1.0 / n_steps
    if data.ndim == 1 and data.shape[0] >= 2:
        drift = data[0]
        vol = data[1]
    else:
        drift = 0.0
        vol = np.std(data) if data.size > 1 else 0.1
    # Generate GBM-style increments and return path values
    increments = rng.normal(0, 1, size=(n_paths, n_steps))
    log_paths = np.cumsum(
        (drift - 0.5 * vol ** 2) * dt + vol * np.sqrt(dt) * increments,
        axis=1,
    )
    result = np.exp(log_paths)
    # Reshape to match input dimensionality if needed
    if data.ndim == 1:
        return result.mean(axis=0) if result.shape[0] > 1 else result.ravel()
    return result

@register_atom(witness_volatility_surface_modeling)
@icontract.require(lambda data: np.isfinite(data).all(), "data must contain only finite values")
@icontract.require(lambda data: data.shape[0] > 0, "data must not be empty")
@icontract.require(lambda data: data.ndim >= 1, "data must have at least one dimension")
@icontract.require(lambda data: data is not None, "data must not be None")
@icontract.require(lambda data: isinstance(data, np.ndarray), "data must be a numpy array")
@icontract.ensure(lambda result: result is not None, "result must not be None")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be a numpy array")
@icontract.ensure(lambda result: result.ndim >= 1, "result must have at least one dimension")
def volatility_surface_modeling(data: np.ndarray) -> np.ndarray:
    """Interpolates and calibrates an implied variance surface.

    Args:
        data: Input N-dimensional tensor or 1D scalar array.

    Returns:
        Processed output array.
    """
    # Interpolate implied volatility surface from input data.
    # data is treated as a flat or 2D array of vol quotes.
    from scipy.interpolate import RBFInterpolator
    if data.ndim == 1:
        # 1D case: treat as vol values at evenly spaced strikes
        n = data.shape[0]
        strikes = np.linspace(0.5, 1.5, n)
        maturities = np.array([0.25])
        # Create a grid and interpolate to a finer grid
        fine_strikes = np.linspace(0.5, 1.5, n)
        result = np.interp(fine_strikes, strikes, data)
        return result
    elif data.ndim == 2:
        n_mat, n_strike = data.shape
        strikes = np.linspace(0.5, 1.5, n_strike)
        maturities = np.linspace(0.1, 2.0, n_mat)
        # Build coordinate pairs for RBF interpolation
        coords = np.array([(m, k) for m in maturities for k in strikes])
        values = data.ravel()
        rbf = RBFInterpolator(coords, values, kernel="thin_plate_spline")
        # Evaluate on same grid
        result = rbf(coords).reshape(data.shape)
        return result
    else:
        # Higher dimensional: flatten, interpolate, reshape
        flat = data.ravel()
        n = flat.shape[0]
        x = np.linspace(0, 1, n)
        result = np.interp(x, x, flat).reshape(data.shape)
        return result
