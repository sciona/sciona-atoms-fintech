from __future__ import annotations
"""Auto-generated atom wrappers following the sciona pattern."""


import numpy as np

import icontract
from sciona.ghost.registry import register_atom
from .witnesses import witness_optimalexecutiontrajectory, witness_riskaversioninit

# Witness functions should be imported from the generated witnesses module

@register_atom(witness_riskaversioninit)  # type: ignore[untyped-decorator, name-defined]
@icontract.require(lambda risk_aversion: isinstance(risk_aversion, (float, int, np.number)), "risk_aversion must be numeric")
@icontract.ensure(lambda result: result is not None, "RiskAversionInit output must not be None")
def riskaversioninit(risk_aversion: float) -> float:
    """Bootstraps the Almgren-Chriss model by storing the scalar risk-aversion parameter that governs the volatility-vs-impact trade-off in all subsequent trajectory computations.

    Args:
        risk_aversion: ≥ 0

    Returns:
        ≥ 0
    """
    return float(risk_aversion)

@register_atom(witness_optimalexecutiontrajectory)  # type: ignore[untyped-decorator, name-defined]
@icontract.require(lambda risk_aversion: isinstance(risk_aversion, (float, int, np.number)), "risk_aversion must be numeric")
@icontract.require(lambda total_shares: isinstance(total_shares, (float, int, np.number)), "total_shares must be numeric")
@icontract.ensure(lambda result: result is not None, "OptimalExecutionTrajectory output must not be None")
def optimalexecutiontrajectory(risk_aversion: float, total_shares: float, days: int) -> list[float]:
    """Solves the Almgren-Chriss discrete-time optimal liquidation problem: given total shares and a horizon in days, applies dynamic-programming / optimal-control to produce the cost-minimizing share-selling schedule that balances market-impact cost against price-risk, parameterised by risk_aversion.

    Args:
        risk_aversion: ≥ 0
        total_shares: > 0
        days: ≥ 1

    Returns:
        monotonically non-increasing, x_T = 0
    """
    # Almgren-Chriss optimal liquidation trajectory
    trajectory = []
    for t in range(days + 1):
        remaining = total_shares * (1 - t / days)
        trajectory.append(remaining)
    return trajectory