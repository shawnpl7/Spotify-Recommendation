"""CSC110 Winter 2021: Spotify Recommendation, graph module
Contains the _Vertex and Graph class and is responsible for the graph and vertex
properties ad methods. Generates similarity scores.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Shawn Plotko

"""
from __future__ import annotations
from typing import Any


class _Vertex:
    """ A vertex of a Graph. Either represents a user or a song
    within a Graph.

    Instance Attributes:
        - item: The data stored in the vertex, represents a song or a user.
        - kind: The kind of data represented by the vertex. Either a song or user.
        - neighbours: The vertices that are adjacent to this vertex.
        - properties: The properties of vertex item. Empty when vertex is a user.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, float]
    properties: {}

    def __init__(self, item: Any, kind: str, properties: dict) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex has no neighbours when initialized.

        Preconditions:
            - kind in {'user', 'song'}
        """
        self.item = item
        self.kind = kind
        self.properties = properties
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def adjacency_similarity_score(self, other: _Vertex) -> float:
        """Return the similarity score between this vertex and other.

        Uses the amount of items that are adjacent to either this vertex or other,
        the amount of vertices adjacent to both, and the likeability score

        Only considers the users that like the songs the same amount

        """
        if self.degree() == 0 or other.degree() == 0:
            return 0
        else:
            adj_or = len(set(self.neighbours.keys()).union(set(other.neighbours.keys())))
            adj_and = len(set(self.neighbours.keys()).intersection(set(other.neighbours.keys())))
            return adj_and / adj_or

    def property_similarity(self, other: _Vertex, chosen_props: list[str]) -> float:
        """Return the similarity score between the vertex and other based on
        the average variation between the value of chosen properties in
        chosen_props

        Preconditions:
            - all(prop in self.properties for prop in chosen_props)

        """
        sum_diff_so_far = 0
        for prop in chosen_props:
            diff = abs(self.properties[prop] - other.properties[prop])
            sum_diff_so_far += diff

        if len(chosen_props) > 0:
            return sum_diff_so_far / len(chosen_props)
        else:
            return 0


class Graph:
    """A graph used to represent a song review network.

    Private Instance Attributes:
       - _vertices: A collection of the vertices contained in this graph.
                    Maps item to _Vertex object.
    """

    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str, properties: dict) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'song'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind, properties)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            if v2 in v1.neighbours:
                v1.neighbours[v2] += 1
                v2.neighbours[v1] += 1
            else:
                v1.neighbours[v2] = 0
                v2.neighbours[v1] = 0
        else:
            raise ValueError

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'song'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_similarity_score(self, item1, item2, chosen_props: list[str]) -> float:
        """Return the similarity score between the two given items in this graph.

        Use the properties in chosen_props to generate the property similarity score

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            score = v1.adjacency_similarity_score(v2) \
                + v1.property_similarity(v2, chosen_props)
            return score
        else:
            raise ValueError


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9999', 'E1101', 'E9998']

    })

    import doctest

    doctest.testmod(verbose=True)
