from __future__ import annotations

import importlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles/institutional_quant_engine_review_bundle.json"
FAMILY_ROOT = REPO_ROOT / "src/sciona/atoms/fintech/institutional_quant_engine"

SAFE_ROWS = {
    "copula_dependence",
    "dynamic_hedge",
    "evt_model",
    "hawkes_process",
    "heston_model",
    "hierarchical_risk_parity",
    "order_flow_imbalance",
    "queue_estimator/atoms",
    "supply_chain",
    "triangular_arbitrage",
}

HELD_ROWS = {
    "fractional_diff",
    "pin_model",
    "wash_trade",
}


def _load_bundle() -> dict[str, object]:
    return json.loads(BUNDLE_PATH.read_text())


def _rows_by_id(bundle: dict[str, object]) -> dict[str, dict[str, object]]:
    rows = bundle["rows"]
    assert isinstance(rows, list)
    return {str(row["row_id"]): row for row in rows if isinstance(row, dict)}


def _load_reference_atoms(relative_path: str) -> set[str]:
    payload = json.loads((FAMILY_ROOT / relative_path).read_text())
    atoms = payload["atoms"]
    assert isinstance(atoms, dict)
    return set(atoms)


def _load_uncertainty_atoms(relative_path: str) -> set[str]:
    payload = json.loads((FAMILY_ROOT / relative_path).read_text())
    assert isinstance(payload["atom"], str)
    estimates = payload["estimates"]
    assert isinstance(estimates, list)
    assert estimates
    for estimate in estimates:
        assert isinstance(estimate["scalar_factor"], int | float)
        assert isinstance(estimate["confidence"], int | float)
    atoms = payload["atoms"]
    assert isinstance(atoms, dict)
    return set(atoms)


def _resolve_atom(fqdn: str) -> object:
    module_name, leaf_name = fqdn.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, leaf_name)


def test_pubrev_001_safe_rows_are_ready_and_not_bundle_blocked() -> None:
    bundle = _load_bundle()
    rows = _rows_by_id(bundle)

    assert bundle["ready_rows"] == 15
    assert bundle["conditional_rows"] == 0
    assert bundle["not_ready_rows"] == 3
    assert bundle["limitations"] == []
    assert bundle["required_actions"] == []

    for row_id in SAFE_ROWS:
        row = rows[row_id]
        assert row["semantic_verdict"] == "supported"
        assert row["trust_readiness"] == "ready"
        assert row["limitations"] == []
        assert row["required_actions"] == []
        assert row["source_paths"]


def test_pubrev_001_held_rows_remain_unpublished_with_remediation() -> None:
    rows = _rows_by_id(_load_bundle())

    for row_id in HELD_ROWS:
        row = rows[row_id]
        assert row["semantic_verdict"] == "semantic_drift"
        assert row["trust_readiness"] == "not_ready"
        assert row["developer_semantic_verdict"] == "semantic_drift_requires_repair"
        assert row["limitations"]
        assert row["required_actions"]
        assert "REMEDIATION.md" in row["evidence_files"]


def test_pubrev_001_atom_keys_are_exact_importable_fqdns() -> None:
    rows = _rows_by_id(_load_bundle())

    for row_id in SAFE_ROWS | HELD_ROWS:
        atom_keys = rows[row_id]["atom_keys"]
        assert isinstance(atom_keys, list)
        for atom_key in atom_keys:
            assert callable(_resolve_atom(str(atom_key)))


def test_pubrev_001_ready_rows_have_reference_and_uncertainty_bindings() -> None:
    rows = _rows_by_id(_load_bundle())
    root_reference_atoms = _load_reference_atoms("references.json")
    root_uncertainty_atoms = _load_uncertainty_atoms("uncertainty.json")
    queue_reference_atoms = _load_reference_atoms("queue_estimator/references.json")
    queue_uncertainty_atoms = _load_uncertainty_atoms("queue_estimator/uncertainty.json")

    for row_id in SAFE_ROWS:
        row = rows[row_id]
        evidence_files = row["evidence_files"]
        source_paths = row["source_paths"]
        assert isinstance(evidence_files, list)
        assert isinstance(source_paths, list)

        for evidence_file in evidence_files:
            assert (FAMILY_ROOT / str(evidence_file)).exists()

        for atom_key, source_path in zip(row["atom_keys"], source_paths, strict=True):
            reference_key = f"{atom_key}@{str(source_path).removeprefix('src/')}"
            if row_id == "queue_estimator/atoms":
                assert reference_key in queue_reference_atoms
                assert reference_key in queue_uncertainty_atoms
            else:
                assert reference_key in root_reference_atoms
                assert reference_key in root_uncertainty_atoms
