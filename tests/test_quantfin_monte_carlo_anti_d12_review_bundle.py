from __future__ import annotations

import importlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles" / "quantfin_review_bundle.json"
MONTE_CARLO_MODULE = "sciona.atoms.fintech.quantfin.monte_carlo_anti_d12"
EXPECTED_ATOM_KEYS = {
    f"{MONTE_CARLO_MODULE}.avg",
    f"{MONTE_CARLO_MODULE}.evolve",
    f"{MONTE_CARLO_MODULE}.insertcf_recursive",
    f"{MONTE_CARLO_MODULE}.insertcf_singleton",
    f"{MONTE_CARLO_MODULE}.insertcflist_fold",
    f"{MONTE_CARLO_MODULE}.insertcflist_fold_alt",
    f"{MONTE_CARLO_MODULE}.maxstep",
    f"{MONTE_CARLO_MODULE}.process_base_case",
    f"{MONTE_CARLO_MODULE}.process_with_cashflows_only",
    f"{MONTE_CARLO_MODULE}.process_with_observation_only",
    f"{MONTE_CARLO_MODULE}.process_with_pending_cashflows",
    f"{MONTE_CARLO_MODULE}.quicksim",
    f"{MONTE_CARLO_MODULE}.quicksimanti",
    f"{MONTE_CARLO_MODULE}.runmc",
    f"{MONTE_CARLO_MODULE}.runsim",
    f"{MONTE_CARLO_MODULE}.runsimulation",
    f"{MONTE_CARLO_MODULE}.runsimulationanti",
    f"{MONTE_CARLO_MODULE}.simulatestate",
}
EXPECTED_EVIDENCE_FILES = [
    "monte_carlo_anti_d12/cdg.json",
    "monte_carlo_anti_d12/matches.json",
    "monte_carlo_anti_d12/references.json",
]
EXPECTED_REF_IDS = {"glasserman2003", "repo_quantfin"}


def _load_bundle() -> dict[str, object]:
    return json.loads(BUNDLE_PATH.read_text())


def _row_by_id(bundle: dict[str, object], row_id: str) -> dict[str, object]:
    rows = bundle["rows"]
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        if row["row_id"] == row_id:
            return row
    raise AssertionError(f"missing review bundle row {row_id}")


def _effective_notes(bundle: dict[str, object], row: dict[str, object], field: str) -> list[str]:
    bundle_notes = bundle[field]
    row_notes = row[field]
    assert isinstance(bundle_notes, list)
    assert isinstance(row_notes, list)
    return [*bundle_notes, *row_notes]


def test_quantfin_monte_carlo_anti_d12_row_is_ready_and_registered() -> None:
    bundle = _load_bundle()
    module = importlib.import_module(MONTE_CARLO_MODULE)
    registry = importlib.import_module("sciona.ghost.registry").REGISTRY

    row = _row_by_id(bundle, "monte_carlo_anti_d12/atoms")

    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "supported"
    assert row["trust_readiness"] == "ready"
    assert _effective_notes(bundle, row, "limitations") == []
    assert _effective_notes(bundle, row, "required_actions") == []
    assert row["evidence_files"] == EXPECTED_EVIDENCE_FILES
    assert {entry["ref_id"] for entry in row["authoritative_sources"]} == EXPECTED_REF_IDS
    assert set(row["atom_keys"]) == EXPECTED_ATOM_KEYS
    assert {key.rsplit(".", 1)[-1] for key in row["atom_keys"]}.issubset(registry)

    assert callable(module.runmc)
    assert callable(module.runsimulationanti)
    assert callable(module.avg)
