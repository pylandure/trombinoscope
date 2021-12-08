"""
This module manage the main window of the Trombinoscope facebook software.
"""
import sys
import tkinter as tk
from tkinter import messagebox
import yaml
import mysql.connector

from trombinoscope.genre_manager import GenreManager
from trombinoscope.statut_manager import StatutManager


class Trombinoscope:
    """
  This class manage the loading of the Trombinoscope app and display its main window.
  """

    version = 0.1

    def __init__(self):
        """
    Set trombinoscope defaults.

    :return: returns nothing
    """
        self.main_ui = None
        self.genre_manager = None
        self.statut_manager = None
        self.load_configuration()
        self.connect_to_database()

    def load_configuration(self):
        """Set the default configuration and load custom settings from YAML configuration file.

    :raise SystemExit
    """
        self.config = {
            "defaults": {"photo_path": "./photos"},
            "database": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "root",
                "database": "trombinoscope",
            },
            "branding": {
                "window_title": "Trombinoscope Simplon",
                "window_size": "400x400",
                "image_path": "./trombinoscope/images/",
                "add_icon": "add.png",
                "edit_icon": "edit.png",
                "delete_icon": "delete.png",
                "save_icon": "save.png",
                "cancel_icon": "cancel.png",
                "odd_line_background": "snow",
                "even_line_background": "LightBlue1",
            },
        }

        try:
            yml_configuration_file = open("trombinoscope/config/trombinoscope.yml", "r")

            try:
                custom_config = yaml.safe_load(yml_configuration_file)

                # Apply custom settings from yaml.
                for section in self.config.keys():
                    if section in custom_config.keys():
                        for key, value in custom_config[section].items():
                            self.config[section][key] = value

            except (yaml.parser.ScannerError, yaml.parser.ParserError, AttributeError):
                messagebox.showerror(
                    "Erreur",
                    "Le fichier de configuration n'a pas un format YAML valide.",
                )
                sys.exit()

            yml_configuration_file.close()
        except (FileNotFoundError, IOError):
            messagebox.showerror(
                "Erreur", "Impossible de charger le fichier de configuration !"
            )
            sys.exit()

    def connect_to_database(self):
        """Open a connection to the database, and store it in the database property.
    """
        try:
            self.database = mysql.connector.connect(**self.config["database"])
        except mysql.connector.Error as mysql_error:
            error_message = "Impossible de se connecter à la base de données !"
            if mysql_error.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                error_message += \
                    "\nLogin/mot de passe incorrect pour l'utilisateur '{user}'.".format(
                        user=self.config["database"]["user"]
                    )
            elif mysql_error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                error_message += "\nLa base de données '{database}' n'existe pas.".format(
                    database=self.config["database"]["database"]
                )
            else:
                error_message += "\n" + str(mysql_error)

            # Affiche une alerte pour l'erreur et quitte l'application.
            messagebox.showerror("Erreur", error_message)
            sys.exit()

    def about(self):
        """
    Display a message box about this software.

    :return: returns nothing
    """
        messagebox.showinfo(
            "A propos du Trombinoscope",
            """
Trombinoscope {version}

Ce trombinoscope a été créé pour Simplon
durant l'école IA Microsoft Yncrea.

Copyright 2021 Pierre-Yves Landuré, Kevin
""".format(
                version=self.version
            ),
        )

    def quit(self):
        """
    Display a message box to ask for confirmation before exiting the software.

    :return: returns nothing
    """
        answer = messagebox.askquestion(
            "Quitter le trombinoscope",
            "Voulez-vous vraiment sortir du trombinoscope ?",
            icon="error",
        )
        if answer == "yes":
            # Close database before exit.
            if self.main_ui:
                self.main_ui.destroy()
            if self.database:
                self.database.close()

            sys.exit()

    def open_genre_manager(self):
        """ Open a GenreManager UI.
    """
        self.genre_manager = GenreManager(self)
        self.genre_manager.open_ui()

    def open_statut_manager(self):
        """ Open a StatutManager UI
    """
        self.statut_manager = StatutManager(self)
        self.statut_manager.open_ui()

    def open_ui(self):
        """ Create and display the main window for the Trombinoscope app.

    :return: returns nothing
    """
        self.main_ui = tk.Tk()
        self.main_ui.title(self.config["branding"]["window_title"])
        self.main_ui.geometry(self.config["branding"]["window_size"])

        # Build a menu bar for the window.
        menubar = tk.Menu(self.main_ui)

        filemenu = tk.Menu(self.main_ui)
        filemenu.add_command(label="Gérer les genres", command=self.open_genre_manager)
        filemenu.add_command(
            label="Gérer les statuts", command=self.open_statut_manager
        )
        filemenu.add_command(label="A propos", command=self.about)
        filemenu.add_command(label="Quitter", command=self.quit)

        menubar.add_cascade(label="Fichier", menu=filemenu)

        self.main_ui.config(menu=menubar)

        # Add a confirmation message box on window close.
        self.main_ui.protocol("WM_DELETE_WINDOW", self.quit)

        # quit_button=tk.Button(self.main_ui, text="Quitter", command=quit)
        # quit_button.pack(side='west', padx=5, pady=5)
        # quit_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E+tk.N)

        self.main_ui.mainloop()

    @staticmethod
    def start():
        """ Instance a new Trombinoscope and open its UI.

    :return: returns nothing
    """
        trombinoscope = Trombinoscope()
        trombinoscope.open_ui()
