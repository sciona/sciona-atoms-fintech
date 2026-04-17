from __future__ import annotations

import importlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO_ROOT / "docs/review-bundles" / "quantfin_review_bundle.json"
LOCAL_VOL_MODULE = "sciona.atoms.fintech.quantfin.local_vol_d12"
EXPECTED_LOCAL_VOL_KEYS = {
    f"{LOCAL_VOL_MODULE}.allfort",
    f"{LOCAL_VOL_MODULE}.localvol",
    f"{LOCAL_VOL_MODULE}.var",
    f"{LOCAL_VOL_MODULE}.vol_flat_surface",
    f"{LOCAL_VOL_MODULE}.vol_interpolated_surface",
}


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


def test_quantfin_local_vol_d12_row_is_ready_and_importable() -> None:
    bundle = _load_bundle()
    module = importlib.import_module(LOCAL_VOL_MODULE)

    local_vol_row = _row_by_id(bundle, "local_vol_d12/atoms")

    assert local_vol_row["review_status"] == "reviewed"
    assert local_vol_row["semantic_verdict"] == "supported"
    assert local_vol_row["trust_readiness"] == "ready"
    assert _effective_notes(bundle, local_vol_row, "limitations") == []
    assert _effective_notes(bundle, local_vol_row, "required_actions") == []
    assert set(local_vol_row["atom_keys"]) == EXPECTED_LOCAL_VOL_KEYS

    assert callable(module.vol_flat_surface)
    assert callable(module.vol_interpolated_surface)
    assert module.vol is module.vol_interpolated_surface


def test_quantfin_bundle_rollup_counts() -> None:
    bundle = _load_bundle()
    assert bundle["ready_rows"] == 6
    assert bundle["conditional_rows"] == 1
