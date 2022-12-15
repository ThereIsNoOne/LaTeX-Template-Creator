"""Author Szymon Lasota"""
import sys
from tkinter import Menu

from customtkinter import (
    CTk,
    CTkTextbox,
    CTkFrame,
    CTkOptionMenu,
    StringVar
)

from settings import M_WIDTH, M_HEIGHT, get_percent
from latex import TexFile


class ProjectWindow(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{M_WIDTH}x{M_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tex_file = TexFile()
        self.create_gui()

    def close(self) -> None:
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        main_frame = self.mainframe_setup()
        main_frame.place(x=M_WIDTH//3, y=0)
        left_frame = self.left_frame_setup()
        left_frame.place(x=0, y=0)
        self.menu_setup()

    def mainframe_setup(self) -> CTkFrame:
        main_frame = CTkFrame(
            self,
            width=M_WIDTH//2,
            height=M_HEIGHT
        )

        entry = CTkTextbox(
            main_frame,
            width=int(M_WIDTH // 2),
            height=M_HEIGHT
        )
        entry.place(x=0, y=0)

        return main_frame

    def menu_setup(self) -> None:
        menubar = Menu(self, background="#000000")
        file = Menu(menubar, tearoff=0, bg="#4e4e4e", fg="#ffffff")
        file.add_command(label="New", command=self.new)
        file.add_command(label="Open", command=self.open)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Save as...", command=self.save_as)
        file.add_command(label="Export", command=self.export)
        menubar.add_cascade(label="File", menu=file)

        edit = Menu(menubar, tearoff=0,  bg="#4e4e4e", fg="#ffffff")
        edit.add_command(label="Add table", command=self.add_table)
        edit.add_command(label="Add figure", command=self.add_pic)
        edit.add_command(label="Add section", command=self.add_section)
        menubar.add_cascade(label="Edit", menu=edit)

        self.config(menu=menubar)

    def left_frame_setup(self) -> CTkFrame:

        frame = CTkFrame(
            self,
            width=M_WIDTH//3,
            height=M_HEIGHT
        )

        current = StringVar(self)
        current.set("Choose")

        combo_box = CTkOptionMenu(
            frame,
            values=self.tex_file.sections,
            width=M_WIDTH//3 - M_WIDTH//30,
        )
        combo_box.place(x=M_WIDTH//60, y=25)

        return frame

    def new(self) -> None:
        print("new")

    def add_section(self) -> None:
        print("add Section")

    def add_table(self) -> None:
        print("Adding")

    def add_pic(self) -> None:
        print("Adding fig")

    def save_as(self) -> None:
        self.tex_file.save()

    def export(self) -> None:
        print("Export")

    def open(self) -> None:
        print("Open")

    def save(self) -> None:
        self.tex_file.save()

    def run(self):
        self.mainloop()
