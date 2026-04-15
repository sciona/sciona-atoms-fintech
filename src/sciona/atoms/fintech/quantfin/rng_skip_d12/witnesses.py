from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractScalar, AbstractDistribution, AbstractSignal


def witness_randomword32(c: AbstractArray, state: AbstractArray, state_prime: AbstractArray, x: AbstractArray, xor: AbstractArray) -> AbstractArray:
    """Shape-and-type check for randomword32. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=c.shape,
        dtype="float64",
    )
    return result

def witness_randomint(fromIntegral: AbstractArray, g: AbstractArray, g_prime: AbstractArray, i: AbstractArray) -> AbstractArray:
    """Shape-and-type check for randomint. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=fromIntegral.shape,
        dtype="float64",
    )
    return result

def witness_randomword64(buildWord64_prime: AbstractArray, x: AbstractArray, x_prime: AbstractArray, y1: AbstractArray, y2: AbstractArray) -> AbstractArray:
    """Shape-and-type check for randomword64. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=buildWord64_prime.shape,
        dtype="float64",
    )
    return result

def witness_randomdouble(div: AbstractArray, fromIntegral: AbstractArray, val: AbstractArray, x: AbstractArray, x_prime: AbstractArray) -> AbstractArray:
    """Shape-and-type check for randomdouble. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=div.shape,
        dtype="float64",
    )
    return result

def witness_randomint64(fromIntegral: AbstractArray, g: AbstractArray, g_prime: AbstractArray, i: AbstractArray) -> AbstractArray:
    """Shape-and-type check for randomint64. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=fromIntegral.shape,
        dtype="float64",
    )
    return result

def witness_addmod64(a: AbstractArray, b: AbstractArray, m: AbstractArray, mod: AbstractArray) -> AbstractArray:
    """Shape-and-type check for addmod64. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=a.shape,
        dtype="float64",
    )
    return result

def witness_mulmod64(a: AbstractArray, b: AbstractArray, f: AbstractArray, m: AbstractArray) -> AbstractArray:
    """Shape-and-type check for mulmod64. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=a.shape,
        dtype="float64",
    )
    return result

def witness_powmod64(a: AbstractArray, e: AbstractArray, f: AbstractArray, m: AbstractArray) -> AbstractArray:
    """Shape-and-type check for powmod64. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=a.shape,
        dtype="float64",
    )
    return result

def witness_skip(d: AbstractArray, st: AbstractArray, st_prime: AbstractArray) -> AbstractArray:
    """Shape-and-type check for skip. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=d.shape,
        dtype="float64",
    )
    return result

def witness_next(fromIntegral: AbstractArray, g: AbstractArray, g_prime: AbstractArray, w: AbstractArray) -> AbstractArray:
    """Shape-and-type check for next. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=fromIntegral.shape,
        dtype="float64",
    )
    return result

def witness_split(g: AbstractArray, skip: AbstractArray, skipConst: AbstractArray) -> AbstractArray:
    """Shape-and-type check for split. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=g.shape,
        dtype="float64",
    )
    return result

def witness_mulmod64_inner_step(a_prime: AbstractArray, a1: AbstractArray, b_prime: AbstractArray, b1: AbstractArray, step: AbstractArray, otherwise: AbstractArray, r: AbstractArray, r_prime: AbstractArray) -> AbstractArray:
    """Shape-and-type check for mulmod64_inner_step. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=a_prime.shape,
        dtype="float64",
    )
    return result

def witness_powmod64_inner_step(acc: AbstractArray, acc_prime: AbstractArray, e_prime: AbstractArray, e1: AbstractArray, step: AbstractArray, otherwise: AbstractArray, sqr: AbstractArray, sqr_prime: AbstractArray) -> AbstractArray:
    """Shape-and-type check for powmod64_inner_step. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=acc.shape,
        dtype="float64",
    )
    return result
