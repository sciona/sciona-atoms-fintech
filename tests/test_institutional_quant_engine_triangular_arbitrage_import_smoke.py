import importlib


def test_institutional_quant_engine_triangular_arbitrage_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.triangular_arbitrage") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_triangular_arbitrage") is not None
