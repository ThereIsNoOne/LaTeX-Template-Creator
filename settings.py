"""Author Szymon Lasota"""
import json
import os
from json import load

WIDTH, HEIGHT = 1040, 720
M_WIDTH, M_HEIGHT = 1040, 720
TOP_WIDTH, TOP_HEIGHT = 300, 150
settings_path = os.path.join("ProjectData")
user_path = os.path.join("UserData")
settings_path_json = os.path.join("ProjectData", "SETTINGS.json")

with open(settings_path_json, "rt") as file:
    SETTINGS = load(file)


def update_settings(settings):
    with open(settings_path_json, "wt") as file:
        json.dump(settings, file, indent=4)


def get_percent(num: int, percent: float) -> int:
    return int(num * percent)


class Sections(str):
    PREAMBLE = "Preamble"
    INTRO = "Introduction"
    END = "End"


class LatexFigure:

    def __init__(self, name: str) -> None:
        self.figure = str(
                "\n\\begin{figure}[h!]\n"
                + "\t\\centering\n"
                + f"\t\\includegraphics[width=.75\\textwidth]{{{name}}}\n"
                + "\t\\caption{caption}\n"
                + "\t\\label{mylabel}\n"
                + "\\end{figure}"
        )


class LatexTable:
    ...
