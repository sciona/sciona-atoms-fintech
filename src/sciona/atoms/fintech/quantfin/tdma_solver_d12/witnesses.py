from __future__ import annotations
from ageoa.ghost.abstract import AbstractArray, AbstractScalar, AbstractDistribution, AbstractSignal


def witness_tdmasolver(a: AbstractArray, aL: AbstractArray, ai: AbstractArray, b: AbstractArray, bL: AbstractArray, bi: AbstractArray, c: AbstractArray, c_prime: AbstractArray, cL: AbstractArray, cf: AbstractArray, ci: AbstractArray, ci1: AbstractArray, ci1_prime: AbstractArray, d: AbstractArray, d_prime: AbstractArray, dL: AbstractArray, df: AbstractArray, di: AbstractArray, di1_prime: AbstractArray, forM_: AbstractArray, fromList: AbstractArray, head: AbstractArray, last: AbstractArray, length: AbstractArray, map: AbstractArray, new: AbstractArray, read: AbstractArray, reverse: AbstractArray, runST: AbstractArray, thaw: AbstractArray, toList: AbstractArray, unsafeFreeze: AbstractArray, write: AbstractArray, x: AbstractArray, xi1: AbstractArray, xn: AbstractArray) -> AbstractArray:
    """Shape-and-type check for tdmasolver. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=a.shape,
        dtype="float64",
    )
    return result

def witness_cotraversevec(enumFromN: AbstractArray, f: AbstractArray, fmap: AbstractArray, i: AbstractArray, l: AbstractArray, m: AbstractArray, map: AbstractArray) -> AbstractArray:
    """Shape-and-type check for cotraversevec. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=enumFromN.shape,
        dtype="float64",
    )
    return result
