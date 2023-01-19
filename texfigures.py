"""Author: Szymon Lasota, Aleksandra Supeł
Module contains classes that are used to create figures, tables and
math objects in TeX file.
"""
from typing import Dict

import pandas as pd

from settings import SETTINGS


class LatexFigure:
    """Class representing a Latex figure."""

    def __init__(self, name: str) -> None:
        """Constructor of LatexFigure class.

        Args:
            name (str): Name of the Latex figure.
        """
        self.figure = str(
                "\n\\begin{figure}[h!]\n"
                + "\t\\centering\n"
                + f"\t\\includegraphics[width=.75\\textwidth]{{{name}}}\n"
                + "\t\\caption{caption}\n"
                + "\t\\label{mylabel}\n"
                + "\\end{figure}"
        )


class LatexTable:
    """Class representing a Latex table."""

    def __init__(self, df: pd.DataFrame) -> None:
        """Constructor of LatexTable class.

        Args:
            df (pd.DataFrame): Dataframe to be transformed into latex
                table.
        """
        self.df = df
        self.rows_num = df.shape[0]
        self.cols_num = df.shape[1]

    def tex_repr(self) -> str:
        """Generate TeX representation of table."""
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
        """Writes the data frame to the table."""
        repr = ""
        for col in self.df.columns:
            repr += f"\\multicolumn{1}{{|l|}}{{{col}}}"
            if col != self.df.columns[-1]:
                repr += "&"
        for i in range(self.rows_num):
            repr += "\\\\ \\hline\n"
            for j in range(self.cols_num):
                repr += f"{self.df.iloc[i, j]}"
                if j != self.cols_num - 1:
                    repr += "&"
        repr += "\\\\ \\hline\n"
        return repr


class LatexMath:
    """Class representing a Latex math object."""
    EQUATIONS: Dict[str, str] = SETTINGS["equations"]
    DISPLAYMATH: Dict[str, str] = SETTINGS["displaymath"]

    @classmethod
    def write_equation(cls, equation: str) -> str:
        """Write equation to tex file.

        Args:
            equation (str): equation to be written.

        Returns:
            str: tex equation.
        """
        equation_repr = str(
            "\n\\begin{equation}\n"
            + "\t\\label{mylabel}\n"
            + f"\t{cls.EQUATIONS[equation]}\n"
            + "\\end{equation}"
        )
        return equation_repr

    @classmethod
    def write_displaymath(cls, displaymath: str) -> str:
        """write multiline math to tex file.

        Args:
            displaymath (str): multiline math to be written.

        Returns:
            str: tex multiline math.
        """
        dspmath_repr = str(
            "\n\\begin{displaymath}\n"
            + "\t\\begin{split}\n"
            + f"\t\t {cls.DISPLAYMATH[displaymath]}\n"
            + "\t\\end{split}\n"
            + "\\end{displaymath}"
        )
        return dspmath_repr
