# quantfin review record

Provider slice: `sciona-atoms-fintech`
Bundle: `docs/review-bundles/quantfin_review_bundle.json`
Rows covered: 7
Ready rows: 6
Conditional rows: 0
Not-ready rows: 1

## Authoritative sources
- `gatheral2006`: Local-volatility / vol-surface attribution.
- `glasserman2003`: Monte Carlo pricing attribution.
- `heston1993`: Characteristic-function option pricing attribution.
- `repo_quantfin`: Upstream implementation is mapped to the vendored quantfin repository.
- `thomas2011mwc64x`: External MWC64X documentation for the generator and stream-skipping design used by `rng_skip_d12`.

## Scope notes
The pubrev-010 Monte Carlo row is publishable after direct source inspection against upstream `Quant.MonteCarlo`: `run_simulation` delegates to a seeded simulator, `run_simulation_anti` splits trials across antithetic and regular passes, and `quick_sim_anti` uses the fixed seed `500`.

The `tdma_solver_d12` row remains unpublished. Upstream `Quant.Math.Utilities` exposes compact `tdmaSolver aL bL cL dL` and `cotraverseVec f l m` APIs, while the generated Python atoms expose translation-internal helper arguments. Keep this row in remediation until the public Python call surfaces and focused behavior tests match the source contract.
