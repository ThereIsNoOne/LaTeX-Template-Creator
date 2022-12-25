"""Author Szymon Lasota"""
import os
import sys
from shutil import copyfile
from tkinter import Menu
from tkinter import filedialog as fd
from tkinter import messagebox as msg
from typing import Callable

from customtkinter import (END, INSERT, CTk, CTkButton, CTkEntry, CTkFrame,
                           CTkLabel, CTkOptionMenu, CTkTextbox, CTkToplevel,
                           StringVar)

from latex import TexFile
from settings import (M_HEIGHT, M_WIDTH, SETTINGS, Sections, get_percent,
                      update_settings)


class ProjectWindow(CTk):
    """Main project window."""
    def __init__(
            self,
            path_project: str,
            title: str,
            new_project: Callable[[], None],
            *args,
            **kwargs
    ) -> None:
        """Constructor of main project window.

        Args:
            path_project (str): path to temporary project files.
            title (str): title of the project.
            new_project (Callable): Method creates new project window.
            *args ():
            **kwargs ():
        """
        super().__init__(*args, **kwargs)
        self.entry = Sections.INTRO
        self.project_path = path_project
        self.new_project = new_project
        self.active_section = Sections.PREAMBLE
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
            width=M_WIDTH//2,
            height=M_HEIGHT
        )

        self.entry = CTkTextbox(
            main_frame,
            width=int(M_WIDTH // 2),
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
        file.add_command(label="Open", command=self.open)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Save as...", command=self.save_as)
        file.add_command(label="Export", command=self.export)
        menubar.add_cascade(label="File", menu=file)

        add = Menu(menubar, tearoff=0,  bg="#4e4e4e", fg="#ffffff")
        add.add_command(
            label="Add table", command=self.add_table
        )
        add.add_command(
            label="Add figure", command=self.add_pic
        )
        add.add_command(
            label="Add section", command=self.add_section
        )

        submenu = Menu(add, tearoff=0)
        submenu.add_command(
            label="Add math",
            command=self.add_math
        )
        submenu.add_command(
            label="Add equation",
            command=self.add_equation
        )
        add.add_cascade(
            label="Math",
            menu=submenu
        )
        menubar.add_cascade(label="Edit", menu=add)

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

        combo_box = CTkOptionMenu(
            frame,
            values=self.tex_file.sections,
            width=M_WIDTH//3 - M_WIDTH//30,
        )
        combo_box.place(x=M_WIDTH//60, y=25)

        button = CTkButton(
            frame,
            text="Switch",
            command=lambda: self.switch(combo_box.get())
        )
        button.place(
            x=get_percent(M_WIDTH//3, 0.10),
            y=get_percent(M_HEIGHT, 0.90)
        )
        add_pic_button = CTkButton(
            frame,
            text="Add picture",
            command=self.add_pic
        )
        add_pic_button.place(
            x=get_percent(M_WIDTH//3, 0.10),
            y=get_percent(M_HEIGHT, 0.85)
        )
        add_table_button = CTkButton(
            frame,
            text="Add table",
            command=self.add_table
        )
        add_table_button.place(
            x=get_percent(M_WIDTH//3, 0.10),
            y=get_percent(M_HEIGHT, 0.80)
        )

        return frame

    def save(self) -> None:
        """Save the file."""
        self.tex_file.text[self.active_section] =\
            self.entry.textbox.get(1.0, "end-1c")
        self.tex_file.save()

    def switch(self, section: str) -> None:
        """Switch between sections."""
        self.save()
        self.active_section = section
        self.entry.textbox.delete(1.0, END)
        self.entry.insert(INSERT, self.tex_file.text[section])
        print(f"switch {section}")

    def new(self) -> None:
        """Create new project."""
        self.save()
        self.new_project()

    def add_pic(self) -> None:
        """Add picture to current section."""

        path = fd.askopenfilename(
            title="Open file",
        )
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
        self.entry.textbox.delete(1.0, END)
        self.entry.insert(
            INSERT, self.tex_file.text[self.active_section]
        )
        self.save()

    def add_section(self) -> None:
        """Get information about a new section of the project."""
        top = CTkToplevel(self)
        # top.geometry(f"{TOP_WIDTH}x{TOP_HEIGHT}")
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
        self.tex_file.add_section(section)
        self.save()
        top.destroy()
        self.create_gui()

    def add_table(self) -> None:
        print("add_table")

    def add_math(self) -> None:
        print("add_math")

    def add_equation(self) -> None:
        print("add_equation")

    def save_as(self) -> None:
        """Method responsible for 'save as...' button."""
        top = CTkToplevel(self)
        # top.geometry(f"{TOP_WIDTH}x{TOP_HEIGHT}")
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
        os.rename(
            self.project_path + f"/{self.tex_file.title}",
            self.project_path + new_name + ".json"
        )
        os.rename(
            self.project_path,
            self.project_path[:self.project_path.find("/")+1] + new_name
            + "/"
        )
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
        SETTINGS["current"] = self.project_path
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

    def open(self) -> None:
        print("Open")

    def run(self) -> None:
        """Run the project window."""
        self.mainloop()
