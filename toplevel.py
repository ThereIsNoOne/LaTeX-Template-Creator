"""Author: Szymon Lasota"""
from typing import Callable

from customtkinter import (CTkButton, CTkEntry, CTkOptionMenu, CTkTextbox,
                           CTkToplevel, CTkLabel)

from settings import TOP_HEIGHT, TOP_WIDTH, Modes
from texfigures import LatexMath


class EnterMath(CTkToplevel):

    def __init__(
            self,
            mode: str,
            insert: Callable[[str], None],
            *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.title = f"Enter {mode}"
        self.insert = insert
        if mode == Modes.EQUATION:
            self.options = list(LatexMath.EQUATIONS.keys())
        elif mode == Modes.DISPLAYMATH:
            self.options = list(LatexMath.DISPLAYMATH.keys())
        else:
            raise ValueError("Invalid mode")
        self.generate_gui()

    def generate_gui(self) -> None:
        label = CTkLabel(text="Chose what to insert:")
        label.grid(row=0, column=0, columnspan=3)

        combobox = CTkOptionMenu(
            self,
            values=self.options,
            width=TOP_WIDTH
        )
        combobox.grid(row=1, column=0, columnspan=2)

        text = CTkTextbox(
            self,
            width=TOP_WIDTH,
            height=TOP_HEIGHT
        )
        text.grid(row=2, column=0, columnspan=2, rowspan=2)

        insert_button = CTkButton(
            self,
            text=f"Insert {self.mode}",
            command=lambda: self.insert(combobox.get())
        )
        insert_button.grid(row=2, column=2)

        add_button = CTkButton(
            self,
            text=f"Add new {self.mode}",
            command=lambda: self.add_new(text)
        )
        add_button.grid(row=3, column=2)

    def add_new(self, textbox: CTkTextbox) -> None:
        ...
