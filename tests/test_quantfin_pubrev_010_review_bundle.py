from __future__ import annotations

import importlib
import json
from pathlib import Path

import numpy as np

from sciona.atoms.fintech.quantfin.models import ContingentClaim, DiscretizeModel


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles/quantfin_review_bundle.json"
REMEDIATION_PATH = REPO_ROOT / "REMEDIATION.md"
FAMILY_ROOT = REPO_ROOT / "src/sciona/atoms/fintech/quantfin"

MONTECARLO_ATOMS = {
    "sciona.atoms.fintech.quantfin.montecarlo.quick_sim_anti",
    "sciona.atoms.fintech.quantfin.montecarlo.run_simulation",
    "sciona.atoms.fintech.quantfin.montecarlo.run_simulation_anti",
}
TDMA_ATOMS = {
    "sciona.atoms.fintech.quantfin.tdma_solver_d12.cotraversevec",
    "sciona.atoms.fintech.quantfin.tdma_solver_d12.tdmasolver",
}


def _load_bundle() -> dict[str, object]:
    return json.loads(BUNDLE_PATH.read_text())


def _rows_by_id(bundle: dict[str, object]) -> dict[str, dict[str, object]]:
    rows = bundle["rows"]
    assert isinstance(rows, list)
    return {str(row["row_id"]): row for row in rows if isinstance(row, dict)}


def _resolve_atom(fqdn: str) -> object:
    module_name, leaf_name = fqdn.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, leaf_name)


def _reference_atoms(relative_path: str) -> set[str]:
    payload = json.loads((FAMILY_ROOT / relative_path).read_text())
    atoms = payload["atoms"]
    assert isinstance(atoms, dict)
    return set(atoms)


def _uncertainty_atoms(relative_path: str) -> set[str]:
    payload = json.loads((FAMILY_ROOT / relative_path).read_text())
    atoms = payload["atoms"]
    assert isinstance(atoms, dict)
    return set(atoms)


def test_pubrev_010_montecarlo_atoms_are_ready_with_exact_fqdns() -> None:
    bundle = _load_bundle()
    row = _rows_by_id(bundle)["montecarlo"]

    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "supported"
    assert row["trust_readiness"] == "ready"
    assert row["limitations"] == []
    assert row["required_actions"] == []
    assert set(row["atom_keys"]) == MONTECARLO_ATOMS
    assert {entry["ref_id"] for entry in row["authoritative_sources"]} == {
        "glasserman2003",
        "repo_quantfin",
    }

    reference_atoms = _reference_atoms("references.json")
    uncertainty_atoms = _uncertainty_atoms("uncertainty.json")
    for atom_key, source_path in zip(row["atom_keys"], row["source_paths"], strict=True):
        assert callable(_resolve_atom(str(atom_key)))
        review_key = f"{atom_key}@{str(source_path).removeprefix('src/')}"
        assert review_key in reference_atoms
        assert review_key in uncertainty_atoms


def test_pubrev_010_tdma_atoms_remain_unpublished_with_remediation() -> None:
    bundle = _load_bundle()
    row = _rows_by_id(bundle)["tdma_solver_d12/atoms"]

    assert bundle["ready_rows"] == 6
    assert bundle["conditional_rows"] == 0
    assert bundle["not_ready_rows"] == 1
    assert set(row["atom_keys"]) == TDMA_ATOMS
    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "semantic_drift"
    assert row["trust_readiness"] == "not_ready"
    assert row["developer_semantic_verdict"] == "source_api_drift_requires_repair"
    assert row["limitations"]
    assert row["required_actions"]
    assert "REMEDIATION.md" in row["evidence_files"]

    remediation = REMEDIATION_PATH.read_text()
    for atom_key in TDMA_ATOMS:
        assert callable(_resolve_atom(atom_key))
        assert atom_key in remediation


def test_pubrev_010_montecarlo_behavior_matches_upstream_split_contract() -> None:
    montecarlo = importlib.import_module("sciona.atoms.fintech.quantfin.montecarlo")
    model = DiscretizeModel()
    claim = ContingentClaim()
    simulator_name = "pubrev010_deterministic"

    def deterministic_simulator(
        model: DiscretizeModel,
        claim: ContingentClaim,
        rng: np.random.Generator,
        trials: int,
        anti: bool,
    ) -> float:
        del model, claim
        return float((100.0 if anti else 10.0) + trials + rng.random())

    montecarlo._register_simulator(simulator_name, deterministic_simulator)

    seed_123_draw = np.random.default_rng(123).random()
    assert montecarlo.run_simulation(model, claim, 123, 6, True, simulator_name) == (
        100.0 + 6 + seed_123_draw
    )

    expected_anti = ((100.0 + 4 + seed_123_draw) + (10.0 + 4 + seed_123_draw)) / 2.0
    assert montecarlo.run_simulation_anti(model, claim, 123, 8, simulator_name) == expected_anti

    seed_500_draw = np.random.default_rng(500).random()
    expected_quick = ((100.0 + 2 + seed_500_draw) + (10.0 + 2 + seed_500_draw)) / 2.0
    assert montecarlo.quick_sim_anti(model, claim, 4, simulator_name) == expected_quick
