"""Author Szymon Lasota"""
import json
from typing import Dict, Any

from customtkinter import CTkToplevel

from settings import settings_path, Sections, user_path


class TexFile:

    def __init__(
            self,
            title: str = "untitled.json",
            path: str = None,
    ) -> None:
        self.title = title
        if path is not None:
            self.path = f"{path}/{self.title}"
        else:
            self.path = f"{user_path}/{self.title}"
        self.text = self.setup()
        self.sections = [
            key for key in self.text.keys()
            if key != Sections.PREAMBLE and key != Sections.END
        ]

    def save(self) -> None:
        with open(self.path, "wt") as file:
            json.dump(self.text, file)

    def add_section(self, section: str) -> None:
        self.sections.append(section)
        self.text[section] = ""

    def add_table(self) -> None:
        print("Adding")

    def add_pic(self) -> None:
        print("Adding fig")

    @staticmethod
    def setup() -> Dict[Any, str]:
        output = {}
        with open(settings_path+"/start.txt", "rt") as file:
            output[Sections.PREAMBLE] = file.read()
        output["Introduction"] = "Some kind of text"
        output[Sections.END] = "\\end{document}"
        return output
