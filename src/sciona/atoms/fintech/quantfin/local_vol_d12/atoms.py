from __future__ import annotations

"""Atom wrappers for local-volatility surface operations (Dupire model)."""

from collections.abc import Mapping
import numpy as np
import icontract
from typing import Protocol

from ageoa.ghost.registry import register_atom
from .witnesses import witness_allfort, witness_localvol, witness_var, witness_vol

import ctypes
import ctypes.util
from pathlib import Path


QuantfinSurfaceContext = Mapping[str, float | complex | str | bool]


class RealUnaryFunction(Protocol):
    def __call__(self, x: float, /) -> float: ...


# ---------------------------------------------------------------------------
# var  — implied variance at a given strike and maturity
# ---------------------------------------------------------------------------

@register_atom(witness_var)
@icontract.require(lambda s: isinstance(s, float) and s > 0.0, "s -- strike must be a positive float")
@icontract.require(lambda t: isinstance(t, float) and t >= 0.0, "t -- time must be non-negative")
@icontract.ensure(lambda result: isinstance(result, float) and result >= 0.0, "variance must be a non-negative float")
def var(
    s: float,
    t: float,
    t_prime: float,
    v: float,
    vs: QuantfinSurfaceContext,
) -> float:
    """Compute implied variance for a strike and maturity on a volatility surface.

    Calculates var = vol^2 * t, where vol is the implied volatility
    looked up from the surface *vs* at strike *s* and time *t*.

    Args:
        s: Strike price (relative to spot).
        t: Time to maturity in years.
        t_prime: Auxiliary time value (timeFromZero extraction).
        v: Implied volatility at (s, t).
        vs: Volatility surface object.

    Returns:
        Implied variance (volatility squared times time).
    """
    # Implied variance = vol^2 * t
    # v is already the implied vol at (s, t), t_prime is timeFromZero(t)
    return float(v * v * t_prime)


# ---------------------------------------------------------------------------
# localvol  — Dupire local volatility
# ---------------------------------------------------------------------------

@register_atom(witness_localvol)
@icontract.require(lambda s0: isinstance(s0, float) and s0 > 0.0, "s0 -- initial spot must be positive")
@icontract.require(lambda k: isinstance(k, float) and k > 0.0, "k -- current stock level must be positive")
@icontract.ensure(lambda result: isinstance(result, float) and result >= 0.0, "local vol must be non-negative")
def localvol(
    dwdt: float,
    k: float,
    otherwise: float,
    rcurve: QuantfinSurfaceContext,
    s0: float,
    solution: float,
    sqrt: RealUnaryFunction,
    t: float,
    v: float,
    w: float,
) -> float:
    """Compute Dupire local volatility at a given spot level and time.

    Derives the local volatility from an implied-variance surface by
    applying the Dupire formula, which relates local vol to the partial
    derivatives of total implied variance with respect to strike and
    time.

    Args:
        dwdt: Partial derivative of implied variance with respect to time.
        k: Current stock (or strike) level.
        otherwise: Fallback local-vol value when the main formula is valid.
        rcurve: Yield curve used to generate forwards and discount factors.
        s0 -- initial spot price: Starting asset price.
        solution: Dupire formula denominator result.
        sqrt: Square-root function.
        t: Time to maturity in years.
        v: Implied variance at the current point.
        w: Total implied variance w(k, t).

    Returns:
        Local volatility at the given (k, t) point.
    """
    # Dupire local volatility: sigma_local = sqrt(dwdt / solution)
    # where dwdt = dw/dt, solution is the denominator from the Dupire formula.
    # The 'otherwise' parameter is the fallback when the formula is degenerate.
    # Pre-computed: dwdt, w, solution, v
    if solution <= 0.0 or not np.isfinite(solution):
        return float(abs(otherwise))
    local_var = dwdt / solution
    if local_var < 0.0:
        return float(abs(otherwise))
    return float(sqrt(local_var))


# ---------------------------------------------------------------------------
# vol  — flat surface lookup (single value)
# ---------------------------------------------------------------------------

@register_atom(witness_vol)
@icontract.require(lambda x: isinstance(x, float), "x must be a float")
@icontract.ensure(lambda result: isinstance(result, float) and result >= 0.0, "vol must be non-negative")
def vol(x: float) -> float:
    """Return the constant implied volatility from a flat surface.

    For a flat volatility surface the vol is the same at every strike
    and maturity, so only the stored scalar *x* is returned.

    Args:
        x: Stored flat volatility value.

    Returns:
        Implied volatility (constant).
    """
    # Flat vol surface: just return the stored constant.
    return float(abs(x))


