from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "data" / "licenses" / "provider_license.json"
EXPECTED_UNRESOLVED = {
    "sciona.atoms.fintech.hftbacktest",
    "sciona.atoms.fintech.institutional_quant_engine",
    "sciona.atoms.fintech.quant_engine",
    "sciona.atoms.fintech.quantfin",
}


def test_fintech_license_manifest_defaults_to_unknown() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())

    assert manifest["provider_repo"] == "sciona-atoms-fintech"
    assert manifest["repo_default_license"]["license_spdx"] == "NOASSERTION"
    assert manifest["repo_default_license"]["status"] == "unknown"
    assert manifest["family_overrides"] == []

    unresolved = {row["family"] for row in manifest["unresolved_families"]}
    assert unresolved == EXPECTED_UNRESOLVED
