"""State model for a scalar Kalman filter."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class KalmanState(BaseModel):
    """Immutable scalar Kalman filter state."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    x: float = Field(...)
    p: float = Field(..., gt=0.0)
    q: float = Field(..., gt=0.0)
    r: float = Field(..., gt=0.0)
