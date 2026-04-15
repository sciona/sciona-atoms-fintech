from __future__ import annotations

"""Atom wrappers for Monte Carlo simulation with antithetic variates."""

import numpy as np
import icontract
from typing import Any, Callable, TypeAlias

from sciona.ghost.registry import register_atom
from .witnesses import (
    witness_avg,
    witness_evolve,
    witness_insertcf,
    witness_insertcflist,
    witness_maxstep,
    witness_process,
    witness_quicksim,
    witness_quicksimanti,
    witness_runmc,
    witness_runsim,
    witness_runsimulation,
    witness_runsimulationanti,
    witness_simulatestate,
)

import ctypes
import ctypes.util
from pathlib import Path


MonteCarloState: TypeAlias = dict[str, Any]
PricingModel: TypeAlias = dict[str, Any]
ClaimBasket: TypeAlias = list[Any] | dict[str, Any]
RandomState: TypeAlias = int | dict[str, Any]
ObservationValue: TypeAlias = float | int | bool | dict[str, Any] | list[float]
ObservationMap: TypeAlias = dict[float, ObservationValue]
CashFlow: TypeAlias = tuple[float, float] | dict[str, Any]
ClaimProcessor: TypeAlias = dict[str, Any]


# ---------------------------------------------------------------------------
# runmc  — execute a Monte Carlo computation
# ---------------------------------------------------------------------------

@register_atom(witness_runmc)
@icontract.require(lambda initState: initState is not None, "initState must be provided")
@icontract.require(lambda randState: randState is not None, "randState must be provided")
@icontract.ensure(lambda result: result is not None, "runmc must produce a result")
def runmc(
    evalState: Callable,
    evalStateT: Callable,
    flip: Callable,
    initState: MonteCarloState,
    lift: Callable,
    mc: Callable,
    randState: RandomState,
    sampleRVarTWith: Callable,
) -> float:
    """Run a Monte Carlo computation and return its final value.

    Evaluates the monadic Monte Carlo pipeline by sampling random
    variates through the state transformer, starting from the given
    initial and random-generator states.

    Args:
        evalState: Evaluate a stateful computation, discarding the state.
        evalStateT: Evaluate the inner state-transformer layer.
        flip: Flip argument order of a two-argument function.
        initState: Initial model state (observables and time).
        lift: Lift a computation into the monad-transformer stack.
        mc: The Monte Carlo computation to execute.
        randState: Initial random-generator state.
        sampleRVarTWith: Sample a random variable using a given lifter.

    Returns:
        Final numeric result of the Monte Carlo computation.
    """
    # Run a Monte Carlo computation: evaluate the monadic MC pipeline.
    result = evalState(
        evalStateT(sampleRVarTWith(lift, mc), randState),
        initState,
    )
    return float(result)


# ---------------------------------------------------------------------------
# runsimulation
# ---------------------------------------------------------------------------

@register_atom(witness_runsimulation)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def runsimulation(
    anti: bool,
    ccs: ClaimBasket,
    modl: PricingModel,
    run: Callable,
    runMC: Callable,
    seed: RandomState,
    trials: int,
    undefined: ObservationValue,
) -> float:
    """Run a full Monte Carlo simulation for a basket of contingent claims.

    Sets up the random state, constructs the simulation run, and calls
    runMC to compute the expected discounted payoff.

    Args:
        anti: Whether to use antithetic variates.
        ccs: Compiled contingent-claim basket.
        modl: Pricing model that implements the Discretize interface.
        run: Assembled simulation run (simulateState applied to args).
        runMC: Function that executes the Monte Carlo monad.
        seed: Initial random-number generator state.
        trials: Number of Monte Carlo trials.
        undefined: Placeholder initial observable (set during initialize).

    Returns:
        Estimated fair value as a float.
    """
    # Run a full MC simulation: use runMC to execute the assembled run.
    return float(runMC(run, seed, trials))


