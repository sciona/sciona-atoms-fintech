import importlib


def test_institutional_quant_engine_avellaneda_stoikov_d12_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.avellaneda_stoikov_d12") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_avellaneda_stoikov_d12") is not None
