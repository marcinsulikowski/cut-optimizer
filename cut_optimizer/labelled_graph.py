"""A wrapper class for Graph which adds tags for vertices and edges."""

from typing import Any, Dict, Generic, overload, Sequence, TypeVar, Union

from cut_optimizer.graph import Edge, Graph, Vertex

_VertexTag = TypeVar("_VertexTag")
_EdgeTag = TypeVar("_EdgeTag")


class _NoArgument:
    """A helper class used detect skipped arguments in function calls."""


class LabelledGraph(Graph, Generic[_VertexTag, _EdgeTag]):
    """Graph where each vertex and edge can be assigned some value."""

    def __init__(self) -> None:
        super().__init__()
        self.edge_tags: Dict[Edge, _EdgeTag] = {}
        self.vertex_tags: Dict[Vertex, _VertexTag] = {}

    def remove_edge(self, edge: Edge) -> None:
        """Override the method from the superclass to also remove a tag."""
        super().remove_edge(edge)
        try:
            del self.edge_tags[edge]
        except KeyError:
            # The edge didn't have any tag which is OK
            pass

    def add_tagged_vertex(self, tag: _VertexTag) -> Vertex:
        """Add single vertex with a given tag."""
        vertex = super().add_vertex(Vertex())
        self.vertex_tags[vertex] = tag
        return vertex

    def add_tagged_vertices(self, tags: Sequence[_VertexTag]) -> None:
        """Add a set of vertices with given tags."""
        for tag in tags:
            self.add_tagged_vertex(tag)

    def add_tagged_edge(
        self,
        vertex_1: Union[_VertexTag, Vertex],
        vertex_2: Union[_VertexTag, Vertex],
        tag: Union[_EdgeTag, _NoArgument] = _NoArgument(),
    ) -> Edge:
        """Add an edge connecting two vertices.

        Vertices may be given either directly or by their tags. If `tag` is
        given, the created edge is tagged with that tag.
        """
        if not isinstance(vertex_1, Vertex):
            vertex_1 = self.get_vertex(vertex_1)
        if not isinstance(vertex_2, Vertex):
            vertex_2 = self.get_vertex(vertex_2)
        edge = self.add_edge(Edge(vertex_1, vertex_2))
        if not isinstance(tag, _NoArgument):
            self.edge_tags[edge] = tag
        return edge

    @overload
    def get_tag(self, element: Vertex) -> _VertexTag:
        pass

    @overload
    def get_tag(self, element: Edge) -> _EdgeTag:
        pass

    def get_tag(self, element: Union[Vertex, Edge]) -> Any:
        """Return a tag of the given edge/vertex."""
        if isinstance(element, Edge):
            return self.edge_tags[element]
        else:
            return self.vertex_tags[element]

    def get_vertex(self, tag: _VertexTag) -> Vertex:
        """Return a vertex given its tag."""
        for vertex, vertex_tag in self.vertex_tags.items():
            if vertex_tag == tag:
                return vertex
        raise KeyError(tag)

    def get_edge(self, tag: _EdgeTag) -> Edge:
        """Return an edge given its tag."""
        for edge, edge_tag in self.edge_tags.items():
            if edge_tag == tag:
                return edge
        raise KeyError(tag)
