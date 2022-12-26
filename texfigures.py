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
        self.rows_num = df.shape[0]
        self.cols_num = df.shape[1]

    def tex_repr(self) -> str:
        repr = (
            "\n\\begin{table}[h!]\n"
            + "\\centering\n"
            + "\\caption{}\n"
            + "\\begin{tabular}{|" + "r|"*self.cols_num + "}\n"
            + "\\hline"
        )
        repr += self.write_tab()
        repr += (
            "\n\\end{tabular}\n"
            + "\\label{mylabel}\n"
            + "\\caption*{Gdzie}\n"
            + "\\end{table}"
        )
        return repr

    def write_tab(self) -> str:
        repr = ""
        for col in self.df.columns:
            repr += f"\\multicolumn{1}{{|l|}}{{{col}}}"
        repr += "\\\\ \\hline\n"
        for i in range(self.rows_num):
            repr += "\\\\ \\hline\n"
            for j in range(self.cols_num):
                repr += f"{self.df.iloc[i, j]}"
                if j != self.cols_num - 1:
                    repr += "&"
        return repr


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
