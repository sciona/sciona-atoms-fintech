import importlib


def test_institutional_quant_engine_almgren_chriss_import_smoke() -> None:
    assert importlib.import_module("sciona.atoms.fintech.institutional_quant_engine.almgren_chriss") is not None
    assert importlib.import_module("sciona.probes.fintech.institutional_quant_engine_almgren_chriss") is not None
