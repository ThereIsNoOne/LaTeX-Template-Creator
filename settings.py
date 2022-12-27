"""Author Szymon Lasota

Settings file, contains:

- All the constants,
- Settings imported form ``.json`` file,
"""
from enum import Enum, auto
import json
import os
from json import load

settings_path = os.path.join("ProjectData")
user_path = os.path.join("UserData")
settings_path_json = os.path.join("ProjectData", "SETTINGS.json")

with open(settings_path_json, "rt") as file:
    SETTINGS = load(file)

WIDTH, HEIGHT = (SETTINGS["window"]["width"], SETTINGS["window"]["height"])
M_WIDTH, M_HEIGHT = (
    SETTINGS["window"]["main_width"],
    SETTINGS["window"]["main_height"]
)
TOP_WIDTH, TOP_HEIGHT = (
    SETTINGS["window"]["top_width"],
    SETTINGS["window"]["top_height"]
)


def update_settings(settings):
    """Update the settings."""
    with open(settings_path_json, "wt") as file_:
        json.dump(settings, file_, indent=4)


def get_percent(num: int, percent: float) -> int:
    """Get the percentage of value."""
    return int(num * percent/100)


class Sections(str):
    PREAMBLE = "Preamble"
    INTRO = "Introduction"
    END = "End"


class Mode(str):
    DISPLAYMATH = "displaymath"
    EQUATION = "equations"


class Separators:
    SEPARATORS = ["Coma", "Dot", "Tabulator", "Semicolon"]
    DECIMAL = ["Dot", "Coma"]
    representation = {
        "Dot": ".",
        "Coma": ",",
        "Tabulator": "\t",
        "Semicolon": ";"
    }


class Active(Enum):
    WINDOW = auto()
    MENU = auto()
