"""Euler path finding."""

from typing import List, Tuple
import random

from cut_optimizer.graph import Edge, Graph, Vertex


class NoEulerPathFound(Exception):
    """Raised when no Euler path can be found."""


def euler_path(graph: Graph, start: Vertex) -> List[Edge]:
    """Return an Euler path in the graph starting from `start`.

    :raise: NoEulerPathFound if there's no Euler path starting at `start`.
    :return: list of edges which form the path.
    """
    assert start in graph.vertices
    path, _end = _euler_path_for_connected_component(graph.clone(), start)
    return path


def _euler_path_for_connected_component(
    graph: Graph, start: Vertex
) -> Tuple[List[Edge], Vertex]:
    # We'll maintain an invariant that `result` is a path from `start` to
    # `result_end`. If we find a cycle from `start` to `start`, we prepend
    # it to `result`. If we find a path from `start` to a dead end somewhere
    # else, we'll append it to `result` and move `result_end` to a dead end.
    result: List[Edge] = []
    result_end = start

    while graph.neighbors[start]:
        edge = random.choice(list(graph.neighbors[start]))
        graph.remove_edge(edge)
        path, end = _euler_path_for_connected_component(
            graph, edge.other_end(start)
        )
        if end == start:
            # A cycle from start to start - prepend it to the result
            result = [edge] + path + result
        else:
            # A path from start to somewhere else. If `result` already
            # ends somewhere other than `start`, it means that the graph
            # has more than one vertex of odd degree other than `start`.
            # In this case, there's no Euler part starting at `start`.
            if result_end != start:
                raise NoEulerPathFound(start)
            result = result + [edge] + path
            result_end = end
    return result, result_end
