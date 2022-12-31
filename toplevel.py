"""Author: Szymon Lasota
Module contains all Toplevel windows, for gathering information from
user. There are several of them:

* EnterMath is used for choosing equation to be written or creating
new one, that can be saved for later,
* EnterTable is used for importing excel or csv files, reading them and
writing tables.
* NewProject is used to create new project.
"""
from tkinter import messagebox as msg
from typing import Callable

import pandas as pd
from customtkinter import (CTkButton, CTkEntry, CTkLabel, CTkOptionMenu,
                           CTkTextbox, CTkToplevel, StringVar,
                           set_appearance_mode)

from settings import (SETTINGS, TOP_HEIGHT, TOP_WIDTH, Mode, Separators,
                      update_settings)
from texfigures import LatexMath


class EnterMath(CTkToplevel):
    """Class for creating window allowing to enter equation."""

    def __init__(
            self,
            mode: str,
            insert: Callable[[str, str], None],
            *args, **kwargs
    ) -> None:
        """Constructor of EnterMath class.

        Args:
            mode (str): mode used to write math.
            insert (Callable[[str, str], None]): function responsible
                for inserting equations.


        Raises:
            ValueError: if mode is not valid.
        """
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.title = f"Enter {mode}"
        self.insert = insert
        if mode == Mode.EQUATION:
            self.options = list(LatexMath.EQUATIONS.keys())
        elif mode == Mode.DISPLAYMATH:
            self.options = list(LatexMath.DISPLAYMATH.keys())
        else:
            raise ValueError("Invalid mode")
        self.generate_gui()

    def generate_gui(self) -> None:
        """Generate GUI to display."""
        label = CTkLabel(self, text="Chose what to insert:")
        label.grid(row=0, column=0, columnspan=3)

        variable = StringVar(self, value=self.options[0])

        combobox = CTkOptionMenu(
            self,
            values=self.options,
            variable=variable,
            width=TOP_WIDTH
        )
        combobox.grid(row=1, column=0, columnspan=2)

        text = CTkTextbox(
            self,
            width=TOP_WIDTH,
            height=TOP_HEIGHT//3 * 2
        )
        text.grid(row=3, column=0, columnspan=2, rowspan=2)

        name_label = CTkLabel(
            self,
            text="Enter name and equation then press add button."
        )
        name_label.grid(row=2, column=0, columnspan=2)

        name_entry = CTkEntry(
            self,
        )
        name_entry.grid(row=5, column=0, columnspan=2)

        insert_button = CTkButton(
            self,
            text=f"Insert {self.mode}",
            command=lambda: self.insert(combobox.get(), self.mode)
        )
        insert_button.grid(row=5, column=2)

        add_button = CTkButton(
            self,
            text=f"Add new {self.mode}",
            command=lambda: self.add_new(name_entry.get(), text)
        )
        add_button.grid(row=6, column=2)

    def add_new(self, name: str, textbox: CTkTextbox) -> None:
        """Add new equation to app memeory.

        Args:
            name (str): name of equation.
            textbox (CTkTextbox): textbox containing equation..
        """
        try:
            new_equation = textbox.textbox.get(1.0, "end-1c")
        except AttributeError:
            new_equation = textbox.get(1.0, "end-1c")
        if not new_equation or not name:
            return
        if name in self.options:
            msg.showerror(
                title="Fatal Error",
                message="Equation already exists."
            )
            return
        SETTINGS[self.mode][name] = new_equation
        update_settings(SETTINGS)
        self.destroy()


