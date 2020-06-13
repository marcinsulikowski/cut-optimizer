"""Tests for labelled_graph.py"""

import pytest

from cut_optimizer.graph import Vertex
from cut_optimizer.labelled_graph import LabelledGraph


def test_vertex_tags() -> None:
    # pylint: disable=invalid-name
    """Test if tags work for vertices."""
    graph = LabelledGraph[int, str]()
    v1 = graph.add_tagged_vertex(1)
    v2 = graph.add_tagged_vertex(2)
    v3 = graph.add_vertex(Vertex())
    assert graph.get_tag(v1) == 1
    assert graph.get_vertex(1) == v1
    assert graph.get_tag(v2) == 2
    assert graph.get_vertex(2) == v2
    with pytest.raises(KeyError):
        graph.get_tag(v3)


def test_edge_tags() -> None:
    # pylint: disable=invalid-name
    """Test if tags work for edges."""
    graph = LabelledGraph[int, str]()
    v1 = graph.add_tagged_vertex(1)
    v2 = graph.add_tagged_vertex(2)
    v3 = graph.add_vertex(Vertex())
    e1 = graph.add_tagged_edge(v1, v2, "e1")
    e2 = graph.add_tagged_edge(1, v3, "e2")
    e3 = graph.add_tagged_edge(v1, 2, "e3")
    e4 = graph.add_tagged_edge(1, 2)

    assert e1.vertex_1 == v1
    assert e1.vertex_2 == v2
    assert graph.get_tag(e1) == "e1"
    assert graph.get_edge("e1") == e1

    assert e2.vertex_1 == v1
    assert e2.vertex_2 == v3
    assert graph.get_tag(e2) == "e2"
    assert graph.get_edge("e2") == e2

    assert e3.vertex_1 == v1
    assert e3.vertex_2 == v2
    assert graph.get_tag(e3) == "e3"
    assert graph.get_edge("e3") == e3

    assert e4.vertex_1 == v1
    assert e4.vertex_2 == v2
    with pytest.raises(KeyError):
        graph.get_tag(e4)

    # Test that after an edge is removed, it cannot be access via tags.
    graph.remove_edge(e3)
    with pytest.raises(KeyError):
        graph.get_tag(e3)
    with pytest.raises(KeyError):
        graph.get_edge("e3")


def test_repeated_tags() -> None:
    # pylint: disable=invalid-name
    """Test if things work correctly when multiple elements share tags."""
    graph = LabelledGraph[int, str]()
    v1 = graph.add_tagged_vertex(1)
    v2 = graph.add_tagged_vertex(1)
    e1 = graph.add_tagged_edge(v1, v2, "edge")
    e2 = graph.add_tagged_edge(v1, v2, "edge")

    # If tags are repeated, we should be able to get them
    assert graph.get_tag(v1) == 1
    assert graph.get_tag(v2) == 1
    assert graph.get_tag(e1) == "edge"
    assert graph.get_tag(e2) == "edge"

    # If tags are repeated, the reverse mapping does not work
    with pytest.raises(ValueError):
        graph.get_vertex(1)
    with pytest.raises(ValueError):
        graph.get_edge("edge")

    # Deleting an edge should work though, and should fix the
    # reverse mapping for edges.
    graph.remove_edge(e1)
    assert graph.get_tag(v1) == 1
    assert graph.get_tag(v2) == 1
    assert graph.get_tag(e2) == "edge"
    assert graph.get_edge("edge") == e2

    # Deleting all edges makes `graph.get_edge` raise `KeyError`.
    graph.remove_edge(e2)
    with pytest.raises(KeyError):
        graph.get_edge("edge")

    # Test that adding a new one still works.
    e3 = graph.add_tagged_edge(v1, v2, "edge")
    assert graph.get_tag(e3) == "edge"
    assert graph.get_edge("edge") == e3
