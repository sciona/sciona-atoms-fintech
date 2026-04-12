import importlib


def test_institutional_quant_engine_supply_chain_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.supply_chain") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_supply_chain") is not None
