import importlib


def test_institutional_quant_engine_order_flow_imbalance_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.order_flow_imbalance") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_order_flow_imbalance") is not None
