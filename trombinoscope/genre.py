"""
Define the Genre class of the Trombinoscope facebook software.
"""

import tkinter as tk

class Genre:
    """Describe a Genre line from genres table in database.
    """
    def __init__(self, trombinoscope, id_genre, genre):
        self.trombinoscope = trombinoscope
        self._id_genre = id_genre
        self.genre = genre
        self.main_ui = None

    @property
    def id_genre(self):
        """Property for read-only id_genre value.

    :return integer: id_genre
    """
        return self._id_genre

    def edit(self):
        """[summary]
    """
        self.main_ui = tk.Tk()
        self.main_ui.title(
            "Edition du statut" if self.id_genre != 0 else "Ajout d'un statut"
        )
        # self.main_ui.geometry('225x150')
        self.main_ui.mainloop()

    def delete(self):
        """[summary]
        """

    def update(self):
        """[summary]
        """
