import importlib

def test_fintech_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.quant_engine") is not None
    assert importlib.import_module("sciona.probes.fintech.quant_engine") is not None