# ---------------------------------------------------------------------------
# runsimulationanti
# ---------------------------------------------------------------------------

@register_atom(witness_runsimulationanti)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def runsimulationanti(
    ccs: ClaimBasket,
    modl: PricingModel,
    runSim: Callable,
    seed: RandomState,
    trials: int,
) -> float:
    """Run a Monte Carlo simulation using antithetic variates for variance reduction.

    Splits the trial count in half, runs once with normal variates and
    once with flipped variates, and averages the two results.

    Args:
        ccs: Compiled contingent-claim basket.
        modl: Pricing model that implements the Discretize interface.
        runSim: Partial application of runSimulation with anti flag.
        seed: Initial random-number generator state.
        trials: Total number of trials (split evenly between normal and flipped).

    Returns:
        Variance-reduced estimated fair value as a float.
    """
    # Run antithetic simulation: average normal and flipped halves.
    half = trials // 2
    r1 = runSim(modl, ccs, seed, half, False)
    r2 = runSim(modl, ccs, seed, half, True)
    return float((r1 + r2) / 2.0)


# ---------------------------------------------------------------------------
# quicksim
# ---------------------------------------------------------------------------

@register_atom(witness_quicksim)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def quicksim(
    mdl: PricingModel,
    opts: ClaimBasket,
    pureMT: Callable,
    runSimulation: Callable,
    trials: int,
) -> float:
    """Run a quick Monte Carlo simulation with a default random seed.

    Convenience wrapper around runSimulation that uses pureMT(500) as
    the random state and disables antithetic variates.

    Args:
        mdl: Pricing model.
        opts: Contingent-claim basket.
        pureMT: Constructor for a Mersenne Twister generator from a seed.
        runSimulation: Full simulation runner.
        trials: Number of Monte Carlo trials.

    Returns:
        Estimated fair value as a float.
    """
    # Quick sim: use pureMT(500) as seed, no antithetic variates.
    return float(runSimulation(mdl, opts, pureMT(500), trials, False))


# ---------------------------------------------------------------------------
# quicksimanti
# ---------------------------------------------------------------------------

@register_atom(witness_quicksimanti)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def quicksimanti(
    mdl: PricingModel,
    opts: ClaimBasket,
    pureMT: Callable,
    runSimulationAnti: Callable,
    trials: int,
) -> float:
    """Run a quick Monte Carlo simulation with antithetic variates and a default seed.

    Convenience wrapper around runSimulationAnti that uses pureMT(500)
    as the random state.

    Args:
        mdl: Pricing model.
        opts: Contingent-claim basket.
        pureMT: Constructor for a Mersenne Twister generator from a seed.
        runSimulationAnti: Antithetic simulation runner.
        trials: Number of Monte Carlo trials.

    Returns:
        Variance-reduced estimated fair value as a float.
    """
    # Quick sim with antithetic: use pureMT(500) as seed.
    return float(runSimulationAnti(mdl, opts, pureMT(500), trials))


# ---------------------------------------------------------------------------
# evolve
# ---------------------------------------------------------------------------