# ---------------------------------------------------------------------------
# vol  — grid surface lookup (interpolated)
# ---------------------------------------------------------------------------

@register_atom(witness_vol)
@icontract.require(lambda strike: isinstance(strike, float) and strike > 0.0, "strike must be a positive float")
@icontract.ensure(lambda result: isinstance(result, float) and result >= 0.0, "vol must be non-negative")
def vol(
    interpolatedVs: list,
    mats: list,
    mats_prime: list,
    quotes: dict,
    strike: float,
    sts: list,
    t: float,
    tInterp: Callable,
    timeFromZero: Callable,
    vInterp: Callable,
) -> float:
    """Interpolate implied volatility from a grid surface.

    Performs two-dimensional interpolation: first along the strike axis
    at each maturity using *vInterp*, then along the time axis using
    *tInterp*.

    Args:
        interpolatedVs: Strike-interpolated vol values at each maturity.
        mats: List of maturity time objects.
        mats_prime: Maturity values converted to raw floats.
        quotes: Map from (strike, maturity) pairs to quoted volatilities.
        strike: Target strike price.
        sts: List of grid strike levels.
        t: Target time object.
        tInterp: One-dimensional time interpolator.
        timeFromZero: Convert a time object to a float offset from zero.
        vInterp: One-dimensional strike interpolator.

    Returns:
        Interpolated implied volatility at (strike, t).
    """
    # Interpolate vol from a grid surface.
    # interpolatedVs contains strike-interpolated vol values at each maturity.
    # mats_prime contains maturity floats. Use tInterp along time axis.
    t_val = timeFromZero(t)
    # interpolatedVs[i] = vInterp(strike, sts, quotes_at_mat_i)
    # Final interpolation along time using tInterp
    return float(tInterp(t_val, mats_prime, interpolatedVs))


# ---------------------------------------------------------------------------
# allfort  — extract all quotes for a given maturity
# ---------------------------------------------------------------------------

@register_atom(witness_allfort)
@icontract.require(lambda sts: isinstance(sts, list) and len(sts) > 0, "sts must be a non-empty list of strikes")
@icontract.require(lambda quotes: isinstance(quotes, dict), "quotes must be a dict")
@icontract.ensure(lambda result: isinstance(result, list), "result must be a list")
def allfort(
    map: Callable,
    quotes: dict,
    sts: list,
    t_prime: float,
    x: float,
) -> list:
    """Extract all quoted volatilities for a single maturity slice.

    Looks up each strike in *sts* against the quotes map at maturity
    *t_prime* and returns the corresponding volatility values.

    Args:
        map: Map function to apply across strikes.
        quotes: Map from (strike, maturity) pairs to quoted volatilities.
        sts: List of grid strike levels.
        t_prime: Maturity value to look up.
        x: Current strike being processed.

    Returns:
        List of quoted volatilities for every strike at the given maturity.
    """
    # Extract all quoted volatilities for a single maturity slice.
    # Map over strikes, looking up each one at the given maturity.
    return list(map(lambda s: quotes.get((s, t_prime), 0.0), sts))


# ---------------------------------------------------------------------------
# FFI bindings (auto-generated, kept for reference)
# ---------------------------------------------------------------------------

def _var_ffi(s, t, t_prime, v, vs):
    """Wrapper that calls the Haskell version of var."""
    _lib = ctypes.CDLL("./var.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(s, t, t_prime, v, vs)

def _localvol_ffi(dwdt, k, otherwise, rcurve, s0, solution, sqrt, t, v, w):
    """Wrapper that calls the Haskell version of localvol."""
    _lib = ctypes.CDLL("./localvol.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 10
    _func.restype = ctypes.c_void_p
    return _func(dwdt, k, otherwise, rcurve, s0, solution, sqrt, t, v, w)

def _vol_ffi(x):
    """Wrapper that calls the Haskell version of vol (flat surface)."""
    _lib = ctypes.CDLL("./vol.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p]
    _func.restype = ctypes.c_void_p
    return _func(x)

def _vol_grid_ffi(interpolatedVs, mats, mats_prime, quotes, strike, sts, t, tInterp, timeFromZero, vInterp):
    """Wrapper that calls the Haskell version of vol (grid surface)."""
    _lib = ctypes.CDLL("./vol.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 10
    _func.restype = ctypes.c_void_p
    return _func(interpolatedVs, mats, mats_prime, quotes, strike, sts, t, tInterp, timeFromZero, vInterp)

def _allfort_ffi(map, quotes, sts, t_prime, x):
    """Wrapper that calls the Haskell version of allfort."""
    _lib = ctypes.CDLL("./allfort.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(map, quotes, sts, t_prime, x)
