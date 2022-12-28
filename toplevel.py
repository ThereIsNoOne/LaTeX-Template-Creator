"""Author: Szymon Lasota"""
from tkinter import messagebox as msg
from typing import Callable

import pandas as pd
from customtkinter import (CTkButton, CTkEntry, CTkLabel, CTkOptionMenu,
                           CTkTextbox, CTkToplevel, StringVar)

from settings import (SETTINGS, TOP_HEIGHT, TOP_WIDTH, Mode, Separators,
                      update_settings)
from texfigures import LatexMath


class EnterMath(CTkToplevel):

    def __init__(
            self,
            mode: str,
            insert: Callable[[str, str], None],
            *args, **kwargs
    ) -> None:
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
        new_equation = textbox.textbox.get(1.0, "end-1c")
        if not new_equation or not name:
            return
        SETTINGS[self.mode][name] = new_equation
        update_settings(SETTINGS)
        self.destroy()


class EnterTable(CTkToplevel):

    def __init__(
            self,
            path: str,
            add_tab: Callable[[pd.DataFrame], None],
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.title = "Enter Table"
        self.path = path
        self.dfs = {}
        self.add_table = add_tab
        self.generate_gui()

    def generate_gui(self) -> None:
        label_sep = CTkLabel(self, text="Enter separator")
        label_sep.grid(row=0, column=0)

        label_del = CTkLabel(self, text="Enter delimiter")
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
        if self.path is None:
            msg.showerror(
                title="Wrong file path",
                message="You did not enter path to file!"
            )
        if self.path.endswith(".csv"):
            print(pd.read_csv(
                    self.path,
                    decimal=Separators.representation[decimal],
                    sep=Separators.representation[sep]
                ))
            self.dfs = {
                "sheet1": pd.read_csv(
                    self.path,
                    decimal=Separators.representation[decimal],
                    sep=Separators.representation[sep]
                )
            }
            self.generate_gui()
            return
        if not self.path.endswith("xlsx"):
            msg.showerror(
                title="Wrong file path",
                message="File should be .csv or .xlsx type!"
            )
        self.dfs = pd.read_excel(
            self.path,
            decimal=Separators.representation[decimal],
            sheet_name=None
        )
        print(self.dfs)
        self.generate_gui()


class SettingsHandling(CTkToplevel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.create_gui()

    def create_gui(self) -> None:
        label = CTkLabel(self, text="Settings")
        label.place(x=10, y=10)


class NewProject(CTkToplevel):

    def __init__(
            self,
            new_project: Callable[[str, CTkToplevel], None],
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.title("New Project")
        self.new_project = new_project
        self.create_gui()

    def create_gui(self) -> None:
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
