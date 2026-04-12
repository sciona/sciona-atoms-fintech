from __future__ import annotations
from ageoa.ghost.abstract import AbstractArray, AbstractScalar, AbstractDistribution, AbstractSignal


def witness_runmc(evalState: AbstractArray, evalStateT: AbstractArray, flip: AbstractArray, initState: AbstractArray, lift: AbstractArray, mc: AbstractArray, randState: AbstractArray, sampleRVarTWith: AbstractArray) -> AbstractArray:
    """Shape-and-type check for runmc. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=evalState.shape,
        dtype="float64",
    )
    return result

def witness_runsimulation(anti: AbstractArray, ccs: AbstractArray, modl: AbstractArray, run: AbstractArray, runMC: AbstractArray, seed: AbstractArray, trials: AbstractArray, undefined: AbstractArray) -> AbstractArray:
    """Shape-and-type check for runsimulation. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=anti.shape,
        dtype="float64",
    )
    return result

def witness_runsimulationanti(ccs: AbstractArray, modl: AbstractArray, runSim: AbstractArray, seed: AbstractArray, trials: AbstractArray) -> AbstractArray:
    """Shape-and-type check for runsimulationanti. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=ccs.shape,
        dtype="float64",
    )
    return result

def witness_quicksim(mdl: AbstractArray, opts: AbstractArray, pureMT: AbstractArray, runSimulation: AbstractArray, trials: AbstractArray) -> AbstractArray:
    """Shape-and-type check for quicksim. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=mdl.shape,
        dtype="float64",
    )
    return result

def witness_quicksimanti(mdl: AbstractArray, opts: AbstractArray, pureMT: AbstractArray, runSimulationAnti: AbstractArray, trials: AbstractArray) -> AbstractArray:
    """Shape-and-type check for quicksimanti. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=mdl.shape,
        dtype="float64",
    )
    return result

def witness_evolve(anti: AbstractArray, evolve: AbstractArray, evolve_prime: AbstractArray, get: AbstractArray, maxStep: AbstractArray, mdl: AbstractArray, ms: AbstractArray, t1: AbstractArray, t2: AbstractArray, timeDiff: AbstractArray, timeOffset: AbstractArray, unless: AbstractArray) -> AbstractArray:
    """Shape-and-type check for evolve. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=anti.shape,
        dtype="float64",
    )
    return result

def witness_maxstep() -> AbstractArray:
    """Shape-and-type check for maxstep. Returns output metadata without running the real computation."""
    return AbstractArray(shape=(1,), dtype="float64")

def witness_simulatestate(anti: AbstractArray, avg: AbstractArray, ccb: AbstractArray, modl: AbstractArray, replicateM: AbstractArray, singleTrial: AbstractArray, trials: AbstractArray) -> AbstractArray:
    """Shape-and-type check for simulatestate. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=anti.shape,
        dtype="float64",
    )
    return result

def witness_runsim(ccs: AbstractArray, div: AbstractArray, modl: AbstractArray, runSimulation: AbstractArray, seed: AbstractArray, trials: AbstractArray, x: AbstractArray) -> AbstractArray:
    """Shape-and-type check for runsim. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=ccs.shape,
        dtype="float64",
    )
    return result

def witness_process(allcfs: AbstractArray, amt: AbstractArray, anti: AbstractArray, c: AbstractArray, ccs: AbstractArray, cfList: AbstractArray, cfs: AbstractArray, cft: AbstractArray, d: AbstractArray, discCFs: AbstractArray, discount: AbstractArray, evolve: AbstractArray, flip: AbstractArray, foldl_prime: AbstractArray, fst: AbstractArray, gets: AbstractArray, insert: AbstractArray, insertCF: AbstractArray, insertCFList: AbstractArray, map: AbstractArray, mf: AbstractArray, modl: AbstractArray, newCFs: AbstractArray, obs: AbstractArray, obsMap: AbstractArray, obsMap_prime: AbstractArray, process: AbstractArray, t: AbstractArray, xs: AbstractArray) -> AbstractArray:
    """Shape-and-type check for process. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=allcfs.shape,
        dtype="float64",
    )
    return result

def witness_process(anti: AbstractArray, ccs: AbstractArray, cfList: AbstractArray, discCFs: AbstractArray, evolve: AbstractArray, flip: AbstractArray, foldl_prime: AbstractArray, fst: AbstractArray, gets: AbstractArray, insert: AbstractArray, insertCF: AbstractArray, insertCFList: AbstractArray, map: AbstractArray, mf: AbstractArray, modl: AbstractArray, newCFs: AbstractArray, obs: AbstractArray, obsMap: AbstractArray, obsMap_prime: AbstractArray, process: AbstractArray, t: AbstractArray, xs: AbstractArray) -> AbstractArray:
    """Shape-and-type check for process. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=anti.shape,
        dtype="float64",
    )
    return result

def witness_process(anti: AbstractArray, cf: AbstractArray, cfAmount: AbstractArray, cfTime: AbstractArray, cfs: AbstractArray, d: AbstractArray, discCFs: AbstractArray, discount: AbstractArray, evolve: AbstractArray, modl: AbstractArray, obsMap: AbstractArray, process: AbstractArray) -> AbstractArray:
    """Shape-and-type check for process. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=anti.shape,
        dtype="float64",
    )
    return result

def witness_process(discCFs: AbstractArray, return_val: AbstractArray) -> AbstractArray:
    """Shape-and-type check for process. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=discCFs.shape,
        dtype="float64",
    )
    return result

def witness_insertcf(amt: AbstractArray, amt_prime: AbstractArray, cfs: AbstractArray, insertCF: AbstractArray, otherwise: AbstractArray, t: AbstractArray, t_prime: AbstractArray) -> AbstractArray:
    """Shape-and-type check for insertcf. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=amt.shape,
        dtype="float64",
    )
    return result

def witness_insertcf(cf: AbstractArray) -> AbstractArray:
    """Shape-and-type check for insertcf. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=cf.shape,
        dtype="float64",
    )
    return result

def witness_avg(fromIntegral: AbstractArray, sum: AbstractArray, trials: AbstractArray, v: AbstractArray) -> AbstractArray:
    """Shape-and-type check for avg. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=fromIntegral.shape,
        dtype="float64",
    )
    return result

def witness_insertcflist(cfList: AbstractArray, flip: AbstractArray, foldl_prime: AbstractArray, insertCF: AbstractArray, xs: AbstractArray) -> AbstractArray:
    """Shape-and-type check for insertcflist. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=cfList.shape,
        dtype="float64",
    )
    return result

def witness_insertcflist(cfList: AbstractArray, flip: AbstractArray, foldl_prime: AbstractArray, insertCF: AbstractArray, xs: AbstractArray) -> AbstractArray:
    """Shape-and-type check for insertcflist. Returns output metadata without running the real computation."""
    result = AbstractArray(
        shape=cfList.shape,
        dtype="float64",
    )
    return result
