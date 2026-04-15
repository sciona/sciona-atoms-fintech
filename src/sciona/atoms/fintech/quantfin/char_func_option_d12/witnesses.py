from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractScalar


def witness_charfuncoption(arg0: AbstractScalar, cf: AbstractScalar, charFuncMart: AbstractScalar, d: AbstractScalar, damp: AbstractScalar, damp_prime: AbstractScalar, disc: AbstractScalar, exp: AbstractScalar, f: AbstractScalar, fg: AbstractScalar, func1: AbstractScalar, func2: AbstractScalar, i: AbstractScalar, intF: AbstractScalar, k: AbstractScalar, leftTerm: AbstractScalar, log: AbstractScalar, model: AbstractScalar, opt: AbstractScalar, p1: AbstractScalar, p2: AbstractScalar, pi: AbstractScalar, q: AbstractScalar, realPart: AbstractScalar, rightTerm: AbstractScalar, s: AbstractScalar, strike: AbstractScalar, tmat: AbstractScalar, v: AbstractScalar, v_prime: AbstractScalar, x: AbstractScalar, yc: AbstractScalar) -> AbstractScalar:
    """Describe the scalar option price returned by characteristic-function inversion."""
    return AbstractScalar(dtype="float64")

def witness_f(exp: AbstractScalar, i: AbstractScalar, k: AbstractScalar, leftTerm: AbstractScalar, realPart: AbstractScalar, rightTerm: AbstractScalar, v: AbstractScalar, v_prime: AbstractScalar) -> AbstractScalar:
    """Describe the scalar real-valued Fourier integrand."""
    return AbstractScalar(dtype="float64")

def witness_cf(charFuncMart: AbstractScalar, fg: AbstractScalar, model: AbstractScalar, tmat: AbstractScalar, x: AbstractScalar) -> AbstractScalar:
    """Describe the complex characteristic-function value at a single frequency."""
    return AbstractScalar(dtype="complex128")
