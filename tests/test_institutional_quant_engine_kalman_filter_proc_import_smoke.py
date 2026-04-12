import importlib


def test_institutional_quant_engine_kalman_filter_proc_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.kalman_filter_proc") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_kalman_filter_proc") is not None
