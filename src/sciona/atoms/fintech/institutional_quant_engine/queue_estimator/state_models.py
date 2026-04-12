"""State model for deterministic queue-position estimation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OrderState(BaseModel):
    """Queue state for one resting order."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    my_order_id: str = Field(...)
    my_qty: float = Field(..., ge=0.0)
    orders_ahead: float = Field(..., ge=0.0)
    is_filled: bool = Field(default=False)
