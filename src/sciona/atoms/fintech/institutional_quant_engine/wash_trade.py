from __future__ import annotations

"""Wash-trade ring detection over directed participant graphs."""

import numpy as np
import icontract
from sciona.ghost.registry import register_atom
from .wash_trade_witnesses import witness_detect_wash_trade_rings


@register_atom(witness_detect_wash_trade_rings)
@icontract.require(lambda trade_graph: isinstance(trade_graph, np.ndarray), "trade_graph must be np.ndarray")
@icontract.require(lambda trade_graph: trade_graph.ndim == 2, "trade_graph must be a matrix")
@icontract.require(lambda trade_graph: trade_graph.shape[0] == trade_graph.shape[1], "trade_graph must be square")
@icontract.ensure(lambda result, trade_graph: result.shape == (trade_graph.shape[0],), "result must have one flag per participant")
@icontract.ensure(lambda result: result.dtype == np.bool_, "result must be a boolean mask")
def detect_wash_trade_rings(trade_graph: np.ndarray) -> np.ndarray:
    """Flag participants that belong to any directed trading cycle.

    Positive entries in ``trade_graph[i, j]`` indicate trades from participant
    ``i`` to participant ``j``. The returned mask is true for every node that
    can reach itself through one or more directed edges.
    """
    adjacency = np.asarray(trade_graph > 0, dtype=bool)
    n = int(adjacency.shape[0])
    flagged = np.zeros(n, dtype=bool)

    for start in range(n):
        stack = list(np.flatnonzero(adjacency[start]))
        seen: set[int] = set()
        while stack:
            node = int(stack.pop())
            if node == start:
                flagged[start] = True
                break
            if node in seen:
                continue
            seen.add(node)
            stack.extend(int(next_node) for next_node in np.flatnonzero(adjacency[node]))

    return flagged
