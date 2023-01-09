"""Author Szymon Lasota
This module contains the project window class, which is main window. It
allows user to write and edit LaTeX-style documents easily. It provides
option to add figures in `.jpeg`, `.pdf` and `.png` files, import tables
directly from `.csv` or `.xlsx` files. Users can provide it with their
own math equations (save them for later and then reuse it). There is
easy access to all sections including the preamble which contains
predefined packages.
"""

import os
import platform
import subprocess
import sys
from shutil import copyfile
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter import messagebox as msg
from typing import Callable

import pandas as pd
from customtkinter import (END, INSERT, CTk, CTkButton, CTkEntry, CTkFrame,
                           CTkLabel, CTkOptionMenu, CTkTextbox, CTkToplevel,
                           StringVar)

from latex import TexFile
from settings import (M_HEIGHT, M_WIDTH, SETTINGS, Mode, Sections, get_percent,
                      help_file, update_settings)
from texfigures import LatexMath, LatexTable
from toplevel import EnterMath, EnterTable, NewProject, SettingsTop


class ProjectWindow(CTk):
    """Main project window."""
    def __init__(
            self,
            path_project: str,
            title: str,
            new_project: Callable[[str, CTkToplevel], None],
            reboot: Callable[[], None],
            *args,
            **kwargs
    ) -> None:
        """Constructor of main project window.

        Args:
            path_project (str): path to temporary project files.
            title (str): title of the project.
            new_project (Callable): Method creates new project window.
            *args
            **kwargs
        """
        super().__init__(*args, **kwargs)
        self.entry = Sections.INTRO
        self.project_path = path_project
        self.new_project = new_project
        self.reboot = reboot
        self.active_section = Sections.PREAMBLE
        self.title("Project Window")
        self.geometry(f"{M_WIDTH}x{M_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tex_file = TexFile(path=path_project, title=title)
        self.create_gui()

    def close(self) -> None:
        """Method for closing the window."""
        self.save()
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        """Method for creating a new window."""
        left_frame = self.left_frame_setup()
        left_frame.place(x=0, y=0)
        main_frame = self.mainframe_setup()
        main_frame.place(x=M_WIDTH//3, y=0)
        self.menu_setup()

    def mainframe_setup(self) -> CTkFrame:
        """Create main_frame for project window.

        Returns:
            CTkFrame: Main frame for project window.
        """
        main_frame = CTkFrame(
            self,
            width=M_WIDTH//3 * 2,
            height=M_HEIGHT
        )

        self.entry = CTkTextbox(
            main_frame,
            width=int(M_WIDTH//3 * 2),
            height=M_HEIGHT,
        )
        self.entry.place(x=0, y=0)
        self.entry.insert(
            INSERT, self.tex_file.text[self.active_section]
        )
        return main_frame

    def menu_setup(self) -> None:
        """Set up the menubar for project window."""
        menubar = Menu(self, background="#000000")

        file = Menu(menubar, tearoff=0, bg="#4e4e4e", fg="#ffffff")
        file.add_command(label="New", command=self.new)
        file.add_command(label="Close project", command=self.close_project)
        file.add_command(label="Settings", command=self.settings)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Save as...", command=self.save_as)
        file.add_command(label="Export", command=self.export)
        menubar.add_cascade(label="File", menu=file)

        edit = Menu(menubar, tearoff=0,  bg="#4e4e4e", fg="#ffffff")
        edit.add_command(
            label="Add table", command=self.get_table_file
        )
        edit.add_command(
            label="Add figure", command=self.add_pic
        )
        edit.add_command(
            label="Add section", command=self.add_section
        )
        edit.add_command(
            label="Remove current section", command=self.remove_section
        )

        submenu = Menu(edit, tearoff=0,  bg="#4e4e4e", fg="#ffffff")
        submenu.add_command(
            label="Add math",
            command=self.add_math
        )
        submenu.add_command(
            label="Add equation",
            command=self.add_equation
        )
        edit.add_cascade(
            label="Math",
            menu=submenu
        )
        menubar.add_cascade(label="Edit", menu=edit)

        help_ = Menu(menubar, tearoff=0,  bg="#4e4e4e", fg="#ffffff")
        help_.add_command(label="Instruction", command=self.instruction)
        menubar.add_cascade(label="Help", menu=help_)

        self.config(menu=menubar)

    def left_frame_setup(self) -> CTkFrame:
        """Left frame setup, left frame contains action buttons and
            section selection combobox.

        Returns:
            CTkFrame: left frame for the project window.
        """

        frame = CTkFrame(
            self,
            width=M_WIDTH//3,
            height=M_HEIGHT
        )

        variable = StringVar(self, self.tex_file.sections[0])

        combo_box = CTkOptionMenu(
            frame,
            values=self.tex_file.sections,
            variable=variable,
            width=M_WIDTH//3 - M_WIDTH//30,
        )
        combo_box.place(x=M_WIDTH//60, y=25)

        button = CTkButton(
            frame,
            text="Switch",
            command=lambda: self.switch(combo_box.get())
        )
        button.place(
            x=get_percent(M_WIDTH//3, 10),
            y=get_percent(M_HEIGHT, 90)
        )
        add_pic_button = CTkButton(
            frame,
            text="Add picture",
            command=self.add_pic
        )
        add_pic_button.place(
            x=get_percent(M_WIDTH//3, 10),
            y=get_percent(M_HEIGHT, 85)
        )
        add_table_button = CTkButton(
            frame,
            text="Add table",
            command=self.get_table_file
        )
        add_table_button.place(
            x=get_percent(M_WIDTH//3, 10),
            y=get_percent(M_HEIGHT, 80)
        )

        return frame

    def settings(self) -> None:
        """Open the settings."""
        SettingsTop()

    def remove_section(self) -> None:
        """Remove section from the project."""
        del self.tex_file.text[self.active_section]
        self.tex_file.sections.remove(self.active_section)
        self.active_section = self.tex_file.sections[0]
        try:
            self.entry.textbox.delete(1.0, END)
        except AttributeError:
            self.entry.delete(1.0, END)
        self.entry.insert(INSERT, self.tex_file.text[self.active_section])
        self.save()
        self.create_gui()

    @staticmethod
    def instruction() -> None:
        """Shows instruction."""
        if platform.system() == 'Darwin':
            subprocess.call(('open', help_file))
        elif platform.system() == 'Windows':
            os.startfile(help_file)
        else:
            subprocess.call(('xdg-open', help_file))

    def save(self) -> None:
        """Save the file."""
        try:
            self.tex_file.text[self.active_section] =\
                self.entry.textbox.get(1.0, "end-1c")
        except AttributeError:
            self.tex_file.text[self.active_section] =\
                self.entry.get(1.0, "end-1c")
        self.tex_file.save()

    def switch(self, section: str) -> None:
        """Switch between sections."""
        self.save()
        self.active_section = section
        try:
            self.entry.textbox.delete(1.0, END)
        except AttributeError:
            self.entry.delete(1.0, END)
        self.entry.insert(INSERT, self.tex_file.text[section])

    def new(self) -> None:
        """Create new project."""
        self.save()
        NewProject(self.new_project)

    def add_pic(self) -> None:
        """Add picture to current section."""

        path = fd.askopenfilename(
            title="Open file",
        )

        if path is None:
            return
        if not (
            path.lower().endswith(".jpg")
            or path.lower().endswith(".pdf")
            or path.lower().endswith(".png")
        ):
            msg.showerror(
                title="Wrong file extension",
                message="Your file must be .pdf, .png, .jpg"
            )
            return

        name = ""
        for char in path[::-1]:
            if char == "/":
                break
            name += char
        self.tex_file.add_pic(path, name[::-1], self.active_section)
        try:
            self.entry.textbox.delete(1.0, END)
        except AttributeError:
            self.entry.delete(1.0, END)
        self.entry.insert(
            INSERT, self.tex_file.text[self.active_section]
        )
        self.save()

    def add_section(self) -> None:
        """Get information about a new section of the project."""
        top = CTkToplevel(self)
        top.title("Add section")
        label = CTkLabel(top, text="Insert section name:")
        entry = CTkEntry(top)
        button = CTkButton(
            top,
            text="Ok",
            command=lambda: self.process_section_add(entry.get(), top)
        )
        label.grid(row=0, column=0, columnspan=2)
        entry.grid(row=1, column=0, columnspan=2)
        button.grid(row=2, column=1)

    def process_section_add(
            self,
            section: str,
            top: CTkToplevel
    ) -> None:
        """Add a section to the project.

        Args:
            section (str): The name of the section.
            top (CTkToplevel): Window responsible for getting inf of
                section.
        """
        if not section:
            msg.showerror(
                title="No section name",
                message="You must enter a section name."

            )
            return
        if section in self.tex_file.sections:
            msg.showerror(
                title="Name error",
                message="Name already used."

            )
            return
        self.tex_file.add_section(section)
        self.save()
        top.destroy()
        self.create_gui()

    def get_table_file(self) -> None:
        path = fd.askopenfilename(
            title="Open file",
            filetypes=[
                ("Data files", ["*.csv", ".xlsx"]),
            ]
        )
        if path is None:
            return
        EnterTable(path, self.add_table)

    def add_table(self, df: pd.DataFrame) -> None:
        """Add the table to the project.

        Args:
            df (pd.DataFrame): Dataframe to be converted into tex table.
        """
        self.save()
        tab = LatexTable(df)
        self.tex_file.text[self.active_section] += tab.tex_repr()
        try:
            self.entry.textbox.delete(1.0, END)
        except AttributeError:
            self.entry.delete(1.0, END)
        self.entry.insert(
            INSERT, self.tex_file.text[self.active_section]
        )
        self.save()

    def add_math(self) -> None:
        """Add math to project."""
        EnterMath(Mode.DISPLAYMATH, self.insert_text, self)

    def add_equation(self) -> None:
        """Add equation to project"""
        EnterMath(Mode.EQUATION, self.insert_text, self)

    def insert_text(self, math_object: str, flag: str) -> None:
        """Insert math or equation to project."""
        self.save()
        if flag == Mode.DISPLAYMATH:
            self.tex_file.text[self.active_section] +=\
                 LatexMath.write_displaymath(math_object)
        elif flag == Mode.EQUATION:
            self.tex_file.text[self.active_section] +=\
                LatexMath.write_equation(math_object)
        try:
            self.entry.textbox.delete(1.0, END)
        except AttributeError:
            self.entry.delete(1.0, END)
        self.entry.insert(
            INSERT, self.tex_file.text[self.active_section]
        )
        self.save()

    def save_as(self) -> None:
        """Method responsible for 'save as...' button."""
        top = CTkToplevel(self)
        top.title("New name")
        label = CTkLabel(top, text="Insert new project name:")
        entry = CTkEntry(top)
        button = CTkButton(
            top,
            text="Ok",
            command=lambda: self.process_new_name(entry.get(), top)
        )
        label.grid(row=0, column=0, columnspan=2)
        entry.grid(row=1, column=0, columnspan=2)
        button.grid(row=2, column=1)

    def process_new_name(self, new_name: str, top: CTkToplevel) -> None:
        """Method responsible for changing the name of the project."""
        if not new_name:
            msg.showerror(
                title="Fatal Error",
                message="New project name must not be empty."
            )
            return
        if new_name in SETTINGS["projects"].keys():
            msg.showerror(
                title="Fatal Error",
                message="New project name already exists."
            )
            return
        os.rename(
            self.project_path + f"/{self.tex_file.title}",
            self.project_path + new_name + ".json"
        )
        os.rename(
            self.project_path,
            self.project_path[:self.project_path.find("/")+1] + new_name
            + "/"
        )
        SETTINGS["projects"][new_name] = []
        SETTINGS["projects"][new_name].extend([
            self.project_path[:self.project_path.find("/") + 1] + new_name
            + "/",
            new_name + ".json"
        ])
        del SETTINGS["projects"][self.tex_file.title[:-5]]
        self.tex_file.title = new_name + ".json"
        self.tex_file.folder_path = (
                self.project_path[:self.project_path.find("/") + 1] + new_name
                + "/"
        )
        self.tex_file.path = (
            self.project_path[:self.project_path.find("/") + 1] + new_name
            + "/"
            + self.tex_file.title
        )
        self.project_path = (
            self.project_path[:self.project_path.find("/") + 1] + new_name
            + "/"
        )
        SETTINGS["current"] = [self.project_path, new_name + ".json"]
        update_settings(SETTINGS)
        top.destroy()
        self.tex_file.save()

    def export(self) -> None:
        """Export project to directory, prepare it for compilation."""
        try:
            path = fd.asksaveasfile(
                    filetypes=[("All files", "*.*")],
                ).name
        except AttributeError:
            print("Cancelled")
            return
        self.tex_file.export(path)
        self.pack_figs(path)

    def pack_figs(self, path: str) -> None:
        """Pack all picture files to **compilation** folder.

        Args:
            path (str): path to **compilation** folder.
        """
        for main_path, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".json"):
                    continue
                copyfile(main_path + file, path + "/" + file.split("/")[-1])

    def close_project(self) -> None:
        """Close project and open main menu."""
        SETTINGS["current"] = None
        update_settings(SETTINGS)
        self.reboot()

    def run(self) -> None:
        """Run the project window."""
        self.mainloop()
