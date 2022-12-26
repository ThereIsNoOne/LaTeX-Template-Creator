"""Author: Szymon Lasota
Module contains classes that are used to create figures, tables and
math objects in TeX file.
"""
from typing import Dict

import pandas as pd

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

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def tex_repr(self) -> str:
        ...


class LatexMath:
    EQUATIONS: Dict[str, str] = SETTINGS["equations"]
    DISPLAYMATH: Dict[str, str] = SETTINGS["displaymath"]

    @classmethod
    def write_equation(cls, equation: str) -> str:
        equation_repr = str(
            "\n\\begin{equation}\n"
            + "\t\\label{mylabel}\n"
            + f"\t{cls.EQUATIONS[equation]}\n"
            + "\\end{equation}"
        )
        return equation_repr

    @classmethod
    def write_displaymath(cls, displaymath: str) -> str:
        dspmath_repr = str(
            "\n\\begin{displaymath]\n"
            + "\t\\begin{split}\n"
            + f"\t\t {cls.DISPLAYMATH[displaymath]}\n"
            + "\t\\end{split}\n"
            + "\\end{displaymath}"
        )
        return dspmath_repr
