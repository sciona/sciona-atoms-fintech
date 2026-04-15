from __future__ import annotations

"""Atom wrappers for characteristic-function option pricing."""

from collections.abc import Mapping
import numpy as np
import icontract
from typing import Protocol, TypeAlias

from sciona.ghost.registry import register_atom
from .witnesses import witness_cf, witness_charfuncoption, witness_f

import ctypes
import ctypes.util
from pathlib import Path


QuantfinContext: TypeAlias = Mapping[str, float | complex | str | bool]


class ComplexFunction(Protocol):
    def __call__(self, x: complex, /) -> complex: ...


class RealFunction(Protocol):
    def __call__(self, x: float, /) -> float: ...


class RealFromComplex(Protocol):
    def __call__(self, x: complex, /) -> float: ...


class RealIntegrand(Protocol):
    def __call__(self, x: float, /) -> float: ...


class RealIntegrator(Protocol):
    def __call__(self, func: RealIntegrand, lower: float, upper: float, tolerance: float, /) -> float: ...


class MartingaleCharacteristicBuilder(Protocol):
    def __call__(self, model: QuantfinContext, fg: QuantfinContext, tmat: float, /) -> ComplexFunction: ...


class IntegrandFunction(Protocol):
    def __call__(
        self,
        exp: ComplexFunction,
        i: complex,
        k: complex,
        leftTerm: complex,
        realPart: RealFromComplex,
        rightTerm: complex,
        v: complex,
        v_prime: complex,
        /,
    ) -> float: ...


# ---------------------------------------------------------------------------
# charfuncoption
# ---------------------------------------------------------------------------

@register_atom(witness_charfuncoption)
@icontract.require(lambda strike: isinstance(strike, float) and strike > 0.0, "strike must be a positive float")
@icontract.require(lambda tmat: isinstance(tmat, float) and tmat > 0.0, "tmat -- time to maturity must be positive")
@icontract.require(lambda damp: isinstance(damp, float), "damp must be a float")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def charfuncoption(
    arg0: float,
    cf: ComplexFunction,
    charFuncMart: MartingaleCharacteristicBuilder,
    d: float,
    damp: float,
    damp_prime: float,
    disc: RealFunction,
    exp: ComplexFunction,
    f: IntegrandFunction,
    fg: QuantfinContext,
    func1: RealIntegrand,
    func2: RealIntegrand,
    i: complex,
    intF: RealIntegrator,
    k: float,
    leftTerm: complex,
    log: RealFunction,
    model: QuantfinContext,
    opt: str,
    p1: float,
    p2: float,
    pi: float,
    q: float,
    realPart: RealFromComplex,
    rightTerm: complex,
    s: float,
    strike: float,
    tmat: float,
    v: complex,
    v_prime: complex,
    x: float,
    yc: QuantfinContext,
) -> float:
    """Price a European option via characteristic-function inversion.

    Uses Fourier inversion of the model characteristic function to
    compute call or put prices.  The integration is damped to improve
    convergence.

    Args:
        arg0: Auxiliary numeric argument passed through the pipeline.
        cf: Characteristic function evaluated at a complex frequency.
        charFuncMart: Martingale-corrected characteristic function builder.
        d: Discount factor at maturity.
        damp: Damping coefficient for the Fourier integrand.
        damp_prime: Shifted damping coefficient used inside the integrand.
        disc: Discounting function from a yield curve.
        exp: Complex exponential function.
        f: Inner integrand helper that combines left and right terms.
        fg: Forward-generating yield curve object.
        func1: First probability integrand for the call decomposition.
        func2: Second probability integrand for the call decomposition.
        i: Imaginary unit (0 + 1j).
        intF: Numerical integration routine (lower, upper, tolerance).
        k: Log-strike used in the Fourier transform.
        leftTerm: Left multiplier in the integrand numerator.
        log: Natural logarithm function.
        model: Pricing model that implements the characteristic function.
        opt: Option type indicator (put or call).
        p1: First exercise probability from the inversion integral.
        p2: Second exercise probability from the inversion integral.
        pi: Mathematical constant pi.
        q: Forward price adjustment factor.
        realPart: Extract the real part of a complex number.
        rightTerm: Right multiplier (the characteristic function value).
        s: Current spot price.
        strike: Option strike price.
        tmat: Time to maturity in years.
        v: Complex integration variable.
        v_prime: Shifted complex integration variable.
        x: Intermediate workspace scalar.
        yc: Yield curve used for discounting.

    Returns:
        Fair value of the option as a float.
    """
    # Characteristic-function option pricing via Fourier inversion.
    # k = log(strike), d = discount factor, s = spot price
    # p1 and p2 are the two exercise probabilities from numerical integration
    # of func1 and func2 (the damped integrands).
    # Call price = d * (s * q * p1 - strike * p2)
    k_val = log(strike)
    d_val = disc(tmat)
    q_val = q if isinstance(q, (int, float)) else 1.0
    # Compute the two probability integrals via the provided integrator
    p1_val = 0.5 + (1.0 / pi) * intF(func1, 1e-8, 1000.0, 1e-8)
    p2_val = 0.5 + (1.0 / pi) * intF(func2, 1e-8, 1000.0, 1e-8)
    price = d_val * (s * q_val * p1_val - strike * p2_val)
    return float(price)


