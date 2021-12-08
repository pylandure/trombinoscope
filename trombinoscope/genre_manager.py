"""
Define the GenreManager class of the Trombinoscope facebook software.
"""

import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error as MysqlError

from .genre import Genre


class GenreManager:
    """Create a managing UI for genres.
    """

    def __init__(self, trombinoscope):
        """ Instanciate a GenreManager

    :param trombinoscope: the parent Trombinoscope
    """
        self.trombinoscope = trombinoscope
        self.main_ui = None

    def get_genres(self):
        """ Load genres from database

    :return A list of Genre.
    """
        genres = []
        sql_queries = "SELECT id_genre, genre FROM genre ORDER BY genre ASC"
        cursor = self.trombinoscope.db.cursor()

        try:
            cursor.execute(sql_queries)
            for (id_genre, genre) in cursor:
                genres.append(Genre(self.trombinoscope, id_genre, genre))
        except MysqlError as mysql_error:
            error_message = "Impossible de récupérer les genres:\n" + str(mysql_error)

            # Affiche une alerte pour l'erreur.
            messagebox.showerror("Erreur", error_message)
        finally:
            cursor.close()

        return genres

    def open_ui(self):
        """ Open the main genre management UI
    """

        self.main_ui = tk.Tk()
        self.main_ui.title("Gestion des genres")
        self.main_ui.geometry("225x150")

        odd_background = self.trombinoscope.config["branding"]["odd_line_background"]
        even_background = self.trombinoscope.config["branding"]["even_line_background"]

        edit_icon = tk.PhotoImage(
            master=self.main_ui,
            file=self.trombinoscope.config["branding"]["image_path"]
            + "/"
            + self.trombinoscope.config["branding"]["edit_icon"],
        )
        delete_icon = tk.PhotoImage(
            master=self.main_ui,
            file=self.trombinoscope.config["branding"]["image_path"]
            + "/"
            + self.trombinoscope.config["branding"]["delete_icon"],
        )

        genres = self.get_genres()

        current_row = 0
        for genre in genres:
            background_color = (
                odd_background if current_row % 2 == 0 else even_background
            )
            genre_label = tk.Label(
                self.main_ui,
                text=genre.genre,
                width=25,
                anchor="w",
                justify="left",
                background=background_color,
            )
            genre_label.grid(row=current_row, column=0, sticky="W")

            genre_edit_button = tk.Button(
                self.main_ui,
                image=edit_icon,
                text="Modifier",
                relief="flat",
                background=background_color,
                command=genre.edit,
            )
            genre_edit_button.grid(row=current_row, column=1)

            genre_edit_button = tk.Button(
                self.main_ui,
                image=delete_icon,
                text="Supprimer",
                relief="flat",
                background=background_color,
                command=genre.delete,
            )
            genre_edit_button.grid(row=current_row, column=2)

            current_row += 1

        self.main_ui.mainloop()
