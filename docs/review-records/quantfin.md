# quantfin review record

Provider slice: `sciona-atoms-fintech`
Bundle: `docs/review-bundles/quantfin_review_bundle.json`
Rows covered: 7
Ready rows: 7
Conditional rows: 0
Not-ready rows: 0

## Authoritative sources
- `gatheral2006`: Local-volatility / vol-surface attribution.
- `glasserman2003`: Monte Carlo pricing attribution.
- `heston1993`: Characteristic-function option pricing attribution.
- `repo_quantfin`: Upstream implementation is mapped to the vendored quantfin repository.
- `thomas2011mwc64x`: External MWC64X documentation for the generator and stream-skipping design used by `rng_skip_d12`.

## Scope notes
The pubrev-010 Monte Carlo row is publishable after direct source inspection against upstream `Quant.MonteCarlo`: `run_simulation` delegates to a seeded simulator, `run_simulation_anti` splits trials across antithetic and regular passes, and `quick_sim_anti` uses the fixed seed `500`.

The `tdma_solver_d12` row was reingested from upstream `Quant.Math.Utilities` with compact Python APIs: `tdma_solver(sub_diagonal, diagonal, super_diagonal, rhs)` mirrors `tdmaSolver aL bL cL dL`, and `cotraverse_vec(aggregator, length, vectors)` mirrors `cotraverseVec f l m`. Focused behavior tests cover a known tridiagonal solve, zero-pivot rejection, and index-wise vector co-traversal.
