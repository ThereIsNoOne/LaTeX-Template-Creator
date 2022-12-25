"""Author: Szymon Lasota
Module contains classes that are used to create figures, tables and
math objects in TeX file.
"""
from typing import Dict

from settings import SETTINGS


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


class LatexMath:
    EQUATIONS: Dict[str, str] = SETTINGS["equations"]
    DISPLAYMATH: Dict[str, str] = SETTINGS["displaymath"]

    def write_equation(self, equation: str) -> str:
        equation_repr = str(
            "\n\\begin{equation}\n"
            + "\t\\label{mylabel}\n"
            + f"\t{self.EQUATIONS[equation]}"
            + "\\end{equation}"
        )
        return equation_repr

    def write_displaymath(self, displaymath: str) -> str:
        dspmath_repr = str(
            "\n\\begin{displaymath]\\n"
            + "\t\\begin{split}\n"
            + f"\t\t {self.DISPLAYMATH[displaymath]}\n"
            + "\t\\end{split}\n"
            + "\\end{displaymath}"
        )
        return dspmath_repr
