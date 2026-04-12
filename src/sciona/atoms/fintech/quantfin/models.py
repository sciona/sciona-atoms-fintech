from __future__ import annotations

from typing import Any, Callable, Dict, List, Protocol, runtime_checkable

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

class YieldCurve(BaseModel):
    """Abstract base class for time-dependent discount factor curves."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def disc(self, t: float) -> float:
        """Compute the discount factor for the given time horizon."""
        raise NotImplementedError("Subclasses must implement disc")

    def forward(self, t1: float, t2: float) -> float:
        """Compute the instantaneous forward rate at the given time."""
        return np.log(self.disc(t1) / self.disc(t2)) / (t2 - t1)

    def spot(self, t: float) -> float:
        """Compute the zero-coupon rate for the given maturity."""
        return self.forward(0.0, t)

class FlatCurve(YieldCurve):
    """A constant-rate discount factor curve with continuous compounding."""
    rate: float = Field(..., ge=0.0)

    def disc(self, t: float) -> float:
        """Return exp(-rate * t) for this constant-rate curve."""
        return float(np.exp(-self.rate * t))

class NetYC(YieldCurve):
    """Discount curve representing the multiplicative ratio of two base curves."""
    yc1: SerializeAsAny[YieldCurve]
    yc2: SerializeAsAny[YieldCurve]

    def disc(self, t: float) -> float:
        """Return the ratio of the two underlying discount factors."""
        return self.yc1.disc(t) / self.yc2.disc(t)

class CashFlow(BaseModel):
    """A time-indexed scalar value with an associated discount curve."""
    time: float = Field(..., ge=0.0)
    amount: float

class CCProcessor(BaseModel):
    """Processor that evaluates a set of named payout mappings over a state trajectory."""
    monitor_time: float = Field(..., ge=0.0)
    payout_func_names: List[str] = Field(
        default_factory=list,
        description="Deterministic identifiers for payout functions",
    )
    payout_funcs: List[Callable[[Dict[float, Any]], CashFlow]] = Field(
        default_factory=list,
        exclude=True,
        repr=False,
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ContingentClaim(BaseModel):
    """A conditional payout specification defined by a set of evaluation times and payout functions."""
    processors: List[CCProcessor] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)

class DiscretizeModel(BaseModel):
    """Interface for continuous-time models that can be discretized for stochastic simulation."""
    model_config = ConfigDict(arbitrary_types_allowed=True)


@runtime_checkable
class SeededMonteCarloSimulator(Protocol):
    """Deterministic simulator boundary using an explicit seeded RNG."""

    def __call__(
        self,
        model: DiscretizeModel,
        claim: ContingentClaim,
        rng: np.random.Generator,
        trials: int,
        anti: bool,
    ) -> float:
        ...
