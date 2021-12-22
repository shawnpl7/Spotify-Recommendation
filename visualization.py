"""CSC110 Winter 2021: Spotify Recommendation, visualization module
Contains the Window class and is responsible for visual/interactive components

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Shawn Plotko

"""

from tkinter import *
import recommendations
from graph import Graph


class Window:
    """The main visualization window. Displays appropriate user interface
    elements and allows for user input.

    Instance Attributes:
        - graph: The Graph used to output song recommendations
        - song_entry: A tkinter Entry element use to get user's song
        - rec_list: A tkinter Listbox used to display recommendations
        - error_lbl: A tkinter Label that displays relevant error messages
        - energy_chkbtn_stat: A tkinter IntVar, stores status of energy Checkbutton
        - liveness_chkbtn_stat: A tkinter IntVar, stores status of liveness Checkbutton
        - loudness_chkbtn_stat: A tkinter IntVar, stores status of loudness Checkbutton
        - tempo_chkbtn_stat: A tkinter IntVar, stores status of tempo Checkbutton

    """
    graph: Graph
    song_entry: Entry
    rec_list: Listbox
    error_lbl: Label
    energy_chkbtn_stat: IntVar
    liveness_chkbtn_stat: IntVar
    loudness_chkbtn_stat: IntVar
    tempo_chkbtn_stat: IntVar

    def __init__(self, g: Graph) -> None:
        """ Initialize a new Window with the given graph.
        Creates all necessary Window elements

        """
        self.graph = g

        window = Tk()
        btn = Button(window, text="Get Recommendation!", command=self.show_recommended)
        btn.place(x=300, y=350)

        self.error_lbl = Label(window, text='Invalid Input')

        self.energy_chkbtn_stat = IntVar()
        self.tempo_chkbtn_stat = IntVar()
        self.liveness_chkbtn_stat = IntVar()
        self.loudness_chkbtn_stat = IntVar()

        tempo_chkbtn = Checkbutton(window, text='Tempo',
                                   variable=self.tempo_chkbtn_stat, onvalue=1, offvalue=0)
        loudness_chkbtn = Checkbutton(window, text='Loudness',
                                   variable=self.loudness_chkbtn_stat, onvalue=1, offvalue=0)
        liveness_chkbtn = Checkbutton(window, text='Liveness',
                                   variable=self.liveness_chkbtn_stat, onvalue=1, offvalue=0)
        energy_chkbtn = Checkbutton(window, text='Energy',
                                   variable=self.energy_chkbtn_stat, onvalue=1, offvalue=0)

        chkbtn_x = 50
        tempo_chkbtn.place(x=chkbtn_x, y=100)
        loudness_chkbtn.place(x=chkbtn_x, y=150)
        liveness_chkbtn.place(x=chkbtn_x, y=200)
        energy_chkbtn.place(x=chkbtn_x, y=250)

        self.rec_list = Listbox()
        self.rec_list.place(x=300, y=100)

        self.song_entry = Entry()
        self.song_entry.place(x=300, y=300)

        heading_lbl = Label(window, text='Recommendations', font='Ariel 18 bold')
        heading_lbl.place(x=250, y=50)

        note_lbl = Label(window, text='Note: Songs are case sensitive', font='Ariel 12')
        note_lbl.place(x=40, y=300)

        window.title('Spotify Recommendations')
        window.geometry("600x500")
        window.mainloop()

    def show_recommended(self) -> None:
        """ Generate and display the appropriate recommendations when
        the btn is pressed by the user.
        """
        self.error_lbl.place(x=1000, y=300)
        song = self.song_entry.get()
        if song in self.graph.get_all_vertices('song'):
            chosen_props = self._get_properties()
            rec = recommendations.get_recommendations(self.graph, song, chosen_props)
            self.rec_list.delete(0, END)
            for s in rec:
                self.rec_list.insert(END, s)
        else:
            self.error_lbl.place(x=500, y=300)

    def _get_properties(self) -> list[str]:
        """ Return the selected properties to use
        in the recommendation generation algorithm as a list
        of str.

        Each str represents a selected property

        """
        chosen_props = []
        if self.tempo_chkbtn_stat.get() == 1:
            chosen_props.append('Tempo')
        if self.energy_chkbtn_stat.get() == 1:
            chosen_props.append('Energy')
        if self.liveness_chkbtn_stat.get() == 1:
            chosen_props.append('Liveness')
        if self.loudness_chkbtn_stat.get() == 1:
            chosen_props.append('Loudness')
        return chosen_props


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
