"""CSC110 Winter 2021: Spotify Recommendation, main module
This module is responsible for generating a graph given the appropriate datasets.
Responsible for running the main program.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Shawn Plotko

"""
from graph import Graph
from visualization import Window


def generate_graph(song_file: str, playlist_file: str) -> Graph:
    """Generate and return a Graph object populated with songs
    and users as given in both song_file and playlist_file

    Preconditions:
        - song_file is formatted the same as song_data.txt
        - playlist_file is formatted the same as playlist_data.txt
    """
    g = Graph()
    songs = _load_songs(song_file)
    file = open(playlist_file, "r")
    user_id = 0
    for row in file:
        row_as_lst = row.split(',')
        user_id += 1
        g.add_vertex(user_id, 'user', {})
        for song in row_as_lst:
            if song in songs:
                properties = {'Energy': songs[song][0], 'Liveness': songs[song][1],
                              'Loudness': songs[song][2], 'Tempo': songs[song][3]}
                g.add_vertex(song, 'song', properties)
                g.add_edge(user_id, song)

    return g


def _load_songs(song_file: str) -> dict[str, list]:
    """Return a dict mapping each song name in song_file
    to a list of its property values

    Property values include Energy, Liveness, Loudness, and Tempo

    Preconditions:
        - song_file is formatted the same as song_data.txt

    """
    file = open(song_file, "r")
    song_data_so_far = {}
    file.readline()
    for row in file:
        row_as_lst = row.split(',')
        song_data_so_far[row_as_lst[9]] = []
        properties = [float(row_as_lst[1]), float(row_as_lst[6]),
                      float(row_as_lst[7]), float(row_as_lst[13])]
        song_data_so_far[row_as_lst[9]].extend(properties)
    file.close()
    return song_data_so_far


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

    # Generates graph and creates window
    graph = generate_graph('spotify_data\\song_data.txt', 'spotify_data\\playlist_data.txt')
    w = Window(graph)
