from __future__ import annotations

import numpy as np
import icontract
from ageoa.ghost.registry import register_atom
from .supply_chain_witnesses import witness_propagate_supply_shock


@register_atom(witness_propagate_supply_shock)
@icontract.require(lambda adjacency: adjacency.ndim >= 1, "adjacency must have at least one dimension")
@icontract.require(lambda initial_shock: initial_shock.ndim >= 1, "initial_shock must have at least one dimension")
@icontract.require(lambda adjacency: adjacency is not None, "adjacency cannot be None")
@icontract.require(lambda adjacency: isinstance(adjacency, np.ndarray), "adjacency must be np.ndarray")
@icontract.require(lambda initial_shock: initial_shock is not None, "initial_shock cannot be None")
@icontract.require(lambda initial_shock: isinstance(initial_shock, np.ndarray), "initial_shock must be np.ndarray")
@icontract.ensure(lambda result: isinstance(result, np.ndarray), "result must be np.ndarray")
@icontract.ensure(lambda result: result is not None, "result must not be None")
def propagate_supply_shock(adjacency: np.ndarray, initial_shock: np.ndarray) -> np.ndarray:
    """Propagates a supply chain disruption shock through a Directed Acyclic Graph (DAG) of supplier relationships, computing downstream impact at each node.

    Args:
        adjacency: Weighted adjacency matrix of the supply chain DAG, shape (n_nodes, n_nodes)
        initial_shock: Vector of initial shock magnitudes at each node, shape (n_nodes,)

    Returns:
        Propagated impact scores at each downstream node, shape (n_nodes,)
    """
    # Propagate shock through DAG: impact = (I - A)^{-1} @ shock
    n = adjacency.shape[0]
    impact = initial_shock.copy().astype(float)
    # Iterative propagation (converges for DAGs)
    for _ in range(n):
        impact = initial_shock + adjacency.T @ impact
    return impact