@register_atom(witness_evolve)
@icontract.require(lambda mdl: mdl is not None, "mdl -- model must be provided")
@icontract.ensure(lambda result: result is not None, "evolve must produce a result")
def evolve(
    anti: bool,
    evolve: Callable,
    evolve_prime: Callable,
    get: Callable,
    maxStep: Callable,
    mdl: PricingModel,
    ms: float,
    t1: float,
    t2: float,
    timeDiff: Callable,
    timeOffset: Callable,
    unless: Callable,
) -> MonteCarloState:
    """Evolve the model state from current time to a target time.

    If the time gap exceeds the model's maximum step size, the
    evolution is broken into sub-steps.  Antithetic variates are
    applied when *anti* is True.

    Args:
        anti: Whether to flip random variates.
        evolve: Recursive reference for multi-step evolution.
        evolve_prime: Single-step evolution function (evolve').
        get: Retrieve current state from the monad.
        maxStep: Return the maximum allowed time step for the model.
        mdl: Pricing model.
        ms: Maximum step size returned by maxStep.
        t1: Current simulation time.
        t2: Target simulation time.
        timeDiff: Compute the difference between two times.
        timeOffset: Offset a time by a given amount.
        unless: Conditional guard (skip when times are equal).

    Returns:
        Updated monadic state after evolution.
    """
    # Evolve model state from t1 to t2, breaking into sub-steps if needed.
    # ms = maxStep(mdl), timeDiff gives gap, timeOffset advances time.
    dt = timeDiff(t2, t1)
    if dt <= 0:
        return get()
    if dt <= ms:
        return evolve_prime(mdl, anti, t1, t2)
    else:
        t_mid = timeOffset(t1, ms)
        evolve_prime(mdl, anti, t1, t_mid)
        return evolve(
            anti,
            evolve,
            evolve_prime,
            get,
            maxStep,
            mdl,
            ms,
            t_mid,
            t2,
            timeDiff,
            timeOffset,
            unless,
        )


# ---------------------------------------------------------------------------
# maxstep
# ---------------------------------------------------------------------------

@register_atom(witness_maxstep)
@icontract.require(lambda: True, "no preconditions for zero-parameter factory")
@icontract.ensure(lambda result: isinstance(result, float) and result > 0.0, "maxStep must be a positive float")
def maxstep() -> float:
    """Return the default maximum discretization time step.

    The default is 1/250, representing one trading day in a 250-day
    year.

    Returns:
        Maximum time step as a float (default 0.004).
    """
    # Default max step: 1/250 (one trading day).
    return 1.0 / 250.0


# ---------------------------------------------------------------------------
# simulatestate
# ---------------------------------------------------------------------------

@register_atom(witness_simulatestate)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def simulatestate(
    anti: bool,
    avg: Callable,
    ccb: list,
    modl: PricingModel,
    replicateM: Callable,
    singleTrial: Callable,
    trials: int,
) -> float:
    """Simulate the discounted payoff for a contingent-claim basket.

    Runs *trials* independent paths, each initializing the model,
    processing cash flows, and discounting.  The results are averaged.

    Args:
        anti: Whether to use antithetic variates.
        avg: Averaging function over trial results.
        ccb: List of contingent-claim processors (observation times and payoffs).
        modl: Pricing model.
        replicateM: Replicate a monadic action a given number of times.
        singleTrial: A single trial computation (initialize then process).
        trials: Number of independent trials to run.

    Returns:
        Average discounted payoff across all trials.
    """
    # Simulate: replicate singleTrial 'trials' times and average.
    results = replicateM(trials, singleTrial)
    return float(avg(trials, results))


# ---------------------------------------------------------------------------
# runsim  — convenience wrapper
# ---------------------------------------------------------------------------

@register_atom(witness_runsim)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def runsim(
    ccs: ClaimBasket,
    div: Callable,
    modl: PricingModel,
    runSimulation: Callable,
    seed: RandomState,
    trials: int,
    x: bool,
) -> float:
    """Run a simulation variant with a given antithetic flag.

    Helper used by runSimulationAnti to execute half the trials with
    a specific variate direction.

    Args:
        ccs: Compiled contingent-claim basket.
        div: Integer division function.
        modl: Pricing model.
        runSimulation: Full simulation runner.
        seed: Random-generator state.
        trials: Number of trials (will be halved internally).
        x: Antithetic flag for this half of the run.

    Returns:
        Estimated fair value for this half-run.
    """
    # Run simulation with halved trials and the given antithetic flag.
    half_trials = div(trials, 2)
    return float(runSimulation(modl, ccs, seed, half_trials, x))


# ---------------------------------------------------------------------------
# process  — full cash-flow processing (variant 1: with remaining CFs)
# ---------------------------------------------------------------------------

