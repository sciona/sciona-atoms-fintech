import icontract
from typing import Dict

import numpy as np

from sciona.ghost.registry import register_atom
from sciona.atoms.fintech.quantfin.models import (
    ContingentClaim,
    DiscretizeModel,
    SeededMonteCarloSimulator,
)
from sciona.atoms.fintech.quantfin.witnesses import witness_run_simulation, witness_run_simulation_anti, witness_quick_sim_anti

SIMULATOR_REGISTRY: Dict[str, SeededMonteCarloSimulator] = {}


@icontract.require(lambda name: isinstance(name, str) and name.strip() != "", "name must be non-empty")
@icontract.require(lambda simulator: callable(simulator), "simulator must be callable")
def _register_simulator(name: str, simulator: SeededMonteCarloSimulator) -> None:
    """Register a deterministic seeded simulator by name."""
    SIMULATOR_REGISTRY[name] = simulator


def _list_simulators() -> list[str]:
    """Return sorted simulator registry keys."""
    return sorted(SIMULATOR_REGISTRY.keys())


@icontract.require(lambda simulator_name: simulator_name in SIMULATOR_REGISTRY, "simulator_name must reference a registered simulator")
def _resolve_simulator(simulator_name: str) -> SeededMonteCarloSimulator:
    return SIMULATOR_REGISTRY[simulator_name]


@register_atom(witness_run_simulation)
@icontract.require(lambda trials: trials > 0)
@icontract.require(lambda seed: seed >= 0, "seed must be non-negative")
@icontract.require(lambda simulator_name: isinstance(simulator_name, str) and simulator_name.strip() != "", "simulator_name must be non-empty")
@icontract.ensure(lambda result: isinstance(result, float), "result must be float")
@icontract.ensure(lambda result: np.isfinite(result), "result must be finite")
def run_simulation(
    model: DiscretizeModel,
    claim: ContingentClaim,
    seed: int,
    trials: int,
    anti: bool,
    simulator_name: str,
) -> float:
    """Run one Monte Carlo pass with an explicit seeded RNG boundary.

    Args:
        model: Discretized market model or simulation model state.
        claim: Contingent claim whose payoff is being priced.
        seed: Non-negative RNG seed.
        trials: Number of Monte Carlo trajectories.
        anti: Whether to use antithetic pairing inside the simulator.
        simulator_name: Registry key selecting the seeded simulator.

    Returns:
        Estimated discounted payoff expectation as a finite float.
    """
    simulator = _resolve_simulator(simulator_name)
    rng = np.random.default_rng(seed)
    return float(simulator(model, claim, rng, trials, anti))

@register_atom(witness_run_simulation_anti)
@icontract.require(lambda trials: trials > 0)
@icontract.require(lambda trials: trials % 2 == 0, "Trials must be even for antithetic variates")
@icontract.require(lambda seed: seed >= 0, "seed must be non-negative")
@icontract.ensure(lambda result: isinstance(result, float))
@icontract.ensure(lambda result: np.isfinite(result), "result must be finite")
def run_simulation_anti(
    model: DiscretizeModel,
    claim: ContingentClaim,
    seed: int,
    trials: int,
    simulator_name: str,
) -> float:
    """Run an antithetic Monte Carlo estimate with paired trajectories.

    Args:
        model: Discretized market model or simulation model state.
        claim: Contingent claim whose payoff is being priced.
        seed: Non-negative RNG seed.
        trials: Even number of Monte Carlo trajectories.
        simulator_name: Registry key selecting the seeded simulator.

    Returns:
        Finite antithetic Monte Carlo estimate.
    """
    half_trials = trials // 2
    res_anti = run_simulation(model, claim, seed, half_trials, True, simulator_name)
    res_reg = run_simulation(model, claim, seed, half_trials, False, simulator_name)

    return float((res_anti + res_reg) / 2.0)

@register_atom(witness_quick_sim_anti)
@icontract.require(lambda trials: trials > 0)
@icontract.require(lambda trials: trials % 2 == 0, "Trials must be even for antithetic variates")
@icontract.ensure(lambda result: isinstance(result, float), "result must be float")
@icontract.ensure(lambda result: np.isfinite(result), "result must be finite")
def quick_sim_anti(
    model: DiscretizeModel,
    claim: ContingentClaim,
    trials: int,
    simulator_name: str,
) -> float:
    """Convenience wrapper for antithetic Monte Carlo with a default seed.

    Args:
        model: Discretized market model or simulation model state.
        claim: Contingent claim whose payoff is being priced.
        trials: Even number of Monte Carlo trajectories.
        simulator_name: Registry key selecting the seeded simulator.

    Returns:
        Finite antithetic Monte Carlo estimate.
    """
    return run_simulation_anti(model, claim, 500, trials, simulator_name)
