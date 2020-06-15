"""Tests for optimize_x_moves.py."""

from typing import Sequence

from cut_optimizer.algorithms.optimize_x_moves import (
    optimize_x_moves,
    SolutionStep,
)
from cut_optimizer.instance import Point, Polyline


def steps_to_string(
    solution: Sequence[SolutionStep], show_directions: bool = False
) -> str:
    """Returns concatenated names of given polylines."""

    def step_to_string(step: SolutionStep) -> str:
        if (
            not show_directions
            or step.polyline.is_closed
            or step.polyline.start == step.start
        ):
            return step.polyline.name
        else:
            return step.polyline.name + "'"

    return "".join(step_to_string(step) for step in solution)


def test_simplest_closed_polylines() -> None:
    """Test the simplest problem with only closed polylines."""
    polylines = [
        Polyline("A", Point(1, 2), Point(3, 4), is_closed=True),
        Polyline("B", Point(5, 6), Point(7, 8), is_closed=True),
        Polyline("C", Point(9, 10), Point(11, 12), is_closed=True),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "ABC"


def test_case_1() -> None:
    """Test 1."""
    polylines = [
        Polyline("A", Point(1, 0), Point(7, 0), is_closed=False),
        Polyline("B", Point(8, 0), Point(99, 0), is_closed=False),
        Polyline("C", Point(9, 0), Point(20, 0), is_closed=False),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "ACB"


def test_case_2() -> None:
    """Test 2."""
    polylines = [
        Polyline("L", Point(3, 0), Point(30, 0), is_closed=False),
        Polyline("A", Point(1, 0), Point(2, 0), is_closed=False),
        Polyline("B", Point(4, 0), Point(5, 0), is_closed=False),
        Polyline("C", Point(33, 0), Point(34, 0), is_closed=False),
        Polyline("D", Point(22, 0), Point(28, 0), is_closed=False),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "ABLCD"


def test_case_3() -> None:
    """Test 3."""
    polylines = [
        Polyline("L", Point(3, 0), Point(30, 0), is_closed=False),
        Polyline("A", Point(1, 0), Point(2, 0), is_closed=False),
        Polyline("B", Point(4, 0), Point(5, 0), is_closed=False),
        Polyline("C", Point(33, 0), Point(34, 0), is_closed=False),
        Polyline("D", Point(6, 0), Point(28, 0), is_closed=False),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "ALCDB"


def test_case_4() -> None:
    """Test 4."""
    polylines = [
        Polyline("A", Point(1, 0), Point(10, 0), is_closed=False),
        Polyline("B", Point(10, 0), Point(1, 0), is_closed=False),
        Polyline("C", Point(7, 0), Point(8, 0), is_closed=False),
        Polyline("D", Point(7, 0), Point(8, 0), is_closed=False),
    ]
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"AC'DB", "AD'CB", "B'C'DA'", "B'D'CA'",}


def test_case_5() -> None:
    """Test 5."""
    polylines = [
        Polyline("A", Point(1, 0), Point(10, 0), is_closed=False),
        Polyline("B", Point(1, 0), Point(3, 0), is_closed=False),
        Polyline("C", Point(1, 0), Point(3, 0), is_closed=False),
    ]
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"BC'A", "CB'A"}


def test_case_6() -> None:
    """Test 6."""
    polylines = [
        Polyline("A", Point(1, 0), Point(100, 0), is_closed=False),
        Polyline("B", Point(3, 0), Point(110, 0), is_closed=False),
        Polyline("C", Point(5, 0), Point(9, 0), is_closed=False),
    ]
    assert (
        steps_to_string(optimize_x_moves(polylines), show_directions=True)
        == "AB'C"
    )


def test_case_7() -> None:
    """Test 7."""
    polylines = [
        Polyline("A", Point(0, 0), Point(3, 0), is_closed=False),
        Polyline("B", Point(0, 0), Point(3, 0), is_closed=False),
        Polyline("C", Point(3, 0), Point(6, 0), is_closed=False),
        Polyline("D", Point(3, 0), Point(6, 0), is_closed=False),
    ]
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"ACD'B'", "ADC'B'", "BCD'A'", "BDC'A'"}


def test_case_8() -> None:
    """Test 8."""
    polylines = [
        Polyline("A", Point(1, 0), Point(3, 3), is_closed=True),
        Polyline("A", Point(1, 0), Point(3, 3), is_closed=True),
        Polyline("B", Point(3, 0), Point(6, 3), is_closed=True),
        Polyline("B", Point(3, 0), Point(6, 3), is_closed=True),
        Polyline("C", Point(6, 0), Point(9, 3), is_closed=True),
        Polyline("C", Point(6, 0), Point(9, 3), is_closed=True),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "AABBCC"


def test_case_9() -> None:
    """Test 9."""
    polylines = [
        Polyline("A", Point(100, 0), Point(130, 0), is_closed=False),
        Polyline("B", Point(125, 0), Point(160, 0), is_closed=False),
        Polyline("C", Point(155, 0), Point(190, 0), is_closed=False),
        Polyline("D", Point(145, 0), Point(150, 0), is_closed=False),
        Polyline("E", Point(120, 0), Point(129, 0), is_closed=True),
        Polyline("F", Point(180, 0), Point(220, 0), is_closed=True),
        Polyline("G", Point(140, 0), Point(145, 0), is_closed=True),
    ]
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"AEBD'GCF", "AEBGDCF"}


def test_case_10() -> None:
    """Test 10."""
    polylines = [
        Polyline("A", Point(100, 0), Point(999, 0), is_closed=False),
        Polyline("B", Point(200, 0), Point(400, 0), is_closed=True),
        Polyline("C", Point(300, 0), Point(780, 0), is_closed=True),
        Polyline("D", Point(780, 0), Point(900, 0), is_closed=True),
    ]
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"BCAD", "CBAD"}

    polylines.append(
        Polyline("E", Point(750, 0), Point(800, 0), is_closed=True),
    )
    assert steps_to_string(
        optimize_x_moves(polylines), show_directions=True
    ) in {"BADEC"}


def test_case_11() -> None:
    """Test 11."""
    polylines = [
        Polyline("A", Point(100, 0), Point(500, 100), is_closed=True),
        Polyline("B", Point(200, 0), Point(900, 200), is_closed=True),
        Polyline("C", Point(300, 0), Point(320, 400), is_closed=True),
        Polyline("D", Point(400, 0), Point(700, 300), is_closed=True),
        Polyline("E", Point(500, 0), Point(999, 250), is_closed=True),
        Polyline("F", Point(600, 0), Point(720, 350), is_closed=True),
        Polyline("G", Point(700, 0), Point(999, 150), is_closed=True),
        Polyline("H", Point(800, 0), Point(800, 550), is_closed=True),
        Polyline("I", Point(900, 0), Point(950, 300), is_closed=True),
    ]
    assert steps_to_string(optimize_x_moves(polylines)) == "ABCDEFGHI"
