"""Minimizes the amount of X-axis moves needed to cut a set of polylines."""

from typing import Iterable, List, Tuple, Union

from cut_optimizer.algorithms.euler_path import euler_path
from cut_optimizer.graph import Vertex
from cut_optimizer.instance import Polyline
from cut_optimizer.labelled_graph import LabelledGraph


class Penalty:
    """Penalty which to be associated with idle moves of the cutter."""

    def __init__(self, value: int) -> None:
        self.value = value


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
        """Add penalty edges - phase 1."""

    def make_connected(self) -> None:
        """Add minimal edges to make the graph connected."""

    def solve_for_end(self, path_end: Vertex) -> Tuple[int, List[Polyline]]:
        """TODO."""
        path_begin = self.get_vertex(0)
        self.add_required_penalties(path_begin, path_end)
        self.make_connected()
        path = euler_path(self, path_begin)
        tags = [self.get_tag(edge) for edge in path]
        penalties = [tag.value for tag in tags if isinstance(tag, Penalty)]
        polylines = [tag for tag in tags if isinstance(tag, Polyline)]
        self.remove_penalty_edges()
        return sum(penalties), polylines

    def _ensure_vertex(self, x_coordinate: int) -> Vertex:
        """Create vertex for a given X coordinate if not exists

        :return: the just created or already existing vertex.
        """
        try:
            return self.get_vertex(x_coordinate)
        except KeyError:
            return self.add_tagged_vertex(x_coordinate)


def optimize_x_moves(polylines: List[Polyline]) -> List[Polyline]:
    """Find an order of cutting which minimizes moves along the X axis."""
    graph = XCoordGraph()
    graph.add_open_polylines(poly for poly in polylines if poly.is_open)
    graph.add_closed_polylines(poly for poly in polylines if poly.is_closed)
    solutions = sorted(
        [graph.solve_for_end(vertex) for vertex in graph.vertices]
    )
    return solutions[0][1]
