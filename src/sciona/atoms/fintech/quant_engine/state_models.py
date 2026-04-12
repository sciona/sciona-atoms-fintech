from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

class LimitQueueState(BaseModel):
    """State for queue-priority execution engine."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    strategy: str | None = Field(default=None)
    risk_limit: float | None = Field(default=None)
    orders_ahead: int | None = Field(default=None)
    my_qty: int | None = Field(default=None)
    is_filled: bool | None = Field(default=None)
    ofi_stream: list[float] | None = Field(default=None)
