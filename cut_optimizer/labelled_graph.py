"""A wrapper class for Graph which adds tags for vertices and edges."""

from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    overload,
    Sequence,
    Set,
    TypeVar,
    Union,
)

from cut_optimizer.graph import Edge, Graph, Vertex

_VertexTag = TypeVar("_VertexTag")
_EdgeTag = TypeVar("_EdgeTag")


class _NoArgument:
    """A helper class used detect skipped arguments in function calls."""


class LabelledGraph(Graph, Generic[_VertexTag, _EdgeTag]):
    """Graph where each vertex and edge can be assigned some value."""

    def __init__(self) -> None:
        super().__init__()
        # Mapping from graph elements to tags
        self.edge_tags: Dict[Edge, _EdgeTag] = {}
        self.vertex_tags: Dict[Vertex, _VertexTag] = {}
        # Reverse mappings:
        self.tag_to_edges: Dict[_EdgeTag, Set[Edge]] = {}
        self.tag_to_vertices: Dict[_VertexTag, Set[Vertex]] = {}

    def remove_edge(self, edge: Edge) -> None:
        """Override the method from the superclass to also remove a tag."""
        super().remove_edge(edge)
        try:
            tag = self.edge_tags[edge]
        except KeyError:
            # The edge didn't have any tag which is OK
            pass
        else:
            del self.edge_tags[edge]
            edges_with_tag = self.tag_to_edges[tag]
            edges_with_tag.remove(edge)
            if not edges_with_tag:
                del self.tag_to_edges[tag]

    def add_tagged_vertex(self, tag: _VertexTag) -> Vertex:
        """Add single vertex with a given tag."""
        vertex = super().add_vertex(Vertex())
        self.vertex_tags[vertex] = tag
        if tag in self.tag_to_vertices:
            self.tag_to_vertices[tag].add(vertex)
        else:
            self.tag_to_vertices[tag] = {vertex}
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
            if tag in self.tag_to_edges:
                self.tag_to_edges[tag].add(edge)
            else:
                self.tag_to_edges[tag] = {edge}
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

    def get_vertex_tags(self) -> Iterable[_VertexTag]:
        """Return all vertex tags."""
        return self.tag_to_vertices.keys()

    def get_edge_tags(self) -> Iterable[_EdgeTag]:
        """Return all edge tags."""
        return self.tag_to_edges.keys()

    def get_vertex(self, tag: _VertexTag) -> Vertex:
        """Return a vertex given its tag.

        :raises KeyError: if there's no vertex with the given tag.
        :raises ValueError: if there's more than 1 vertex with the given tag.
        """
        candidates = self.tag_to_vertices[tag]
        if len(candidates) == 1:
            return next(iter(candidates))
        else:
            raise ValueError(tag)

    def get_edge(self, tag: _EdgeTag) -> Edge:
        """Return an edge given its tag.

        :raises KeyError: if there's no edge with the given tag.
        :raises ValueError: if there's more than 1 edge with the given tag.
        """
        candidates = self.tag_to_edges[tag]
        if len(candidates) == 1:
            return next(iter(candidates))
        else:
            raise ValueError(tag)
