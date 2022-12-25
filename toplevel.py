"""Author: Szymon Lasota"""
from typing import Callable

from customtkinter import (CTkButton, CTkEntry, CTkOptionMenu, CTkTextbox,
                           CTkToplevel)

from settings import TOP_HEIGHT, TOP_WIDTH
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
        if mode == "equations":
            self.options = list(LatexMath.EQUATIONS.keys())
        elif mode == "displalymath":
            self.options = list(LatexMath.DISPLAYMATH.keys())
        else:
            raise ValueError("Invalid mode")

    def generate_gui(self) -> None:
        label = "Chose what to insert:"

        combobox = CTkOptionMenu(
            self,
            self.options
        )

        text = CTkTextbox(
            self,
            width=TOP_WIDTH,
            height=TOP_HEIGHT
        )

        insert_button = CTkButton(
            self,
            text=f"Insert {self.mode}",
            command=lambda: self.insert(combobox.get())
        )

        add_button = CTkButton(
            self,
            text=f"Add new {self.mode}",
            command=lambda: self.add_new(text)
        )

    def add_new(self, textbox: CTkTextbox) -> None:
        ...