@register_atom(witness_process)
@icontract.require(lambda discCFs: isinstance(discCFs, (int, float)), "discCFs must be numeric")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def process(
    allcfs: list,
    amt: float,
    anti: bool,
    c: ClaimProcessor,
    ccs: list,
    cfList: list,
    cfs: list,
    cft: float,
    d: float,
    discCFs: float,
    discount: Callable,
    evolve: Callable,
    flip: Callable,
    foldl_prime: Callable,
    fst: Callable,
    gets: Callable,
    insert: Callable,
    insertCF: Callable,
    insertCFList: Callable,
    map: Callable,
    mf: list,
    modl: PricingModel,
    newCFs: list,
    obs: ObservationValue,
    obsMap: ObservationMap,
    obsMap_prime: ObservationMap,
    process: Callable,
    t: float,
    xs: list,
) -> float:
    """Process cash flows by interleaving observation and payment times.

    When the next cash-flow time precedes the next observation time,
    the model evolves to that cash-flow time, discounts the payment,
    and accumulates.  Otherwise it evolves to the observation time,
    records the observable, generates new cash flows, and recurses.

    Args:
        allcfs: Full remaining cash-flow list.
        amt: Cash-flow amount at the current time.
        anti: Whether to use antithetic variates.
        c: Current contingent-claim processor.
        ccs: Remaining processors after the current one.
        cfList: Intermediate cash-flow list workspace.
        cfs: Remaining cash flows after the current one.
        cft: Time of the current cash flow.
        d: Discount factor at the current time.
        discCFs: Running sum of discounted cash flows.
        discount: Discounting function from the model.
        evolve: Model evolution function.
        flip: Argument-order flipper.
        foldl_prime: Strict left fold.
        fst: Extract the first element of a pair.
        gets: Extract a field from the monadic state.
        insert: Map insertion function.
        insertCF: Insert a single cash flow in sorted order.
        insertCFList: Insert a list of cash flows in sorted order.
        map: Map a function over a list.
        mf: Payout functions for the current processor.
        modl: Pricing model.
        newCFs: Newly generated cash flows from the current observation.
        obs: Current observable value.
        obsMap: Map of observation times to observable values.
        obsMap_prime: Updated observation map after insertion.
        process: Recursive reference to this function.
        t: Current observation time.
        xs: Workspace list for fold operations.

    Returns:
        Total discounted cash-flow value for this trial path.
    """
    # Process cash flows: interleave observation and payment times.
    # If next CF time < next observation time, discount the CF and accumulate.
    # Otherwise, evolve to observation time and generate new CFs.
    if allcfs and (not ccs or cft <= t):
        # Process the cash flow
        evolve(modl, anti, cft, cft)
        d_val = discount(modl, cft)
        new_disc = discCFs + d_val * amt
        return float(process(anti, modl, ccs, cfs, obsMap, new_disc))
    else:
        # Process the observation
        evolve(modl, anti, t, t)
        obs_val = gets(modl)
        obsMap_new = insert(t, obs_val, obsMap)
        new_cfs_list = list(map(lambda pf: pf(obsMap_new), mf))
        merged = insertCFList(cfList, new_cfs_list)
        return float(process(anti, modl, ccs, merged, obsMap_new, discCFs))


# ---------------------------------------------------------------------------
# process  — variant 2: processors remain, no pending CFs
# ---------------------------------------------------------------------------

