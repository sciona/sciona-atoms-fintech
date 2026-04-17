from __future__ import annotations

import importlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATHS = [
    REPO_ROOT / "docs/review-bundles/quant_engine_review_bundle.json",
    REPO_ROOT / "docs/review-bundles/quantfin_review_bundle.json",
    REPO_ROOT / "docs/review-bundles/institutional_quant_engine_review_bundle.json",
    REPO_ROOT / "docs/review-bundles/hftbacktest_review_bundle.json",
]


def test_provider_owned_review_bundles_map_to_registered_atoms() -> None:
    registry = importlib.import_module("sciona.ghost.registry").REGISTRY

    for bundle_path in BUNDLE_PATHS:
        bundle = json.loads(bundle_path.read_text())
        assert bundle["review_status"] == "reviewed"
        assert (REPO_ROOT / bundle["review_record_path"]).exists()

        for row in bundle["rows"]:
            importlib.import_module(row["module"])
            for atom_key in row["atom_keys"]:
                leaf = atom_key.rsplit(".", 1)[-1]
                assert leaf in registry, f"missing registry entry for {leaf} in {row['module']}"
