"""Minimizes the amount of X-axis moves needed to cut a set of polylines."""

import random
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Union

from disjoint_set import DisjointSet

from cut_optimizer.algorithms.euler_path import euler_path
from cut_optimizer.graph import Edge, Vertex
from cut_optimizer.instance import Point, Polyline
from cut_optimizer.labelled_graph import LabelledGraph


@dataclass
class SolutionStep:
    """A step in the solution."""

    polyline: Polyline
    start: Point
    end: Point


class Penalty:
    """Penalty which to be associated with idle moves of the cutter."""

    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Penalty({self.value})"


class XCoordGraph(LabelledGraph[int, Union[Polyline, Penalty]]):
    """Graph where vertices are X coordinates and edges and polylines."""

    def __init__(self) -> None:
        super().__init__()
        self.add_tagged_vertex(0)

    def add_open_polylines(self, polylines: Iterable[Polyline]) -> None:
        """Adds vertices and edges representing open polylines."""
        for polyline in polylines:
            assert polyline.is_open
            vertex_1 = self._ensure_vertex(polyline.start.x)
            vertex_2 = self._ensure_vertex(polyline.end.x)
            self.add_tagged_edge(vertex_1, vertex_2, polyline)

    def add_closed_polylines(self, polylines: Iterable[Polyline]) -> None:
        """Adds vertices and edges representing closed polylines.

        This can be called only after all open polylines are already added.
        """
        for polyline in polylines:
            assert polyline.is_closed
            # The code below is not correct. For each polyline we need to
            # choose if we want to start cutting it from up, down, or
            # somewhere in the middle.
            vertex = self._ensure_vertex(polyline.start.x)
            self.add_tagged_edge(vertex, vertex, polyline)

    def remove_penalty_edges(self) -> None:
        """Remove all penalty edges from the graph."""
        penalty_edges = [
            edge
            for edge in self.edges
            if isinstance(self.get_tag(edge), Penalty)
        ]
        for edge in penalty_edges:
            self.remove_edge(edge)

    def add_required_penalties(self, begin: Vertex, end: Vertex) -> None:
        """Add penalty edges - phase 1

        Add penalty edges between vertices to ensure that any vertex different
        than the begin and end of the path has even degree.
        """
        # We want to ensure that there's an Euler path from begin to end which
        # means that any vertex other than the two needs to be of an even
        # degree, and that the degree of both `begin` and `end` is odd, unless
        # they are the same vertex.
        vertices_to_change_degree = [
            vertex
            for vertex in self.vertices
            if self.get_vertex_degree(vertex) % 2 == 1
            and vertex not in {begin, end}
        ]
        if begin == end:
            if not self.is_even_degree(begin):
                vertices_to_change_degree.append(begin)
        else:
            if self.is_even_degree(begin):
                vertices_to_change_degree.append(begin)
            if self.is_even_degree(end):
                vertices_to_change_degree.append(end)
        vertices_to_change_degree.sort(key=self.get_tag)
        assert len(vertices_to_change_degree) % 2 == 0

        # Change the degrees by adding minimal amount of edges, i.e.,
        # edge from vertex 0 to 1, 2 to 3, 4 to 5, etc.
        for i in range(len(vertices_to_change_degree) // 2):
            vertex_1 = vertices_to_change_degree[2 * i]
            vertex_2 = vertices_to_change_degree[2 * i + 1]
            self.add_tagged_edge(
                vertex_1,
                vertex_2,
                Penalty(self.get_tag(vertex_2) - self.get_tag(vertex_1)),
            )

    def make_connected(self) -> None:
        """Add minimal edges to make the graph connected."""
        # Create a collection of all edges which connect consecutive vertices.
        # For each such edge remember its length because we'll try to use the
        # shortest of them to connect components of the graph.
        candidate_edges: List[Tuple[int, Vertex, Vertex]] = []
        x_coords = sorted(self.get_vertex_tags())
        for x_1, x_2 in zip(x_coords, x_coords[1:]):
            vertex_1 = self.get_vertex(x_1)
            vertex_2 = self.get_vertex(x_2)
            candidate_edges.append((abs(x_2 - x_1), vertex_1, vertex_2))
        candidate_edges.sort(
            key=lambda candidate: (candidate[0], random.uniform(0, 1))
        )

        union_find = DisjointSet[Vertex]()
        for edge in self.edges:
            union_find.union(edge.vertex_1, edge.vertex_2)
        for distance, vertex_1, vertex_2 in candidate_edges:
            if not union_find.connected(vertex_1, vertex_2):
                # This step is performed after fixing the parity of degrees of
                # each vertex. At this stage we don't want to change any
                # partities so we need to add two edges.
                self.add_tagged_edge(vertex_1, vertex_2, Penalty(distance))
                self.add_tagged_edge(vertex_1, vertex_2, Penalty(distance))
                union_find.union(vertex_1, vertex_2)

    def path_to_solution(self, path: List[Edge]) -> List[SolutionStep]:
        """Get a solution which corresponds to a given Euler path."""
        solution = []
        current_pos = self.get_vertex(0)
        for edge in path:
            next_pos = edge.other_end(current_pos)
            edge_tag = self.get_tag(edge)
            if isinstance(edge_tag, Polyline):
                current_x = self.get_tag(current_pos)
                polyline = edge_tag
                if polyline.is_closed:
                    start = Point(current_x, polyline.start.y)
                    end = start
                else:
                    assert current_x in (polyline.start.x, polyline.end.x)
                    if current_x == polyline.start.x:
                        start = polyline.start
                        end = polyline.end
                    else:
                        start = polyline.end
                        end = polyline.start
                    solution.append(SolutionStep(polyline, start, end))
            current_pos = next_pos
        return solution

    def path_to_penalty(self, path: List[Edge]) -> int:
        """Get the total penalty of a given Euler path."""
        tags = [self.get_tag(edge) for edge in path]
        return sum(tag.value for tag in tags if isinstance(tag, Penalty))

    def solve_for_end(self, path_end: Vertex) -> Tuple[int, List[SolutionStep]]:
        """Find the best solution that ends on the given vertex."""
        path_begin = self.get_vertex(0)
        self.add_required_penalties(path_begin, path_end)
        self.make_connected()
        path = euler_path(self, path_begin)
        penalty = self.path_to_penalty(path)
        solution = self.path_to_solution(path)
        self.remove_penalty_edges()
        return penalty, solution

    def _ensure_vertex(self, x_coordinate: int) -> Vertex:
        """Create vertex for a given X coordinate if not exists

        :return: the just created or already existing vertex.
        """
        try:
            return self.get_vertex(x_coordinate)
        except KeyError:
            return self.add_tagged_vertex(x_coordinate)


def optimize_x_moves(polylines: List[Polyline]) -> List[SolutionStep]:
    """Find an order of cutting which minimizes moves along the X axis."""
    graph = XCoordGraph()
    graph.add_open_polylines(poly for poly in polylines if poly.is_open)
    graph.add_closed_polylines(poly for poly in polylines if poly.is_closed)
    solutions = sorted(
        [graph.solve_for_end(vertex) for vertex in graph.vertices],
        key=lambda penalty_and_solution: (
            penalty_and_solution[0],
            random.uniform(0, 1),
        ),
    )
    return solutions[0][1]
