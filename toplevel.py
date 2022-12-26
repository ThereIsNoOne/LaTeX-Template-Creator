"""Author: Szymon Lasota"""
from typing import Callable

from customtkinter import (CTkButton, CTkEntry, CTkLabel, CTkOptionMenu,
                           CTkTextbox, CTkToplevel, StringVar)

from settings import SETTINGS, TOP_HEIGHT, TOP_WIDTH, Mode, update_settings
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
