import importlib


def test_hftbacktest_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.hftbacktest") is not None
    assert importlib.import_module("sciona.probes.fintech.hftbacktest") is not None
