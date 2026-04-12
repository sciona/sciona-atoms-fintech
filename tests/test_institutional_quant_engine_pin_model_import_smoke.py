import importlib


def test_institutional_quant_engine_pin_model_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.pin_model") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_pin_model") is not None
