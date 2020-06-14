"""Minimizes the amount of X-axis moves needed to cut a set of polylines."""

from typing import Iterable, List

from cut_optimizer.graph import Vertex
from cut_optimizer.instance import Polyline
from cut_optimizer.labelled_graph import LabelledGraph


class XCoordGraph(LabelledGraph[int, Polyline]):
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
    return polylines
