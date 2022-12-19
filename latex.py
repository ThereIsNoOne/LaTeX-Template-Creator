"""Author Szymon Lasota"""
import json
import os
from shutil import copyfile
from typing import Any, Dict

from settings import LatexFigure, Sections, settings_path


class TexFile:

    def __init__(
            self,
            path: str,
            title: str = "untitled.json",
    ) -> None:
        self.title = title
        self.folder_path = path
        self.path = path + "" + title
        self.text = self.setup()
        self.sections = [
            key for key in self.text.keys()
            if key != Sections.END
        ]

    def save(self) -> None:
        try:
            with open(self.path, "wt") as file:
                json.dump(self.text, file, indent=4)
        except FileNotFoundError:
            os.mkdir(self.folder_path)
            with open(self.path, "wt") as file:
                json.dump(self.text, file, indent=4)

    def add_section(self, section: str) -> None:
        self.sections.append(section)
        self.text[section] = ""

    def add_table(self) -> None:
        print("Adding")

    def add_pic(self, pic: str, name: str, section: str) -> None:
        copyfile(pic, self.folder_path + name)
        fig = LatexFigure(name)
        self.text[section] += fig.figure

    def setup(self) -> Dict[Any, str]:
        temp_1 = {}
        with open(settings_path + "/start.txt", "rt") as file:
            temp_1[Sections.PREAMBLE] = file.read()
        try:
            with open(self.path, "rt") as file:
                temp_2 = json.load(file)
        except FileNotFoundError as exc:
            temp_2 = {}
        if Sections.INTRO not in temp_2.keys():
            temp_1[Sections.INTRO] = "Some kind of text"
        output = {**temp_1, **temp_2, Sections.END: "\\end{document}"}
        return output

    def export(self, path: str) -> None:
        with open(self.path, "rt") as file:
            text_dict = json.load(file)

        text = ""
        for key in text_dict.keys():
            if key == Sections.PREAMBLE or key == Sections.END:
                text += text_dict[key]
                continue
            text += f"\\section{key}\n" + text_dict[key]
        with open(path, "wt") as file:
            file.write(text)
