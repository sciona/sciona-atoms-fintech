import importlib


def test_institutional_quant_engine_fractional_diff_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.fractional_diff") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_fractional_diff") is not None
