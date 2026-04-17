from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles/quant_engine_review_bundle.json"


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


def test_quant_engine_bundle_is_ready_without_bundle_level_blockers() -> None:
    bundle = _load_bundle()

    assert bundle["review_status"] == "reviewed"
    assert bundle["limitations"] == []
    assert bundle["required_actions"] == []
    assert bundle["covered_rows"] == 2
    assert bundle["ready_rows"] == 2
    assert bundle["conditional_rows"] == 0


def test_quant_engine_ofi_row_is_publishable() -> None:
    bundle = _load_bundle()
    row = _row_by_id(bundle, "calculate_ofi")

    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "supported"
    assert row["trust_readiness"] == "ready"
    assert row["evidence_files"] == ["cdg.json", "references.json"]
    assert _effective_notes(bundle, row, "limitations") == []
    assert _effective_notes(bundle, row, "required_actions") == []


def test_quant_engine_execution_row_is_publishable() -> None:
    bundle = _load_bundle()
    row = _row_by_id(bundle, "execution_atoms")

    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "supported"
    assert row["trust_readiness"] == "ready"
    assert row["evidence_files"] == ["cdg.json", "references.json"]
    assert _effective_notes(bundle, row, "limitations") == []
    assert _effective_notes(bundle, row, "required_actions") == []
