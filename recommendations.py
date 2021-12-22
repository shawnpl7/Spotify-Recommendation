"""CSC110 Winter 2021: Spotify Recommendation, recommendation module
This module is responsible for generating appropriate song recommendations
given a graph.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Shawn Plotko

"""
from graph import Graph


def get_recommendations(graph: Graph, song: str, chosen_props: list[str],
                        max_songs: int = 5) -> list[str]:
    """Return a list of max_songs recommended song titles as str using the given graph,
    a song and a list of the chosen properties.

    Only the chosen properties are utilized to generate the similarity scores.

    Preconditions:
        - song in graph.get_all_vertices('song')
        - max_songs >= 1
        - all elements of chosen_props are valid properties

    """
    rec = []
    for _ in range(max_songs):
        most_sim = _max_similarity(graph, song, rec, chosen_props)
        if most_sim != '':
            rec.append(most_sim)
    return rec


def _max_similarity(graph: Graph, song: str, rec: list,
                    chosen_props: list[str]) -> str:
    """Return a str corresponding to a song in graph that has the highest
    similarity score with the given song.

     Preconditions:
        - song in graph.get_all_vertices('song')
        - all elements of chosen_props are valid properties

    """
    most_similar_so_far = ''
    max_so_far = 0
    for other in graph.get_all_vertices('song'):
        score = graph.get_similarity_score(song, other, chosen_props)
        if other != song and other not in rec:
            if 0 < score > max_so_far or (
                    score > 0 and score == max_so_far and other > most_similar_so_far):
                max_so_far = score
                most_similar_so_far = other
    return most_similar_so_far


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
