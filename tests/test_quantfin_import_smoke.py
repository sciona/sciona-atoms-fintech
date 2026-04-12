import importlib


def test_quantfin_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.quantfin") is not None
    assert importlib.import_module("sciona.probes.fintech.quantfin") is not None
