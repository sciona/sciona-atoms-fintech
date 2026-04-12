from __future__ import annotations

from typing import Any
Boolean: Any = Any

"""Auto-generated atom wrappers following the sciona pattern."""


import numpy as np
import icontract
from ageoa.ghost.registry import register_atom
from .wash_trade_witnesses import witness_detect_wash_trade_rings


@register_atom(witness_detect_wash_trade_rings)
@icontract.require(lambda trade_graph: trade_graph.ndim >= 1, "trade_graph must have at least one dimension")
@icontract.require(lambda trade_graph: trade_graph is not None, "trade_graph cannot be None")
@icontract.require(lambda trade_graph: isinstance(trade_graph, np.ndarray), "trade_graph must be np.ndarray")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def detect_wash_trade_rings(trade_graph: np.ndarray) -> np.ndarray:
    """Detects wash trading rings in a directed trade graph by identifying simple cycles that indicate coordinated market manipulation.

    Args:
        trade_graph: Directed adjacency matrix of trades between participants, shape (n_traders, n_traders)

    Returns:
        Boolean mask of participants flagged as part of a wash-trading ring, shape (n_traders,)
    """
    # Detect wash trading rings via cycle detection in adjacency matrix
    n = trade_graph.shape[0]
    flagged = np.zeros(n, dtype=bool)
    # A trader is in a wash ring if there's a cycle through them
    # Check: A^k has nonzero diagonal for cycle of length k
    A = (trade_graph > 0).astype(float)
    power = A.copy()
    for k in range(2, min(n + 1, 6)):  # check cycles up to length 5
        power = power @ A
        diag = np.diag(power)
        flagged |= (diag > 0)
    return flagged.astype(np.float64)
