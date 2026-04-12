import importlib


def test_institutional_quant_engine_dynamic_hedge_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.dynamic_hedge") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_dynamic_hedge") is not None
