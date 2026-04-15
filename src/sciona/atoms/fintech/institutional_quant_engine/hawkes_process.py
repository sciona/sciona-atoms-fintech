from __future__ import annotations

import numpy as np

import icontract
from sciona.ghost.registry import register_atom
from .hawkes_process_witnesses import witness_sample_hawkes_event_trajectory

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_sample_hawkes_event_trajectory)  # type: ignore[untyped-decorator, name-defined]
@icontract.require(lambda mu: isinstance(mu, (float, int, np.number)), "mu must be numeric")
@icontract.require(lambda alpha: isinstance(alpha, (float, int, np.number)), "alpha must be numeric")
@icontract.require(lambda beta: isinstance(beta, (float, int, np.number)), "beta must be numeric")
@icontract.require(lambda T: isinstance(T, (float, int, np.number)), "T must be numeric")
@icontract.ensure(lambda result: result is not None, "sample_hawkes_event_trajectory output must not be None")
def sample_hawkes_event_trajectory(mu: float, alpha: float, beta: float, T: float) -> np.ndarray:  # type: ignore[type-arg]
    """Simulates a Hawkes point-process realization over a finite horizon using the provided base intensity and excitation/decay parameters.

    Args:
        mu: mu >= 0
        alpha: alpha >= 0
        beta: beta > 0
        T: T > 0

    Returns:
        sorted ascending, each t in [0, T]
    """
    t = 0.0
    points = []
    while t < T:
        past = np.array(points) if points else np.array([])
        upper_bound = mu + np.sum(alpha * np.exp(-beta * (t - past)))
        dt = -np.log(np.random.uniform()) / upper_bound
        t += dt
        if t >= T:
            break
        past_new = np.array(points) if points else np.array([])
        actual_intensity = mu + np.sum(alpha * np.exp(-beta * (t - past_new)))
        if np.random.uniform() < actual_intensity / upper_bound:
            points.append(t)
    return np.array(points)

import numpy as np

import icontract
from sciona.ghost.registry import register_atom
from .hawkes_process_witnesses import witness_hawkesprocesssimulator

# Witness functions should be imported from the generated witnesses module
@register_atom(witness_hawkesprocesssimulator)  # type: ignore[untyped-decorator]
@icontract.require(lambda mu: isinstance(mu, (float, int, np.number)), "mu must be numeric")
@icontract.require(lambda alpha: isinstance(alpha, (float, int, np.number)), "alpha must be numeric")
@icontract.require(lambda beta: isinstance(beta, (float, int, np.number)), "beta must be numeric")
@icontract.require(lambda T: isinstance(T, (float, int, np.number)), "T must be numeric")
@icontract.ensure(lambda result: result is not None, "HawkesProcessSimulator output must not be None")
def hawkesprocesssimulator(mu: float, alpha: float, beta: float, T: float) -> np.ndarray:  # type: ignore[type-arg]
    """Simulates a univariate Hawkes self-exciting point process over the interval [0, T] using Ogata's thinning algorithm. Given baseline intensity mu, excitation amplitude alpha, and exponential decay rate beta, draws stochastic event times whose conditional intensity is λ(t) = μ + Σᵢ α·exp(−β(t−tᵢ)) for all past events tᵢ < t. Returns the full realisation as an array of arrival times.

    Args:
        mu: strictly positive scalar
        alpha: non-negative scalar; α/β < 1 for stationarity
        beta: strictly positive scalar
        T: strictly positive scalar

    Returns:
        monotonically increasing, all values in (0, T]
    """
    t = 0.0
    points = []
    while t < T:
        past = np.array(points) if points else np.array([])
        upper_bound = mu + np.sum(alpha * np.exp(-beta * (t - past)))
        dt = -np.log(np.random.uniform()) / upper_bound
        t += dt
        if t >= T:
            break
        past_new = np.array(points) if points else np.array([])
        actual_intensity = mu + np.sum(alpha * np.exp(-beta * (t - past_new)))
        if np.random.uniform() < actual_intensity / upper_bound:
            points.append(t)
    return np.array(points)
