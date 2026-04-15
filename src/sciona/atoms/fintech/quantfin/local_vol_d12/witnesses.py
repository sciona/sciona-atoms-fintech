from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractScalar


def witness_var(s: AbstractScalar, t: AbstractScalar, t_prime: AbstractScalar, v: AbstractScalar, vs: AbstractScalar) -> AbstractScalar:
    """Describe the scalar implied variance returned from a local-vol surface."""
    return AbstractScalar(dtype="float64", min_val=0.0)

def witness_localvol(dwdt: AbstractScalar, k: AbstractScalar, otherwise: AbstractScalar, rcurve: AbstractScalar, s0: AbstractScalar, solution: AbstractScalar, sqrt: AbstractScalar, t: AbstractScalar, v: AbstractScalar, w: AbstractScalar) -> AbstractScalar:
    """Describe the scalar Dupire local volatility returned at one surface point."""
    return AbstractScalar(dtype="float64", min_val=0.0)

def witness_vol(x: AbstractArray) -> AbstractArray:
    """Shape-and-type check for vol. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=x.shape,
        dtype="float64",
    )
    return result

def witness_vol(interpolatedVs: AbstractArray, mats: AbstractArray, mats_prime: AbstractArray, quotes: AbstractArray, strike: AbstractArray, sts: AbstractArray, t: AbstractArray, tInterp: AbstractArray, timeFromZero: AbstractArray, vInterp: AbstractArray) -> AbstractArray:
    """Shape-and-type check for vol. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=interpolatedVs.shape,
        dtype="float64",
    )
    return result

def witness_allfort(map: AbstractArray, quotes: AbstractArray, sts: AbstractArray, t_prime: AbstractArray, x: AbstractArray) -> AbstractArray:
    """Shape-and-type check for allfort. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=map.shape,
        dtype="float64",
    )
    return result
