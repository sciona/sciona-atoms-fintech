import importlib


def test_institutional_quant_engine_wash_trade_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.wash_trade") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_wash_trade") is not None
