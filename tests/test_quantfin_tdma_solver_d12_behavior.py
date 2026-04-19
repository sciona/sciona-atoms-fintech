from __future__ import annotations

import pytest

from sciona.atoms.fintech.quantfin.tdma_solver_d12 import cotraverse_vec, tdma_solver


def test_tdma_solver_matches_known_tridiagonal_system() -> None:
    result = tdma_solver(
        sub_diagonal=[0.0, -1.0, -1.0],
        diagonal=[2.0, 2.0, 2.0],
        super_diagonal=[-1.0, -1.0, 0.0],
        rhs=[1.0, 0.0, 1.0],
    )

    assert result == pytest.approx([1.0, 1.0, 1.0])


def test_tdma_solver_rejects_zero_pivot() -> None:
    with pytest.raises(ValueError, match="zero first pivot"):
        tdma_solver(
            sub_diagonal=[0.0, 1.0],
            diagonal=[0.0, 2.0],
            super_diagonal=[1.0, 0.0],
            rhs=[1.0, 1.0],
        )


def test_cotraverse_vec_aggregates_index_aligned_slices() -> None:
    result = cotraverse_vec(
        aggregator=sum,
        length=3,
        vectors=[
            [1.0, 2.0, 3.0],
            [10.0, 20.0, 30.0],
            [100.0, 200.0, 300.0],
        ],
    )

    assert result == [111.0, 222.0, 333.0]
