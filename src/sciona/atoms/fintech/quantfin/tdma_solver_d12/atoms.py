from __future__ import annotations

"""Atom wrappers for tridiagonal matrix (TDMA) solver utilities."""

import numpy as np
import icontract
from collections.abc import Callable, Iterable, Sequence
from typing import TypeAlias

from sciona.ghost.registry import register_atom
from .witnesses import witness_cotraversevec, witness_tdmasolver

import ctypes
import ctypes.util
from pathlib import Path


ScalarVector: TypeAlias = Sequence[float]
WrappedVectors: TypeAlias = Sequence[ScalarVector]
ProjectedSlices: TypeAlias = Sequence[float]
IndexRangeFactory: TypeAlias = Callable[[int, int], Sequence[int]]
ProjectedFunctorMap: TypeAlias = Callable[[Callable[[ScalarVector], float], WrappedVectors], ProjectedSlices]
IndexAggregator: TypeAlias = Callable[[ProjectedSlices], float]
IndexMap: TypeAlias = Callable[[Callable[[int], float], Sequence[int]], Iterable[float]]


# ---------------------------------------------------------------------------
# tdmasolver
# ---------------------------------------------------------------------------

@register_atom(witness_tdmasolver)
@icontract.require(lambda a: isinstance(a, list) and len(a) > 0, "a must be a non-empty list")
@icontract.require(lambda b: isinstance(b, list) and len(b) > 0, "b must be a non-empty list")
@icontract.require(lambda c: isinstance(c, list) and len(c) > 0, "c must be a non-empty list")
@icontract.require(lambda d: isinstance(d, list) and len(d) > 0, "d must be a non-empty list")
@icontract.ensure(lambda result: isinstance(result, list), "result must be a list")
@icontract.ensure(lambda result: len(result) > 0, "result must be non-empty")
def tdmasolver(
    a: list,
    aL: list,
    ai: float,
    b: list,
    bL: list,
    bi: float,
    c: list,
    c_prime: list,
    cL: list,
    cf: list,
    ci: float,
    ci1: float,
    ci1_prime: float,
    d: list,
    d_prime: list,
    dL: list,
    df: list,
    di: float,
    di1_prime: float,
    forM_: Callable,
    fromList: Callable,
    head: Callable,
    last: Callable,
    length: Callable,
    map: Callable,
    new: Callable,
    read: Callable,
    reverse: Callable,
    runST: Callable,
    thaw: Callable,
    toList: Callable,
    unsafeFreeze: Callable,
    write: Callable,
    x: list,
    xi1: float,
    xn: list,
) -> list:
    """Solve a tridiagonal matrix system using the Thomas algorithm (TDMA).

    Performs forward elimination and back-substitution on a tridiagonal
    system Ax = d where A is decomposed into sub-diagonal *a*, main
    diagonal *b*, and super-diagonal *c*.

    Args:
        a: Sub-diagonal coefficient list.
        aL: Sub-diagonal raw input list.
        ai: Current sub-diagonal element during sweep.
        b: Main diagonal coefficient list.
        bL: Main diagonal raw input list.
        bi: Current main diagonal element during sweep.
        c: Super-diagonal coefficient list.
        c_prime: Modified super-diagonal after forward sweep.
        cL: Super-diagonal raw input list.
        cf: Frozen super-diagonal vector after forward pass.
        ci: Current super-diagonal element.
        ci1: Previous super-diagonal element for back-sub.
        ci1_prime: Modified previous super-diagonal element.
        d: Right-hand side vector.
        d_prime: Modified right-hand side after forward sweep.
        dL: Right-hand side raw input list.
        df: Frozen right-hand side vector after forward pass.
        di: Current right-hand side element.
        di1_prime: Modified previous right-hand side element.
        forM_: Monadic for-each loop combinator.
        fromList: Convert a list to an immutable vector.
        head: Return first element of a list.
        last: Return last element of a list.
        length: Return length of a vector.
        map: Map a function over a list.
        new: Allocate a new mutable vector.
        read: Read an element from a mutable vector.
        reverse: Reverse a list.
        runST: Execute a stateful computation.
        thaw: Thaw an immutable vector into a mutable one.
        toList: Convert a vector to a list.
        unsafeFreeze: Freeze a mutable vector without copying.
        write: Write an element into a mutable vector.
        x: Solution vector workspace.
        xi1: Next solution element during back-substitution.
        xn: Mutable solution vector.

    Returns:
        Solution list for the tridiagonal system.
    """
    # Thomas algorithm (TDMA) for tridiagonal systems.
    # Forward elimination + back substitution.
    n = len(b)
    # Work with copies
    c_mod = [0.0] * n
    d_mod = [0.0] * n

    # Forward sweep
    c_mod[0] = c[0] / b[0]
    d_mod[0] = d[0] / b[0]
    for idx in range(1, n):
        a_val = a[idx] if idx < len(a) else 0.0
        c_val = c[idx] if idx < len(c) else 0.0
        denom = b[idx] - a_val * c_mod[idx - 1]
        c_mod[idx] = c_val / denom if denom != 0.0 else 0.0
        d_mod[idx] = (d[idx] - a_val * d_mod[idx - 1]) / denom if denom != 0.0 else 0.0

    # Back substitution
    x_sol = [0.0] * n
    x_sol[n - 1] = d_mod[n - 1]
    for idx in range(n - 2, -1, -1):
        x_sol[idx] = d_mod[idx] - c_mod[idx] * x_sol[idx + 1]

    return x_sol