@register_atom(witness_process)
@icontract.require(lambda discCFs: isinstance(discCFs, (int, float)), "discCFs must be numeric")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def process(
    anti: bool,
    ccs: list,
    cfList: list,
    discCFs: float,
    evolve: Callable,
    flip: Callable,
    foldl_prime: Callable,
    fst: Callable,
    gets: Callable,
    insert: Callable,
    insertCF: Callable,
    insertCFList: Callable,
    map: Callable,
    mf: list,
    modl: PricingModel,
    newCFs: list,
    obs: ObservationValue,
    obsMap: ObservationMap,
    obsMap_prime: ObservationMap,
    process: Callable,
    t: float,
    xs: list,
) -> float:
    """Process remaining claim processors when no cash flows are pending.

    Evolves to each observation time, records the observable, generates
    new cash flows via the payout functions, and recurses.

    Args:
        anti: Whether to use antithetic variates.
        ccs: Remaining processors.
        cfList: Intermediate cash-flow list workspace.
        discCFs: Running sum of discounted cash flows.
        evolve: Model evolution function.
        flip: Argument-order flipper.
        foldl_prime: Strict left fold.
        fst: Extract the first element of a pair.
        gets: Extract a field from the monadic state.
        insert: Map insertion function.
        insertCF: Insert a single cash flow in sorted order.
        insertCFList: Insert a list of cash flows in sorted order.
        map: Map a function over a list.
        mf: Payout functions for the current processor.
        modl: Pricing model.
        newCFs: Newly generated cash flows from the current observation.
        obs: Current observable value.
        obsMap: Map of observation times to observable values.
        obsMap_prime: Updated observation map after insertion.
        process: Recursive reference to this function.
        t: Current observation time.
        xs: Workspace list for fold operations.

    Returns:
        Total discounted cash-flow value for this trial path.
    """
    # Process remaining processors when no cash flows are pending.
    # Evolve to observation time, record observable, generate new CFs, recurse.
    evolve(modl, anti, t, t)
    obs_val = gets(modl)
    obsMap_new = insert(t, obs_val, obsMap)
    new_cfs_list = list(map(lambda pf: pf(obsMap_new), mf))
    merged = insertCFList(cfList, new_cfs_list)
    return float(process(anti, modl, ccs, merged, obsMap_new, discCFs))


# ---------------------------------------------------------------------------
# process  — variant 3: only cash flows remain
# ---------------------------------------------------------------------------

@register_atom(witness_process)
@icontract.require(lambda discCFs: isinstance(discCFs, float), "discCFs must be a float")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def process(
    anti: bool,
    cf: CashFlow,
    cfAmount: Callable,
    cfTime: Callable,
    cfs: list,
    d: float,
    discCFs: float,
    discount: Callable,
    evolve: Callable,
    modl: PricingModel,
    obsMap: ObservationMap,
    process: Callable,
) -> float:
    """Process remaining cash flows when no more processors exist.

    Evolves to each cash-flow time, discounts the amount, and
    accumulates into the running total.

    Args:
        anti: Whether to use antithetic variates.
        cf: Current cash-flow object.
        cfAmount: Extract the amount from a cash-flow object.
        cfTime: Extract the time from a cash-flow object.
        cfs: Remaining cash flows.
        d: Discount factor at the current cash-flow time.
        discCFs: Running sum of discounted cash flows.
        discount: Discounting function from the model.
        evolve: Model evolution function.
        modl: Pricing model.
        obsMap: Observation map (unused but passed for consistency).
        process: Recursive reference to this function.

    Returns:
        Total discounted cash-flow value for this trial path.
    """
    # Process remaining cash flows when no more processors exist.
    # Evolve to CF time, discount the amount, accumulate, recurse.
    cf_t = cfTime(cf)
    cf_a = cfAmount(cf)
    evolve(modl, anti, cf_t, cf_t)
    d_val = discount(modl, cf_t)
    new_disc = discCFs + d_val * cf_a
    if cfs:
        return float(process(anti, modl, cfs, obsMap, new_disc))
    return float(new_disc)


# ---------------------------------------------------------------------------
# process  — variant 4: base case
# ---------------------------------------------------------------------------

@register_atom(witness_process)
@icontract.require(lambda discCFs: isinstance(discCFs, float), "discCFs must be a float")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def process(
    discCFs: float,
    return_val: Callable,
) -> float:
    """Return the accumulated discounted cash flows (base case).

    When no processors or cash flows remain, the accumulated total is
    returned as the trial result.

    Args:
        discCFs: Total accumulated discounted cash flows.
        return_val: Monadic return that wraps the value.

    Returns:
        Final discounted value for this trial.
    """
    # Base case: return the accumulated discounted cash flows.
    return float(discCFs)


