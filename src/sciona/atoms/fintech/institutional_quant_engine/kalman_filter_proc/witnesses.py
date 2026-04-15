from __future__ import annotations
from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_kalman_filter_proc_placeholder() -> AbstractScalar:
    """Placeholder witness for the KalmanFilter proc atom directory."""
    return AbstractScalar()
