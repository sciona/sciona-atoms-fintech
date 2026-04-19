from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any


MODULE = "sciona.atoms.fintech.quantfin.monte_carlo_anti_d12"


def _impl(name: str) -> Callable[..., Any]:
    importlib.import_module(MODULE)
    registry = importlib.import_module("sciona.ghost.registry").REGISTRY
    return registry[name]["impl"]


def test_insertcf_variants_preserve_time_order() -> None:
    singleton = _impl("insertcf_singleton")
    recursive = _impl("insertcf_recursive")

    assert singleton((0.5, 12.0)) == [(0.5, 12.0)]
    assert recursive(
        7.0,
        4.0,
        [(1.0, 10.0)],
        lambda t, amt, cfs: [(t, amt), *cfs],
        [(0.25, 7.0), (0.5, 4.0), (1.0, 10.0)],
        0.25,
        0.5,
    ) == [(0.25, 7.0), (0.5, 4.0), (1.0, 10.0)]
    assert recursive(
        7.0,
        4.0,
        [(1.0, 10.0)],
        lambda t, amt, cfs: [(t, amt), *cfs],
        [],
        0.75,
        0.5,
    ) == [(0.5, 4.0), (0.75, 7.0), (1.0, 10.0)]


def test_insertcflist_variants_merge_cashflows_with_insert_function() -> None:
    def insert_cf(cf: tuple[float, float], existing: list[tuple[float, float]]) -> list[tuple[float, float]]:
        return sorted([*existing, cf], key=lambda item: item[0])

    base = [(0.50, 5.0), (1.00, 10.0)]
    new_flows = [(0.25, 2.5), (0.75, 7.5)]
    expected = [(0.25, 2.5), (0.50, 5.0), (0.75, 7.5), (1.00, 10.0)]

    for name in ("insertcflist_fold", "insertcflist_fold_alt"):
        insertcflist = _impl(name)
        assert insertcflist(base, lambda fn: fn, None, insert_cf, new_flows) == expected


def test_process_base_case_returns_discounted_cashflows() -> None:
    process_base_case = _impl("process_base_case")

    assert process_base_case(12.5, lambda value: ("wrapped", value)) == 12.5


def test_process_with_cashflows_only_discounts_current_cashflow() -> None:
    process_with_cashflows_only = _impl("process_with_cashflows_only")
    evolve_calls: list[tuple[dict[str, str], bool, float, float]] = []

    result = process_with_cashflows_only(
        False,
        (0.50, 10.0),
        lambda cf: cf[1],
        lambda cf: cf[0],
        [],
        0.0,
        1.25,
        lambda modl, time: modl["discount_curve"][time],
        lambda modl, anti, start, end: evolve_calls.append((modl, anti, start, end)),
        {"discount_curve": {0.50: 0.90}},
        {},
        lambda *args: None,
    )

    assert result == 10.25
    assert evolve_calls == [({"discount_curve": {0.50: 0.90}}, False, 0.50, 0.50)]


def test_process_with_observation_only_generates_and_merges_cashflows() -> None:
    process_with_observation_only = _impl("process_with_observation_only")
    downstream_calls: list[tuple[Any, ...]] = []
    evolve_calls: list[tuple[Any, ...]] = []

    def downstream(*args: Any) -> float:
        downstream_calls.append(args)
        return 42.0

    result = process_with_observation_only(
        True,
        ["next_claim"],
        [(2.00, 1.0)],
        3.5,
        lambda *args: evolve_calls.append(args),
        lambda fn: fn,
        None,
        lambda pair: pair[0],
        lambda modl: modl["spot"],
        lambda time, value, obs_map: {**obs_map, time: value},
        None,
        lambda existing, new: sorted([*existing, *new], key=lambda item: item[0]),
        map,
        [lambda obs_map: (1.50, obs_map[1.0] + 2.0)],
        {"spot": 8.0},
        [],
        None,
        {},
        {},
        downstream,
        1.0,
        [],
    )

    assert result == 42.0
    assert evolve_calls == [({"spot": 8.0}, True, 1.0, 1.0)]
    assert downstream_calls == [
        (True, {"spot": 8.0}, ["next_claim"], [(1.50, 10.0), (2.00, 1.0)], {1.0: 8.0}, 3.5)
    ]


def test_process_with_pending_cashflows_prioritizes_earlier_cashflow() -> None:
    process_with_pending_cashflows = _impl("process_with_pending_cashflows")
    downstream_calls: list[tuple[Any, ...]] = []
    evolve_calls: list[tuple[Any, ...]] = []

    def downstream(*args: Any) -> float:
        downstream_calls.append(args)
        return 11.0

    result = process_with_pending_cashflows(
        [(0.50, 10.0)],
        10.0,
        False,
        "claim",
        ["remaining_claim"],
        [],
        [(0.75, 3.0)],
        0.50,
        0.0,
        2.0,
        lambda modl, time: modl["discount_curve"][time],
        lambda *args: evolve_calls.append(args),
        lambda fn: fn,
        None,
        lambda pair: pair[0],
        lambda modl: modl["spot"],
        lambda time, value, obs_map: {**obs_map, time: value},
        None,
        lambda existing, new: [*existing, *new],
        map,
        [],
        {"spot": 8.0, "discount_curve": {0.50: 0.80}},
        [],
        None,
        {},
        {},
        downstream,
        1.0,
        [],
    )

    assert result == 11.0
    assert evolve_calls == [({"spot": 8.0, "discount_curve": {0.50: 0.80}}, False, 0.50, 0.50)]
    assert downstream_calls == [
        (
            False,
            {"spot": 8.0, "discount_curve": {0.50: 0.80}},
            ["remaining_claim"],
            [(0.75, 3.0)],
            {},
            10.0,
        )
    ]