# ---------------------------------------------------------------------------
# insertcf  — insert a cash flow in sorted order (recursive case)
# ---------------------------------------------------------------------------

@register_atom(witness_insertcf)
@icontract.require(lambda cfs: isinstance(cfs, list), "cfs must be a list")
@icontract.ensure(lambda result: isinstance(result, list), "result must be a list")
def insertcf(
    amt: float,
    amt_prime: float,
    cfs: list,
    insertCF: Callable,
    otherwise: list,
    t: float,
    t_prime: float,
) -> list:
    """Insert a cash flow into a time-sorted list (recursive case).

    Compares the new cash-flow time *t* with the head of the list
    (*t_prime*).  If the new time is later, the head is kept and
    insertion recurses on the tail.

    Args:
        amt: Amount of the cash flow to insert.
        amt_prime: Amount of the head cash flow.
        cfs: Tail of the existing cash-flow list.
        insertCF: Recursive reference to this function.
        otherwise: Result list when the new CF goes before the head.
        t: Time of the cash flow to insert.
        t_prime: Time of the head cash flow.

    Returns:
        Cash-flow list with the new entry inserted in time order.
    """
    # Insert a CF in sorted order (recursive case).
    # If new time t <= head time t_prime, insert before head.
    if t <= t_prime:
        return otherwise  # pre-computed: [new_cf] + [(t_prime, amt_prime)] + cfs
    else:
        # Head stays, recurse on tail
        return [(t_prime, amt_prime)] + insertCF(t, amt, cfs)


# ---------------------------------------------------------------------------
# insertcf  — base case (empty list)
# ---------------------------------------------------------------------------

@register_atom(witness_insertcf)
@icontract.require(lambda cf: cf is not None, "cf must not be None")
@icontract.ensure(lambda result: isinstance(result, list) and len(result) == 1, "result must be a single-element list")
def insertcf(
    cf: CashFlow,
) -> list:
    """Insert a cash flow into an empty list (base case).

    Args:
        cf: Cash-flow object to wrap in a singleton list.

    Returns:
        Single-element list containing the cash flow.
    """
    # Base case: wrap the single CF in a list.
    return [cf]


# ---------------------------------------------------------------------------
# avg
# ---------------------------------------------------------------------------

@register_atom(witness_avg)
@icontract.require(lambda trials: isinstance(trials, int) and trials > 0, "trials must be a positive integer")
@icontract.ensure(lambda result: isinstance(result, float), "result must be a float")
def avg(
    fromIntegral: Callable,
    sum: Callable,
    trials: int,
    v: list,
) -> float:
    """Compute the arithmetic mean of trial results.

    Divides the sum of all trial values by the trial count.

    Args:
        fromIntegral: Convert an integer to a fractional type.
        sum: Sum function over a list of numbers.
        trials: Number of trials.
        v: List of per-trial result values.

    Returns:
        Arithmetic mean of the trial values.
    """
    # Arithmetic mean: sum(v) / fromIntegral(trials)
    return float(sum(v) / fromIntegral(trials))


# ---------------------------------------------------------------------------
# insertcflist  — insert multiple CFs (variant 1)
# ---------------------------------------------------------------------------

@register_atom(witness_insertcflist)
@icontract.require(lambda cfList: isinstance(cfList, list), "cfList must be a list")
@icontract.ensure(lambda result: isinstance(result, list), "result must be a list")
def insertcflist(
    cfList: list,
    flip: Callable,
    foldl_prime: Callable,
    insertCF: Callable,
    xs: list,
) -> list:
    """Insert a list of cash flows into an existing sorted list.

    Uses a strict left fold to insert each new cash flow one at a
    time, maintaining sorted order.

    Args:
        cfList: Existing sorted cash-flow list.
        flip: Argument-order flipper.
        foldl_prime: Strict left fold.
        insertCF: Single cash-flow insertion function.
        xs: List of new cash flows to insert.

    Returns:
        Merged sorted cash-flow list.
    """
    # Insert each new CF from xs into cfList using a strict left fold.
    result = cfList
    for x_item in xs:
        result = insertCF(x_item, result)
    return result


