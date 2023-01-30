"""Author: Szymon Lasota, Aleksandra Supeł
Module contains test functions for the project.
Tests are written for `LatexTable` class.
"""
import pytest

from pandas import DataFrame
from texfigures import LatexTable


@pytest.fixture
def empty_dataframe() -> DataFrame:
    return DataFrame()


@pytest.fixture
def dataframe() -> DataFrame:
    return DataFrame(
        {
            "name": ["Szymon", "Aleksandra"],
            "last name": ["Lasota", "Supeł"]
        }
    )


def test_init_empty(empty_dataframe: DataFrame) -> None:
    table = LatexTable(empty_dataframe)
    assert (table.df.empty and table.rows_num == 0
            and table.cols_num == 0)


def test_init(dataframe: DataFrame) -> None:
    table = LatexTable(dataframe)
    print(dataframe.to_dict())
    assert (
        table.df.to_dict() == {
            "name": {0: "Szymon", 1: "Aleksandra"},
            "last name": {0: "Lasota", 1: "Supeł"}
        }
        and table.rows_num == 2 and table.cols_num == 2)


def test_write_empty(empty_dataframe: DataFrame) -> None:
    repr_ = LatexTable(empty_dataframe).write_tab()
    assert repr_ == "\\\\ \\hline\n"


def test_write(dataframe: DataFrame) -> None:
    repr_ = LatexTable(dataframe).write_tab()
    print(repr_)
    assert repr_ == (
        "\\multicolumn1{|l|}{name}&\\multicolumn1{|l|}{last name}\\\\ "
        + "\\hline\nSzymon&Lasota\\\\ \\hline\nAleksandra&Supeł\\\\ \\hline\n"
    )


def test_repr_empty(empty_dataframe: DataFrame) -> None:
    repr_ = LatexTable(empty_dataframe).tex_repr()
    assert repr_ == (
        "\n\\begin{table}[h!]\n"
        + "\\centering\n"
        + "\\caption{}\n"
        + "\\begin{tabular}{|" + "r|"*0 + "}\n"
        + "\\hline"
        + "\\\\ \\hline\n"
        + "\n\\end{tabular}\n"
        + "\\label{mylabel}\n"
        + "\\caption*{Gdzie}\n"
        + "\\end{table}"
    )


def test_repr(dataframe: DataFrame) -> None:
    repr_ = LatexTable(dataframe).tex_repr()
    assert repr_ == (
        "\n\\begin{table}[h!]\n"
        + "\\centering\n"
        + "\\caption{}\n"
        + "\\begin{tabular}{|" + "r|"*2 + "}\n"
        + "\\hline"
        + "\\multicolumn1{|l|}{name}&\\multicolumn1{|l|}{last name}\\\\ "
        + "\\hline\nSzymon&Lasota\\\\ \\hline\nAleksandra&Supeł\\\\ \\hline\n"
        + "\n\\end{tabular}\n"
        + "\\label{mylabel}\n"
        + "\\caption*{Gdzie}\n"
        + "\\end{table}"
    )