class EnterTable(CTkToplevel):
    """Class for creating window allowing to insert table."""

    def __init__(
            self,
            path: str,
            add_tab: Callable[[pd.DataFrame], None],
            *args,
            **kwargs
    ) -> None:
        """Constructor of EnterTable class.

        Args:
            path (str): path to file with data
            add_tab (Callable[[pd.DataFrame], None]): function inserting
                the table.
        """
        super().__init__(*args, **kwargs)
        self.title = "Enter Table"
        self.path = path
        self.dfs = {}
        self.add_table = add_tab
        self.generate_gui()

    def generate_gui(self) -> None:
        """Create GUI to display."""
        label_sep = CTkLabel(self, text="Enter separator")
        label_sep.grid(row=0, column=0)

        label_del = CTkLabel(self, text="Enter decimal separator")
        label_del.grid(row=0, column=1)

        var_decimal = StringVar(self, Separators.DECIMAL[0])

        combo_decimal = CTkOptionMenu(
            self,
            values=Separators.DECIMAL,
            variable=var_decimal
        )
        combo_decimal.grid(row=1, column=1)

        var_separator = StringVar(self, Separators.SEPARATORS[0])

        combo_separator = CTkOptionMenu(
            self,
            values=Separators.SEPARATORS,
            variable=var_separator
        )
        combo_separator.grid(row=1, column=0)

        read_file_button = CTkButton(
            self,
            text="Read file",
            command=lambda: self.read_file(
                combo_decimal.get(), combo_separator.get()
            )
        )
        read_file_button.grid(row=1, column=2)

        try:
            sheets_var_text = list(self.dfs.keys())[-1]
        except IndexError:
            sheets_var_text = None
        sheets_var = StringVar(self, sheets_var_text)

        sheets_combo = CTkOptionMenu(
            self,
            values=list(self.dfs.keys()),
            variable=sheets_var
        )
        sheets_combo.grid(row=2, column=0)

        add_button = CTkButton(
            self,
            text="Add table",
            command=lambda: self.add_table(
                self.dfs[sheets_combo.get()]
            )
        )
        add_button.grid(row=2, column=1)

    def read_file(self, decimal: str, sep: str) -> None:
        """Read the file.

        Args:
            decimal (str): Character to separating decimal values.
            sep (str): Character to separating columns.
        """
        if self.path is None:
            msg.showerror(
                title="Wrong file path",
                message="You did not enter path to file!"
            )
        if self.path.endswith(".csv"):
            try:
                self.dfs = {
                    "sheet1": pd.read_csv(
                        self.path,
                        decimal=Separators.representation[decimal],
                        sep=Separators.representation[sep]
                    )
                }
            except pd.errors.ParserError:

                msg.showerror(
                    title="Fatal error",
                    message=(
                        "Error occurred while reading file, make sure"
                        + " you pass correct separators and decimal separator"
                    )
                )
            self.generate_gui()
            return
        if not self.path.endswith(".xlsx"):
            msg.showerror(
                title="Wrong file path",
                message="File should be .csv or .xlsx type!"
            )
        self.dfs = pd.read_excel(
            self.path,
            decimal=Separators.representation[decimal],
            sheet_name=None
        )
        self.generate_gui()


class NewProject(CTkToplevel):
    """Class representing New Project window."""

    def __init__(
            self,
            new_project: Callable[[str, CTkToplevel], None],
            *args,
            **kwargs
    ) -> None:
        """Constructor of NewProject class.

        Args:
            new_project (Callable[[str, CTkToplevel], None]): function
                to create a new project.
        """
        super().__init__(*args, **kwargs)
        self.title("New Project")
        self.new_project = new_project
        self.create_gui()

    def create_gui(self) -> None:
        """Create GUI."""
        label = CTkLabel(self, text="Insert project name")
        label.place(x=10, y=10)

        entry = CTkEntry(self)
        entry.place(x=10, y=45)

        add_button = CTkButton(
            self,
            text="Create Project",
            command=lambda: self.new_project(entry.get(), self)
        )
        add_button.place(x=10, y=80)


class SettingsTop(CTkToplevel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.settings_gui()

    def settings_gui(self) -> None:
        """Create GUI."""
        label = CTkLabel(self, text="Choose window mode")
        label.place(x=10, y=10)

        mode = CTkOptionMenu(
            self,
            values=["Dark", "Light"],
            command=self.change_mode

        )
        mode.place(x=10, y=35)

    def change_mode(self, new_mode: str) -> None:
        """Change the mode of the GUI."""
        set_appearance_mode(new_mode)
        SETTINGS["mode"] = new_mode
        update_settings(SETTINGS)
        