# ---------------------------------------------------------------------------
# insertcflist  — variant 2
# ---------------------------------------------------------------------------

@register_atom(witness_insertcflist)
@icontract.require(lambda xs: isinstance(xs, list), "xs must be a list")
@icontract.ensure(lambda result: isinstance(result, list), "result must be a list")
def insertcflist(
    cfList: list,
    flip: Callable,
    foldl_prime: Callable,
    insertCF: Callable,
    xs: list,
) -> list:
    """Insert a list of cash flows into an existing sorted list (alternate witness).

    Identical logic to the first variant; registered under the same
    witness for pattern-matching flexibility.

    Args:
        cfList: Existing sorted cash-flow list.
        flip: Argument-order flipper.
        foldl_prime: Strict left fold.
        insertCF: Single cash-flow insertion function.
        xs: List of new cash flows to insert.

    Returns:
        Merged sorted cash-flow list.
    """
    # Insert each new CF from xs into cfList using a strict left fold.
    result = cfList
    for x_item in xs:
        result = insertCF(x_item, result)
    return result


# ---------------------------------------------------------------------------
# FFI bindings (auto-generated, kept for reference)
# ---------------------------------------------------------------------------

def _runmc_ffi(evalState, evalStateT, flip, initState, lift, mc, randState, sampleRVarTWith):
    """Wrapper that calls the Haskell version of runmc."""
    _lib = ctypes.CDLL("./runmc.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 8
    _func.restype = ctypes.c_void_p
    return _func(evalState, evalStateT, flip, initState, lift, mc, randState, sampleRVarTWith)

def _runsimulation_ffi(anti, ccs, modl, run, runMC, seed, trials, undefined):
    """Wrapper that calls the Haskell version of runsimulation."""
    _lib = ctypes.CDLL("./runsimulation.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 8
    _func.restype = ctypes.c_void_p
    return _func(anti, ccs, modl, run, runMC, seed, trials, undefined)

def _runsimulationanti_ffi(ccs, modl, runSim, seed, trials):
    """Call the Haskell version of run-simulation-anti. Passes arguments through and returns the result."""
    _lib = ctypes.CDLL("./runsimulationanti.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(ccs, modl, runSim, seed, trials)

def _quicksim_ffi(mdl, opts, pureMT, runSimulation, trials):
    """Wrapper that calls the Haskell version of quicksim."""
    _lib = ctypes.CDLL("./quicksim.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(mdl, opts, pureMT, runSimulation, trials)

def _quicksimanti_ffi(mdl, opts, pureMT, runSimulationAnti, trials):
    """Wrapper that calls the Haskell version of quicksimanti."""
    _lib = ctypes.CDLL("./quicksimanti.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(mdl, opts, pureMT, runSimulationAnti, trials)

def _evolve_ffi(anti, evolve, evolve_prime, get, maxStep, mdl, ms, t1, t2, timeDiff, timeOffset, unless):
    """Wrapper that calls the Haskell version of evolve."""
    _lib = ctypes.CDLL("./evolve.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 12
    _func.restype = ctypes.c_void_p
    return _func(anti, evolve, evolve_prime, get, maxStep, mdl, ms, t1, t2, timeDiff, timeOffset, unless)

def _maxstep_ffi():
    """Wrapper that calls the Haskell version of maxstep."""
    _lib = ctypes.CDLL("./maxstep.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.restype = ctypes.c_void_p
    return _func()

def _simulatestate_ffi(anti, avg, ccb, modl, replicateM, singleTrial, trials):
    """Wrapper that calls the Haskell version of simulatestate."""
    _lib = ctypes.CDLL("./simulatestate.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 7
    _func.restype = ctypes.c_void_p
    return _func(anti, avg, ccb, modl, replicateM, singleTrial, trials)

def _runsim_ffi(ccs, div, modl, runSimulation, seed, trials, x):
    """Wrapper that calls the Haskell version of runsim."""
    _lib = ctypes.CDLL("./runsim.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 7
    _func.restype = ctypes.c_void_p
    return _func(ccs, div, modl, runSimulation, seed, trials, x)

def _process_full_ffi(allcfs, amt, anti, c, ccs, cfList, cfs, cft, d, discCFs, discount, evolve, flip, foldl_prime, fst, gets, insert, insertCF, insertCFList, map, mf, modl, newCFs, obs, obsMap, obsMap_prime, process, t, xs):
    """Wrapper that calls the Haskell version of process (full variant)."""
    _lib = ctypes.CDLL("./process.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 29
    _func.restype = ctypes.c_void_p
    return _func(allcfs, amt, anti, c, ccs, cfList, cfs, cft, d, discCFs, discount, evolve, flip, foldl_prime, fst, gets, insert, insertCF, insertCFList, map, mf, modl, newCFs, obs, obsMap, obsMap_prime, process, t, xs)

def _process_no_cfs_ffi(anti, ccs, cfList, discCFs, evolve, flip, foldl_prime, fst, gets, insert, insertCF, insertCFList, map, mf, modl, newCFs, obs, obsMap, obsMap_prime, process, t, xs):
    """Wrapper that calls the Haskell version of process (no pending CFs)."""
    _lib = ctypes.CDLL("./process.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 22
    _func.restype = ctypes.c_void_p
    return _func(anti, ccs, cfList, discCFs, evolve, flip, foldl_prime, fst, gets, insert, insertCF, insertCFList, map, mf, modl, newCFs, obs, obsMap, obsMap_prime, process, t, xs)

def _process_cfs_only_ffi(anti, cf, cfAmount, cfTime, cfs, d, discCFs, discount, evolve, modl, obsMap, process):
    """Wrapper that calls the Haskell version of process (CFs only)."""
    _lib = ctypes.CDLL("./process.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 12
    _func.restype = ctypes.c_void_p
    return _func(anti, cf, cfAmount, cfTime, cfs, d, discCFs, discount, evolve, modl, obsMap, process)

def _process_base_ffi(discCFs, return_val):
    """Wrapper that calls the Haskell version of process (base case)."""
    _lib = ctypes.CDLL("./process.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 2
    _func.restype = ctypes.c_void_p
    return _func(discCFs, return_val)

def _insertcf_ffi(amt, amt_prime, cfs, insertCF, otherwise, t, t_prime):
    """Wrapper that calls the Haskell version of insertcf (recursive)."""
    _lib = ctypes.CDLL("./insertcf.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 7
    _func.restype = ctypes.c_void_p
    return _func(amt, amt_prime, cfs, insertCF, otherwise, t, t_prime)

def _insertcf_base_ffi(cf):
    """Wrapper that calls the Haskell version of insertcf (base case)."""
    _lib = ctypes.CDLL("./insertcf.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p]
    _func.restype = ctypes.c_void_p
    return _func(cf)

def _avg_ffi(fromIntegral, sum, trials, v):
    """Wrapper that calls the Haskell version of avg."""
    _lib = ctypes.CDLL("./avg.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 4
    _func.restype = ctypes.c_void_p
    return _func(fromIntegral, sum, trials, v)

def _insertcflist_ffi(cfList, flip, foldl_prime, insertCF, xs):
    """Wrapper that calls the Haskell version of insertcflist."""
    _lib = ctypes.CDLL("./insertcflist.so")
    _func_name = 'placeholder'
    _func = _lib[_func_name]
    _func.argtypes = [ctypes.c_void_p] * 5
    _func.restype = ctypes.c_void_p
    return _func(cfList, flip, foldl_prime, insertCF, xs)
