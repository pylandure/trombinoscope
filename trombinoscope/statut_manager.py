"""
Define the StatutManager class of the Trombinoscope facebook software.
"""

import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error as MysqlError

from .statut import Statut


class StatutManager:
    """Create a managing UI for statuts.
    """
    def __init__(self, trombinoscope):
        """ Instanciate a StatutManager

    :param trombinoscope: the parent Trombinoscope
    """
        self.trombinoscope = trombinoscope
        self.statuts_listbox = None
        self.main_ui = None
        self.refresh()

    def refresh_list_box(self):
        """Refresh the self.statuts_listbox contents.
    """
        if not self.statuts_listbox:
            return False

        # Empty the exisiting listbox.
        self.statuts_listbox.delete(0, tk.END)

        for statut in self.statuts.values():
            self.statuts_listbox.insert(tk.END, statut.qualification)

    def refresh(self):
        """Empty the statuts cache to force a reload from database.
    Call self.refresh_list_box()
    """
        self._statuts = {}
        self._statuts_by_qualification = {}
        return self.refresh_list_box()

    @property
    def statuts(self, refresh=False):
        """ Load statuts from database

    :param refresh: True to reload statuts from database, default to False.
    :return A list of Statut.
    """

        # Reset statuts cache on refresh.
        if refresh:
            self.refresh()

        if len(self._statuts) == 0:
            sql_queries = (
                "SELECT id_statut, qualification FROM statut ORDER BY qualification ASC"
            )
            cursor = self.trombinoscope.database.cursor()

            try:
                cursor.execute(sql_queries)
                for (id_statut, qualification) in cursor:
                    self._statuts[id_statut] = Statut(
                        self.trombinoscope, id_statut, qualification
                    )
                    self._statuts_by_qualification[qualification] = self._statuts[
                        id_statut
                    ]
            except MysqlError as mysql_error:
                error_message = "Impossible de récupérer les genres:\n" + str(
                    mysql_error
                )

                # Affiche une alerte pour l'erreur.
                messagebox.showerror("Erreur", error_message)
            finally:
                cursor.close()

        return self._statuts

    @property
    def statuts_by_qualification(self, refresh=False):
        """ Load statuts from database

    :param refresh: True to reload statuts from database, default to False.
    :return A list of Statut.
    """

        # Reset statuts cache on refresh.
        if refresh:
            self.refresh()

        if len(self._statuts_by_qualification) == 0:
            # Reload from database
            statuts=self.statuts
            del statuts

        return self._statuts_by_qualification

    @property
    def selected_statut(self):
        """Get the Statut selected in self.statuts_listbox.

    Returns:
        Statut: The statut selected in self.statuts_listbox.
    """
        selected_qualification = self.statuts_listbox.get(tk.ACTIVE)
        statut = self.statuts_by_qualification.get(selected_qualification, None)
        return statut

    def add_new_statut(self):
        """Call Statut.edit() on a new Statut
    """
        statut = Statut(self.trombinoscope)
        return statut.edit()

    def edit_selected_statut(self):
        """Call Statut.edit() for selected statut in self.statuts_listbox
    """
        statut = self.selected_statut
        if statut:
            return statut.edit()
        return False

    def delete_selected_statut(self):
        """Call Statut.delete() for selected statut in self.statuts_listbox
    """
        statut = self.selected_statut
        if statut:
            return statut.delete()
        return False

    def open_ui(self):
        """ Open the main statut management UI
    """
        self.main_ui = tk.Tk()
        self.main_ui.title("Gestion des statuts")
        self.main_ui.geometry("225x150")

        add_icon = tk.PhotoImage(
            master=self.main_ui,
            file=self.trombinoscope.config["branding"]["image_path"]
            + "/"
            + self.trombinoscope.config["branding"]["add_icon"],
        )
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

        # Build the bottom buttons frame.
        buttons_frame = tk.Frame(self.main_ui)
        statut_add_button = tk.Button(
            buttons_frame, image=add_icon, text="Ajouter", command=self.add_new_statut
        )
        statut_add_button.pack(padx="5px", side=tk.LEFT)
        statut_edit_button = tk.Button(
            buttons_frame,
            image=edit_icon,
            text="Modifier",
            command=self.edit_selected_statut,
        )
        statut_edit_button.pack(padx="5px", side=tk.LEFT)
        statut_delete_button = tk.Button(
            buttons_frame,
            image=delete_icon,
            text="Supprimer",
            command=self.delete_selected_statut,
        )
        statut_delete_button.pack(padx="5px", side=tk.LEFT)
        buttons_frame.pack(pady="5px", side=tk.BOTTOM)

        statuts_listbox_scrollbar = tk.Scrollbar(self.main_ui)
        statuts_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.statuts_listbox = tk.Listbox(
            self.main_ui, yscrollcommand=statuts_listbox_scrollbar.set
        )
        self.refresh_list_box()
        self.statuts_listbox.pack(expand=True, fill=tk.BOTH)

        self.main_ui.mainloop()
