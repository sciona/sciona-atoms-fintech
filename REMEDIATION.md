# REMEDIATION

This file tracks provider publishability-review atoms that should remain unpublished until the
implementation, public name, metadata, and behavior tests describe the same
contract.

## Quantfin

### `sciona.atoms.fintech.quantfin.tdma_solver_d12.tdmasolver`

Status: keep unpublished for now.

Why it is blocked:
- Upstream `Quant.Math.Utilities.tdmaSolver` accepts four vectors: sub-diagonal, main diagonal, super-diagonal, and right-hand side.
- The generated Python atom exposes many translation-internal helper/workspace arguments (`forM_`, `fromList`, `read`, `write`, `x`, `xn`, and related intermediates).
- The implementation computes a Thomas-algorithm solution from selected list arguments, but the public call surface does not match the upstream source contract and is not suitable for catalog publication.

Proposed fixes:
1. Add a source-aligned wrapper that accepts only the four coefficient/right-hand-side vectors, validates equal lengths and non-zero pivots, and delegates to a tested Thomas sweep.
2. Add deterministic tests against a known tridiagonal linear system and singular-pivot rejection.
3. Reenter publication review only after references, review bundle source paths, uncertainty notes if needed, and behavior tests all describe the same public API.

### `sciona.atoms.fintech.quantfin.tdma_solver_d12.cotraversevec`

Status: keep unpublished for now.

Why it is blocked:
- Upstream `Quant.Math.Utilities.cotraverseVec` accepts an aggregation function, output length, and functor-wrapped unboxed vectors.
- The generated Python atom exposes helper arguments (`enumFromN`, `fmap`, and `map`) that are implementation mechanics rather than the upstream public API.
- The behavior can emulate co-traversal when callers provide those helpers, but that is not source-aligned enough for publication.

Proposed fixes:
1. Replace the generated call surface with a direct Python API for the aggregation function, output length, and wrapped vectors.
2. Add tests proving index-wise aggregation across multiple vectors and preserving output length/order.
3. Reenter publication review only after the review bundle no longer marks this row as `semantic_drift`.

## Institutional Quant Engine

### `sciona.atoms.fintech.institutional_quant_engine.fractional_diff.fractional_differentiator`

Status: keep unpublished for now.

Why it is blocked:
- The current implementation is not identity-preserving for `d=0`.
- With one retained weight, the loop assigns `series[i - 1]` to output index `i`, so the result is shifted rather than matching the input series.
- Publishing under the current name would imply standard fractional differentiation semantics that the implementation does not yet satisfy.

Proposed fixes:
1. Rework the fixed-width fractional-differentiation window so the current observation is included with the correct weight.
2. Add behavior tests covering `d=0` identity behavior, deterministic low-order examples, and threshold truncation.
3. Reenter review only after the corrected source path, references, uncertainty notes, and bundle row all agree.

### `sciona.atoms.fintech.institutional_quant_engine.pin_model.pinlikelihoodevaluation`

Status: keep unpublished for now.

Why it is blocked:
- The implementation returns a summed squared-error score against expected buy and sell counts.
- The public name and docstring claim likelihood evaluation for the Probability of Informed Trading model.
- A squared-error objective is not a PIN likelihood or log-likelihood and should not be published as one.

Proposed fixes:
1. Implement the Easley-style PIN likelihood or log-likelihood with explicit parameter-domain validation.
2. Add tests for scalar and vector buy/sell counts, invalid parameters, and finite likelihood behavior.
3. If squared-error scoring is the intended primitive, rename the atom and rewrite its metadata instead of publishing it as PIN likelihood.

### `sciona.atoms.fintech.institutional_quant_engine.pin_model.pinlikelihoodevaluator`

Status: keep unpublished for now.

Why it is blocked:
- This callable has the same semantic issue as `pinlikelihoodevaluation`.
- It accepts a dictionary parameterization but still returns squared error rather than likelihood or log-likelihood.

Proposed fixes:
1. Share the corrected PIN likelihood implementation with `pinlikelihoodevaluation`, or intentionally split the APIs with distinct names.
2. Add regression tests proving both call surfaces compute the same likelihood semantics for equivalent parameters.
3. Keep this row out of the publishable catalog until the behavior and public contract align.

### `sciona.atoms.fintech.institutional_quant_engine.wash_trade.detect_wash_trade_rings`

Status: keep unpublished for now.

Why it is blocked:
- The current implementation checks adjacency-matrix powers only up to cycle length 5.
- Larger directed wash-trading rings are silently missed despite the general detector name.
- The return type is a float mask even though the docstring describes a Boolean participant mask.

Proposed fixes:
1. Replace bounded power scanning with complete directed-cycle detection, or narrow the public contract to explicitly detect only bounded-size rings.
2. Return a Boolean mask if that is the intended public interface, or document and test numeric scores if a float output is intended.
3. Add tests for cycles of length 2, 3, 5, and greater than 5 before reentering publication review.
