"""
Define the Statut class of the Trombinoscope facebook software.
"""

import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error as MysqlError


class Statut:
    """Describe a Statut line from statuts table in database.
    """

    def __init__(self, trombinoscope, id_statut=None, qualification=""):
        self.trombinoscope = trombinoscope
        self._id_statut = id_statut
        self.qualification = qualification
        self.main_ui = None
        self.qualification_entry = None

    @property
    def id_statut(self):
        """Property for read-only id_statut value.

        :return integer: self._id_statut
        """
        return self._id_statut

    def edit(self):
        """Show an UI to edit this Statut.
        """
        title = "Ajout d'un statut"
        save_label = "Ajouter"
        if self.id_statut != 0:
            title = "Edition du statut n°{id_statut}".format(id_statut=self.id_statut)
            save_label = "Enregistrer"

        self.main_ui = tk.Tk()
        self.main_ui.title(title)

        save_icon = tk.PhotoImage(
            master=self.main_ui,
            file=self.trombinoscope.config["branding"]["image_path"]
            + "/"
            + self.trombinoscope.config["branding"]["save_icon"],
        )
        cancel_icon = tk.PhotoImage(
            master=self.main_ui,
            file=self.trombinoscope.config["branding"]["image_path"]
            + "/"
            + self.trombinoscope.config["branding"]["cancel_icon"],
        )

        # Build the bottom buttons frame.
        buttons_frame = tk.Frame(self.main_ui)
        statut_add_button = tk.Button(
            buttons_frame,
            image=save_icon,
            text=save_label,
            compound=tk.LEFT,
            command=self.update,
        )
        statut_add_button.pack(padx="5px", side=tk.LEFT)
        statut_edit_button = tk.Button(
            buttons_frame,
            image=cancel_icon,
            text="Annuler",
            compound=tk.LEFT,
            command=self.main_ui.destroy,
        )
        statut_edit_button.pack(padx="5px", side=tk.LEFT)
        buttons_frame.pack(pady="5px", side=tk.BOTTOM)

        # Build the qualification entry frame.
        entry_frame = tk.Frame(self.main_ui)
        qualification_entry_label = tk.Label(entry_frame, text="Qualification:")
        qualification_entry_label.pack(padx="5px", side=tk.LEFT)
        self.qualification_entry = tk.Entry(entry_frame, exportselection=0)
        self.qualification_entry.insert(tk.END, self.qualification)
        self.qualification_entry.pack(padx="5px", side=tk.LEFT)
        entry_frame.pack(pady="5px", side=tk.TOP)

        self.main_ui.mainloop()

    def delete(self):
        """Delete this Statut from database.
        """
        answer = messagebox.askquestion(
            "Supprimer le statut n°{id_statut} ?".format(id_statut=self.id_statut),
            "Voulez-vous vraiment supprimer le statut '{qualification}' ?".format(
                qualification=self.qualification
            ),
            icon="warning",
            parent=self.trombinoscope.statut_manager.main_ui,
        )
        if answer == "no":
            return False

        if self.main_ui:
            self.main_ui.destroy()

        sql_queries = "DELETE FROM statut WHERE id_statut=%(id_statut)s"
        sql_queries_params = {"id_statut": self.id_statut}

        # Create the database cursor.
        cursor = self.trombinoscope.database.cursor()

        # Execute the query
        try:
            cursor.execute(sql_queries, params=sql_queries_params)

            # Commit the change.
            self.trombinoscope.database.commit()
        except MysqlError as mysql_error:
            # Affiche une alerte pour l'erreur.
            error_message = "Impossible de supprimer le statut :\n" + str(mysql_error)
            messagebox.showerror(
                "Erreur",
                error_message,
                parent=self.trombinoscope.statut_manager.main_ui,
            )
        finally:
            cursor.close()
            self.trombinoscope.statut_manager.refresh()
            self.trombinoscope.statut_manager.main_ui.focus_force()

    def update(self):
        """Update the database record for this Statut.
      """
        updated_qualification = self.qualification_entry.get().strip()

        # Check that qualification is not empty.
        if len(updated_qualification) == 0:
            messagebox.showerror(
                "Erreur",
                "La qualification est obligatoire !",
                parent=self.trombinoscope.statut_manager.main_ui,
            )
            self.main_ui.focus_force()
            return False
        self.qualification = updated_qualification

        # Destroy editor window.
        self.main_ui.destroy()

        # Prepare the SQL queries.
        sql_queries = "INSERT INTO statut(qualification) VALUES (%(qualification)s)"
        sql_queries_params = {"qualification": self.qualification}

        if self.id_statut is not None:
            sql_queries = """UPDATE statut SET qualification = %(qualification)s
                                          WHERE id_statut=%(id_statut)s"""
            sql_queries_params["id_statut"] = self.id_statut

        # Create the database cursor.
        cursor = self.trombinoscope.database.cursor()

        # Execute the query
        try:
            cursor.execute(sql_queries, params=sql_queries_params)
            if self.id_statut is None:
                self._id_statut = cursor.lastrowid

            # Commit the change.
            self.trombinoscope.database.commit()
        except MysqlError as mysql_error:
            # Affiche une alerte pour l'erreur.
            error_message = "Impossible de mettre à jour le statut :\n" + str(
                mysql_error
            )
            messagebox.showerror("Erreur", error_message, parent=self.main_ui)
            self.main_ui.focus_force()
        finally:
            cursor.close()
            self.trombinoscope.statut_manager.refresh()
            self.trombinoscope.statut_manager.main_ui.focus_force()
