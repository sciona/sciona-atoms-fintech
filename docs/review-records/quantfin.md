# quantfin review record

Provider slice: `sciona-atoms-fintech`
Bundle: `docs/review-bundles/quantfin_review_bundle.json`
Rows covered: 7
Ready rows: 6
Conditional rows: 1

## Authoritative sources
- `gatheral2006`: Local-volatility / vol-surface attribution.
- `glasserman2003`: Monte Carlo pricing attribution.
- `heston1993`: Characteristic-function option pricing attribution.
- `repo_quantfin`: Upstream implementation is mapped to the vendored quantfin repository.
- `thomas2011mwc64x`: External MWC64X documentation for the generator and stream-skipping design used by `rng_skip_d12`.

## Scope notes
The `tdma_solver_d12` row remains source-limited to the upstream repository record only; it remains reviewable but not fully trust-ready.
