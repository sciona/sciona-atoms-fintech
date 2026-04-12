"""Ghost witnesses for scalar Kalman filter atoms."""

from __future__ import annotations

from ageoa.ghost.abstract import AbstractArray, AbstractScalar


def witness_kalmanfilterinit(
    process_variance: AbstractScalar,
    measurement_variance: AbstractScalar,
    estimated_measurement_variance: AbstractScalar,
) -> AbstractArray:
    """Initialization yields a compact scalar-state record."""

    return AbstractArray(shape=(4,), dtype="float64")


def witness_kalmanmeasurementupdate(
    prior_state: AbstractArray,
    measurement: AbstractScalar,
) -> AbstractArray:
    """One update preserves the scalar-state record shape."""

    return AbstractArray(shape=prior_state.shape, dtype="float64")
