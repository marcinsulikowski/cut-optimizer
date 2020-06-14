"""Tests for optimize_x_moves.py."""

from typing import Sequence

import pytest

from cut_optimizer.algorithms.optimize_x_moves import optimize_x_moves
from cut_optimizer.instance import Point, Polyline


def order_to_string(polylines: Sequence[Polyline]) -> str:
    """Returns concatenated names of given polylines."""
    return "".join(poly.name for poly in polylines)


@pytest.mark.xfail
def test_case_1() -> None:
    """Test 1."""
    polylines = [
        Polyline("A", Point(1, 0), Point(7, 0), is_closed=False),
        Polyline("B", Point(8, 0), Point(99, 0), is_closed=False),
        Polyline("C", Point(9, 0), Point(20, 0), is_closed=False),
    ]
    assert order_to_string(optimize_x_moves(polylines)) == "ACB"


@pytest.mark.xfail
def test_case_2() -> None:
    """Test 2."""
    polylines = [
        Polyline("L", Point(3, 0), Point(30, 0), is_closed=False),
        Polyline("A", Point(1, 0), Point(2, 0), is_closed=False),
        Polyline("B", Point(4, 0), Point(5, 0), is_closed=False),
        Polyline("C", Point(33, 0), Point(34, 0), is_closed=False),
        Polyline("D", Point(22, 0), Point(28, 0), is_closed=False),
    ]
    assert order_to_string(optimize_x_moves(polylines)) == "ABLDC"


@pytest.mark.xfail
def test_case_3() -> None:
    """Test 3."""
    polylines = [
        Polyline("L", Point(3, 0), Point(30, 0), is_closed=False),
        Polyline("A", Point(1, 0), Point(2, 0), is_closed=False),
        Polyline("B", Point(4, 0), Point(5, 0), is_closed=False),
        Polyline("C", Point(33, 0), Point(34, 0), is_closed=False),
        Polyline("D", Point(11, 0), Point(28, 0), is_closed=False),
    ]
    assert order_to_string(optimize_x_moves(polylines)) == "ABCDL"


def test_case_4() -> None:
    """Test 4."""
    polylines = [
        Polyline("A", Point(1, 0), Point(10, 0), is_closed=False),
        Polyline("B", Point(10, 0), Point(1, 0), is_closed=False),
        Polyline("C", Point(7, 0), Point(8, 0), is_closed=False),
        Polyline("D", Point(7, 0), Point(8, 0), is_closed=False),
    ]
    assert order_to_string(optimize_x_moves(polylines)) in {
        "ACDB",
        "ADCB",
        "BCDA",
        "BDCA",
    }
