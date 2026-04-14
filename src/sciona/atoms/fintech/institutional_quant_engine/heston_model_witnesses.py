from __future__ import annotations

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractScalar, AbstractSignal


def witness_simulate_heston_paths(
    initial_state: AbstractArray,
    n_steps: AbstractScalar,
) -> AbstractArray:
    """Describe the simulated Heston path tensor produced from the initial state."""
    _ = n_steps
    result = AbstractArray(
        shape=initial_state.shape,
        dtype="float64",)
    
    return result

from sciona.ghost.abstract import AbstractArray, AbstractDistribution, AbstractMCMCTrace, AbstractRNGState, AbstractScalar, AbstractSignal


def witness_hestonpathsampler(trace: AbstractMCMCTrace, target: AbstractDistribution, rng: AbstractRNGState) -> tuple[AbstractMCMCTrace, AbstractRNGState]:
    """Shape-and-type check for mcmc sampler: heston path sampler. Returns output metadata without running the real computation."""
    if trace.param_dims != target.event_shape:
        raise ValueError(
            f"param_dims {trace.param_dims} vs event_shape {target.event_shape}"
        )
        
    return trace.step(accepted=True), rng.advance(n_draws=1)
