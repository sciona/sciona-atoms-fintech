import importlib


def test_institutional_quant_engine_hawkes_process_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.hawkes_process") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_hawkes_process") is not None
