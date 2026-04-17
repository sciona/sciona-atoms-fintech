from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles/quantfin_review_bundle.json"


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


def test_quantfin_char_func_option_row_is_not_poisoned_by_bundle_level_blockers() -> None:
    bundle = _load_bundle()

    assert bundle["limitations"] == []
    assert bundle["required_actions"] == []

    char_func_row = _row_by_id(bundle, "char_func_option_d12/atoms")
    assert char_func_row["review_status"] == "reviewed"
    assert char_func_row["semantic_verdict"] == "supported"
    assert char_func_row["trust_readiness"] == "ready"
    assert _effective_notes(bundle, char_func_row, "limitations") == []
    assert _effective_notes(bundle, char_func_row, "required_actions") == []


def test_quantfin_rng_skip_row_is_ready_with_external_citation() -> None:
    bundle = _load_bundle()
    rng_skip_row = _row_by_id(bundle, "rng_skip_d12/atoms")

    assert rng_skip_row["review_status"] == "reviewed"
    assert rng_skip_row["semantic_verdict"] == "supported"
    assert rng_skip_row["trust_readiness"] == "ready"
    assert _effective_notes(bundle, rng_skip_row, "limitations") == []
    assert _effective_notes(bundle, rng_skip_row, "required_actions") == []
