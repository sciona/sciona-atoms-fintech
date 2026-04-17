from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles" / "quantfin_review_bundle.json"
EXPECTED_REF_IDS = {"repo_quantfin", "thomas2011mwc64x"}


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


def test_quantfin_rng_skip_d12_row_is_ready_with_external_citation() -> None:
    bundle = _load_bundle()
    row = _row_by_id(bundle, "rng_skip_d12/atoms")

    assert row["review_status"] == "reviewed"
    assert row["semantic_verdict"] == "supported"
    assert row["trust_readiness"] == "ready"
    assert row["limitations"] == []
    assert row["required_actions"] == []
    assert {entry["ref_id"] for entry in row["authoritative_sources"]} == EXPECTED_REF_IDS