# ---------------------------------------------------------------------------
# cotraversevec
# ---------------------------------------------------------------------------

@register_atom(witness_cotraversevec)
@icontract.require(lambda l: isinstance(l, int) and l > 0, "l must be a positive integer")
@icontract.require(lambda f: callable(f), "f must be callable")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def cotraversevec(
    enumFromN: IndexRangeFactory,
    f: IndexAggregator,
    fmap: ProjectedFunctorMap,
    i: int,
    l: int,
    m: WrappedVectors,
    map: IndexMap,
) -> list[float]:
    """Apply a co-traversal over unboxed vectors.

    Maps an index-wise extraction function across a functor of vectors,
    producing a single vector of aggregated results.

    Args:
        enumFromN: Generate an index range starting from a given value.
        f: Aggregation function applied to each index slice.
        fmap: Functor map over the input structure.
        i: Current index into the vector.
        l: Length of the output vector.
        m: Functor-wrapped collection of input vectors.
        map: Map function for the output vector.

    Returns:
        Aggregated vector produced by co-traversal.
    """
    # Co-traverse: apply f at each index across the functor of vectors.
    # enumFromN generates indices [0..l-1], f aggregates at each index.
    indices = enumFromN(i, l)
    return [
        float(value)
        for value in map(
            lambda idx: f(fmap(lambda vec: float(vec[idx]), m)),
            indices,
        )
    ]


# ---------------------------------------------------------------------------
# FFI bindings (auto-generated, kept for reference)
# ---------------------------------------------------------------------------

def _tdmasolver_ffi(a, aL, ai, b, bL, bi, c, c_prime, cL, cf, ci, ci1, ci1_prime, d, d_prime, dL, df, di, di1_prime, forM_, fromList, head, last, length, map, new, read, reverse, runST, thaw, toList, unsafeFreeze, write, x, xi1, xn):
    """Wrapper that calls the Haskell version of tdmasolver. Passes arguments through and returns the result."""
    _lib = ctypes.CDLL("./tdmasolver.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    _func.restype = ctypes.c_void_p
    return _func(a, aL, ai, b, bL, bi, c, c_prime, cL, cf, ci, ci1, ci1_prime, d, d_prime, dL, df, di, di1_prime, forM_, fromList, head, last, length, map, new, read, reverse, runST, thaw, toList, unsafeFreeze, write, x, xi1, xn)

def _cotraversevec_ffi(enumFromN, f, fmap, i, l, m, map):
    """Wrapper that calls the Haskell version of cotraversevec. Passes arguments through and returns the result."""
    _lib = ctypes.CDLL("./cotraversevec.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    _func.restype = ctypes.c_void_p
    return _func(enumFromN, f, fmap, i, l, m, map)
