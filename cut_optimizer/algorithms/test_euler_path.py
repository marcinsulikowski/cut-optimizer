"""Tests for euler_path.py"""

import pytest

from cut_optimizer.algorithms.euler_path import euler_path, NoEulerPathFound
from cut_optimizer.labelled_graph import LabelledGraph


def _euler_path_as_string(graph: LabelledGraph[int, str], *, start: int) -> str:
    """Return a string composed of tags of edges in an Euler path."""
    path = euler_path(graph, graph.get_vertex(start))
    return "".join(graph.get_tag(edge) for edge in path)


def test_euler_path_in_K2() -> None:
    """Test finding an Euler path in a K2 graph."""
    graph = LabelledGraph[int, str]()
    graph.add_tagged_vertices([1, 2])
    graph.add_tagged_edge(1, 2, "E")
    assert _euler_path_as_string(graph, start=1) == "E"
    assert _euler_path_as_string(graph, start=2) == "E"


def test_euler_path_in_K3() -> None:
    """Test finding an Euler path in a K3 graph."""
    graph = LabelledGraph[int, str]()
    graph.add_tagged_vertices([1, 2, 3])
    graph.add_tagged_edge(1, 2, "A")
    graph.add_tagged_edge(2, 3, "B")
    graph.add_tagged_edge(1, 3, "C")
    assert _euler_path_as_string(graph, start=1) in {"ABC", "CBA"}
    assert _euler_path_as_string(graph, start=2) in {"ACB", "BCA"}
    assert _euler_path_as_string(graph, start=3) in {"CAB", "BAC"}


def test_euler_path_in_1() -> None:
    """Test finding an Euler path in the following graph:

    [1], [2], [3] - vertices
    A, B, C - edges

              .--C--.
             |       |
    [1]--A--[2]--B--[3]
    """
    graph = LabelledGraph[int, str]()
    graph.add_tagged_vertices([1, 2, 3])
    graph.add_tagged_edge(1, 2, "A")
    graph.add_tagged_edge(2, 3, "B")
    graph.add_tagged_edge(2, 3, "C")
    assert _euler_path_as_string(graph, start=1) in {"ABC", "ACB"}
    assert _euler_path_as_string(graph, start=2) in {"BCA", "CBA"}
    with pytest.raises(NoEulerPathFound):
        _euler_path_as_string(graph, start=3)


def test_euler_path_2() -> None:
    """Test finding an Euler path in the following graph:

    [1], [2], ... - vertices
    A, B, ... - edges

                     .--[2]--.
                     |       |
                     A       B
                     |       |
    [1]--C--[3]--D--[4]--E--[5]
                     |       |
                     F       G
                     |       |
                     '--[6]--'
    """
    graph = LabelledGraph[int, str]()
    graph.add_tagged_vertices([1, 2, 3, 4, 5, 6])
    graph.add_tagged_edge(2, 4, "A")
    graph.add_tagged_edge(2, 5, "B")
    graph.add_tagged_edge(1, 3, "C")
    graph.add_tagged_edge(3, 4, "D")
    graph.add_tagged_edge(4, 5, "E")
    graph.add_tagged_edge(4, 6, "F")
    graph.add_tagged_edge(5, 6, "G")

    assert _euler_path_as_string(graph, start=1) in {
        "CDABEFG",
        "CDABGFE",
        "CDEBAFG",
        "CDEGFAB",
        "CDFGEAB",
        "CDFGBAE",
    }
    assert _euler_path_as_string(graph, start=5) in {
        "BAEGFDC",
        "BAFGEDC",
        "EABGFDC",
        "EFGBADC",
        "GFABEDC",
        "GFEBADC",
    }
    with pytest.raises(NoEulerPathFound):
        _euler_path_as_string(graph, start=2)
    with pytest.raises(NoEulerPathFound):
        _euler_path_as_string(graph, start=3)
    with pytest.raises(NoEulerPathFound):
        _euler_path_as_string(graph, start=4)
