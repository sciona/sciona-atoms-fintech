from __future__ import annotations

import numpy as np
import pandas as pd

from sciona.atoms.fintech.institutional_quant_engine.fractional_diff import (
    fractional_differentiator,
)
from sciona.atoms.fintech.institutional_quant_engine.wash_trade import (
    detect_wash_trade_rings,
)


def test_fractional_differentiator_preserves_identity_for_zero_order() -> None:
    series = pd.Series([10.0, 11.0, 13.0, 16.0], index=pd.RangeIndex(4))

    result = fractional_differentiator(series, d=0.0, threshold=1e-9)

    pd.testing.assert_series_equal(result, series.astype(float))


def test_fractional_differentiator_matches_first_difference() -> None:
    series = pd.Series([10.0, 11.0, 13.0, 16.0], index=pd.RangeIndex(4))

    result = fractional_differentiator(series, d=1.0, threshold=1e-9)

    expected = pd.Series([1.0, 2.0, 3.0], index=pd.RangeIndex(1, 4))
    pd.testing.assert_series_equal(result, expected)


def test_detect_wash_trade_rings_flags_long_directed_cycles() -> None:
    graph = np.zeros((6, 6), dtype=float)
    for src, dst in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]:
        graph[src, dst] = 1.0

    result = detect_wash_trade_rings(graph)

    assert result.dtype == np.bool_
    np.testing.assert_array_equal(result, np.ones(6, dtype=bool))


def test_detect_wash_trade_rings_leaves_acyclic_nodes_unflagged() -> None:
    graph = np.zeros((5, 5), dtype=float)
    graph[0, 1] = 1.0
    graph[1, 2] = 1.0
    graph[2, 0] = 1.0
    graph[3, 4] = 1.0

    result = detect_wash_trade_rings(graph)

    np.testing.assert_array_equal(result, np.array([True, True, True, False, False]))
