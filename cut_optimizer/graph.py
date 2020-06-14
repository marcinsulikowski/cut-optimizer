"""Generic representation of a graph."""

from typing import Dict, Iterable, Set
from multiset import Multiset


class Vertex:
    """Vertex in a graph."""


class Edge:
    """Edge in a graph."""

    def __init__(self, vertex_1: Vertex, vertex_2: Vertex) -> None:
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2

    def other_end(self, vertex: Vertex) -> Vertex:
        """Given one of ends, return the other end."""
        if vertex == self.vertex_1:
            return self.vertex_2
        elif vertex == self.vertex_2:
            return self.vertex_1
        else:
            raise ValueError(vertex)


class Graph:
    """Undirected graph."""

    def __init__(self) -> None:
        self.edges: Set[Edge] = set()
        self.neighbors: Dict[Vertex, "Multiset[Edge]"] = {}

    @property
    def vertices(self) -> Iterable[Vertex]:
        """Return all vertices fo the graph."""
        return self.neighbors.keys()

    def clone(self) -> "Graph":
        """Create a new graph with the same set of vertices and edges."""
        cloned = Graph()
        for vertex in self.vertices:
            cloned.add_vertex(vertex)
        for edge in self.edges:
            cloned.add_edge(edge)
        return cloned

    def add_vertex(self, vertex: Vertex) -> Vertex:
        """Add a new vertex to the graph."""
        assert vertex not in self.neighbors
        self.neighbors[vertex] = Multiset()
        return vertex

    def add_edge(self, edge: Edge) -> Edge:
        """Add a new edge to the graph."""
        assert edge not in self.edges
        assert edge.vertex_1 in self.neighbors
        assert edge.vertex_2 in self.neighbors
        self.neighbors[edge.vertex_1].add(edge, multiplicity=1)
        self.neighbors[edge.vertex_2].add(edge, multiplicity=1)
        self.edges.add(edge)
        return edge

    def remove_edge(self, edge: Edge) -> None:
        """Remove an edge form the graph."""
        self.neighbors[edge.vertex_1].remove(edge, multiplicity=1)
        self.neighbors[edge.vertex_2].remove(edge, multiplicity=1)
        self.edges.remove(edge)

    def get_vertex_degree(self, vertex: Vertex) -> int:
        """Get a degree of a given vertex."""
        return len(self.neighbors[vertex])

    def is_even_degree(self, vertex: Vertex) -> bool:
        """Tell if the degree of a given vertex is even."""
        return self.get_vertex_degree(vertex) % 2 == 0
