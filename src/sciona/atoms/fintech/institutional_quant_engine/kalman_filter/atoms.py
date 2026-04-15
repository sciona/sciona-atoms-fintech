"""Deterministic scalar Kalman filter atoms."""

from __future__ import annotations

import numpy as np

import icontract
from sciona.ghost.registry import register_atom

from .state_models import KalmanState
from .witnesses import witness_kalmanfilterinit, witness_kalmanmeasurementupdate


def _is_numeric_scalar(value: object) -> bool:
    return isinstance(value, (float, int, np.number))


@register_atom(witness_kalmanfilterinit)
@icontract.require(lambda process_variance: _is_numeric_scalar(process_variance) and float(process_variance) > 0.0, "process_variance must be positive")
@icontract.require(lambda measurement_variance: _is_numeric_scalar(measurement_variance) and float(measurement_variance) > 0.0, "measurement_variance must be positive")
@icontract.require(lambda estimated_measurement_variance: _is_numeric_scalar(estimated_measurement_variance) and float(estimated_measurement_variance) > 0.0, "estimated_measurement_variance must be positive")
@icontract.ensure(lambda result: result.p > 0.0 and result.q > 0.0 and result.r > 0.0, "all covariance terms must remain positive")
def kalmanfilterinit(
    process_variance: float,
    measurement_variance: float,
    estimated_measurement_variance: float,
) -> KalmanState:
    """Initialize a scalar Kalman filter state.

    Args:
        process_variance: Process-noise variance ``Q``.
        measurement_variance: Measurement-noise variance ``R``.
        estimated_measurement_variance: Initial covariance estimate ``P``.

    Returns:
        An immutable ``KalmanState`` with initial state estimate ``x = 0.0``.
    """

    return KalmanState(
        x=0.0,
        p=float(estimated_measurement_variance),
        q=float(process_variance),
        r=float(measurement_variance),
    )


@register_atom(witness_kalmanmeasurementupdate)
@icontract.require(lambda prior_state: prior_state is not None, "prior_state cannot be None")
@icontract.require(lambda measurement: _is_numeric_scalar(measurement), "measurement must be numeric")
@icontract.ensure(lambda result: result.p > 0.0, "posterior covariance must remain positive")
def kalmanmeasurementupdate(prior_state: KalmanState, measurement: float) -> KalmanState:
    """Run one scalar Kalman predict/update step.

    Args:
        prior_state: Prior scalar Kalman filter state.
        measurement: Observed scalar measurement.

    Returns:
        The posterior ``KalmanState`` after one predict/update step.
    """

    predicted_p = prior_state.p + prior_state.q
    gain = predicted_p / (predicted_p + prior_state.r)
    innovation = float(measurement) - prior_state.x
    posterior_x = prior_state.x + gain * innovation
    posterior_p = (1.0 - gain) * predicted_p
    if posterior_p <= 0.0:
        posterior_p = np.finfo(float).eps

    return KalmanState(
        x=float(posterior_x),
        p=float(posterior_p),
        q=prior_state.q,
        r=prior_state.r,
    )
