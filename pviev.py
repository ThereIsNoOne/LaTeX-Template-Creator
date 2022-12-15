"""Author Szymon Lasota"""
import sys
from json import loads, dumps

from tkinter import Tk, Frame, Text, Menu, Toplevel, Button

from settings import M_WIDTH, M_HEIGHT


class ProjectWindow(Tk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{M_WIDTH}x{M_HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.create_gui()

    def close(self) -> None:
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        frame = self.mainframe_setup()
        frame.place(x=M_WIDTH//3, y=0)
        self.menu_setup()

    def mainframe_setup(self):
        main_frame = Frame(
            self,
            width=M_WIDTH//2,
            height=M_HEIGHT
        )

        entry = Text(
            main_frame,
            width=int(M_WIDTH // 3),
            height=M_HEIGHT
        )
        entry.place(x=0, y=0)

        return main_frame

    def menu_setup(self) -> None:
        menubar = Menu(self)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="New", command=self.new)
        file.add_command(label="Open", command=self.open)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Save as...", command=self.save_as)
        file.add_command(label="Export", command=self.export)
        menubar.add_cascade(label="File", menu=file)

        edit = Menu(menubar, tearoff=0)
        edit.add_command(label="Add table", command=self.add_table)
        edit.add_command(label="Add figure", command=self.add_pic)
        edit.add_command(label="Add section", command=self.add_section)
        menubar.add_cascade(label="Edit", menu=edit)

        self.config(menu=menubar)

    def new(self) -> None:
        print("new")

    def add_section(self) -> None:
        print("add Section")

    def add_table(self) -> None:
        print("Adding")

    def add_pic(self) -> None:
        print("Adding fig")

    def save_as(self) -> None:
        print("Save")

    def export(self) -> None:
        print("Export")

    def open(self) -> None:
        print("Open")

    def save(self) -> None:
        print("Save")

    def run(self):
        self.mainloop()