# ---------------------------------------------------------------------------
# f  (integrand helper)
# ---------------------------------------------------------------------------

@register_atom(witness_f)
@icontract.require(lambda k: isinstance(k, complex), "k must be complex")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def f(
    exp: ComplexFunction,
    i: complex,
    k: complex,
    leftTerm: complex,
    realPart: RealFromComplex,
    rightTerm: complex,
    v: complex,
    v_prime: complex,
) -> float:
    """Evaluate the real-valued integrand for characteristic-function pricing.

    Combines the complex exponential, the damping-dependent left term,
    and the characteristic-function right term, then extracts the real
    part.

    Args:
        exp: Complex exponential function.
        i: Imaginary unit (0 + 1j).
        k: Log-strike as a complex number.
        leftTerm: Damping-dependent numerator factor.
        realPart: Extract the real part of a complex value.
        rightTerm: Characteristic function value at the shifted frequency.
        v: Real-valued integration variable promoted to complex.
        v_prime: Shifted integration variable.

    Returns:
        Real part of the integrand at the given frequency.
    """
    # Evaluate the real-valued integrand for char-func pricing.
    # integrand = Re(exp(-i * v * k) * leftTerm * rightTerm)
    val = exp(-i * v * k) * leftTerm * rightTerm
    return float(realPart(val))


# ---------------------------------------------------------------------------
# cf  (characteristic function evaluator)
# ---------------------------------------------------------------------------

@register_atom(witness_cf)
@icontract.require(lambda tmat: isinstance(tmat, float) and tmat > 0.0, "tmat must be a positive float")
@icontract.require(lambda x: isinstance(x, complex), "x must be complex")
@icontract.ensure(lambda result: isinstance(result, complex), "result must be complex")
def cf(
    charFuncMart: MartingaleCharacteristicBuilder,
    fg: QuantfinContext,
    model: QuantfinContext,
    tmat: float,
    x: complex,
) -> complex:
    """Evaluate the martingale-corrected characteristic function.

    Delegates to the model's characteristic function generator and
    applies forward-generation adjustments so the discounted price
    process is a martingale.

    Args:
        charFuncMart: Builder that returns the corrected char function.
        fg: Forward-generating yield curve object.
        model: Pricing model providing the raw characteristic function.
        tmat: Time to maturity in years.
        x: Complex frequency at which to evaluate.

    Returns:
        Complex value of the characteristic function at frequency *x*.
    """
    # Evaluate the martingale-corrected characteristic function.
    # Delegates to charFuncMart which builds the corrected CF from the model.
    cf_func = charFuncMart(model, fg, tmat)
    return cf_func(x)


# ---------------------------------------------------------------------------
# FFI bindings (auto-generated, kept for reference)
# ---------------------------------------------------------------------------

def _charfuncoption_ffi(arg0, cf, charFuncMart, d, damp, damp_prime, disc, exp, f, fg, func1, func2, i, intF, k, leftTerm, log, model, opt, p1, p2, pi, q, realPart, rightTerm, s, strike, tmat, v, v_prime, x, yc):
    """Wrapper that calls the Haskell version of charfuncoption."""
    _lib = ctypes.CDLL("./charfuncoption.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 32
    _func.restype = ctypes.c_void_p
    return _func(arg0, cf, charFuncMart, d, damp, damp_prime, disc, exp, f, fg, func1, func2, i, intF, k, leftTerm, log, model, opt, p1, p2, pi, q, realPart, rightTerm, s, strike, tmat, v, v_prime, x, yc)

def _f_ffi(exp, i, k, leftTerm, realPart, rightTerm, v, v_prime):
    """Wrapper that calls the Haskell version of f."""
    _lib = ctypes.CDLL("./f.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 8
    _func.restype = ctypes.c_void_p
    return _func(exp, i, k, leftTerm, realPart, rightTerm, v, v_prime)

def _cf_ffi(charFuncMart, fg, model, tmat, x):
    """Wrapper that calls the Haskell version of cf."""
    _lib = ctypes.CDLL("./cf.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(charFuncMart, fg, model, tmat, x)
