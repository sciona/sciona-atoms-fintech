import importlib


def test_institutional_quant_engine_copula_dependence_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.copula_dependence") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_copula_dependence") is not None
