"""Author Szymon Lasota"""
import json
import os
from shutil import copyfile
from typing import Any, Dict

from settings import Sections, settings_path
from texfigures import LatexFigure, LatexTable


class TexFile:
    """Class representing a Tex file"""
    def __init__(
            self,
            path: str,
            title: str = "untitled.json",
    ) -> None:
        """Constructor of TexFile class.

        Args:
            path (str): Path to the Tex file.
            title (str): Title of the Tex file.
        """
        self.title = title
        self.folder_path = path
        self.path = path + "" + title
        self.text = self.setup()
        self.sections = [
            key for key in self.text.keys()
            if key != Sections.END
        ]

    def save(self) -> None:
        """Save the Tex file to json."""
        try:
            with open(self.path, "wt") as file:
                json.dump(self.text, file, indent=4)
        except FileNotFoundError:
            os.mkdir(self.folder_path)
            with open(self.path, "wt") as file:
                json.dump(self.text, file, indent=4)

    def add_section(self, section: str) -> None:
        """Add section to TeX file.

        Args:
            section (str): Title of section.
        """
        self.sections.append(section)
        self.text[section] = ""

    def add_table(self) -> None:
        print("Adding")

    def add_pic(self, pic: str, name: str, section: str) -> None:
        """Add picture to TeX file.

        Args:
            pic (str): path to picture.
            name (str): name of picture.
            section (str): ): Title of destined section.
        """
        copyfile(pic, self.folder_path + name)
        fig = LatexFigure(name)
        self.text[section] += fig.figure

    def setup(self) -> Dict[Any, str]:
        """Setup of initial state of TeX file.

        Returns:
            Dict[Any, str]: Dictionary-style representation of TeX file.
        """
        temp_1 = {}
        with open(settings_path + "/start.txt", "rt") as file:
            temp_1[Sections.PREAMBLE] = file.read()
        try:
            with open(self.path, "rt") as file:
                temp_2 = json.load(file)
        except FileNotFoundError:
            temp_2 = {}
        if Sections.INTRO not in temp_2.keys():
            temp_1[Sections.INTRO] = "Some kind of text"
        output = {**temp_1, **temp_2, Sections.END: "\\end{document}"}
        return output

    def export(self, path: str) -> None:
        """Export TeX file to folder at given path.

        Args:
            path (str)): path to export
        """
        os.remove(path)
        os.mkdir(path)
        with open(self.path, "rt") as file:
            text_dict = json.load(file)

        text = ""
        for key in text_dict.keys():
            if key == Sections.PREAMBLE:
                text += text_dict[key]
                continue
            if key == Sections.END:
                continue
            text += f"\n\\section{{{key}}}\n" + text_dict[key]
        text += text_dict[Sections.END]
        with open(path+"/main.tex", "wt") as file:
            file.write(text)
