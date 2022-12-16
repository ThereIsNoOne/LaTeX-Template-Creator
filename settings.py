"""Author Szymon Lasota"""
import os

WIDTH, HEIGHT = 1040, 720
M_WIDTH, M_HEIGHT = 1040, 720
settings_path = os.path.join("ProjectData")
user_path = os.path.join("UserData")


def get_percent(num: int, percent: float) -> int:
    return int(num * percent)


class Sections(str):
    PREAMBLE = "Preamble"
    INTRO = "Introduction"
    END = "End"
