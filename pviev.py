"""Author Szymon Lasota"""
import sys
from tkinter import Menu

from customtkinter import (
    CTk,
    CTkTextbox,
    CTkFrame,
    CTkOptionMenu,
    StringVar,
    CTkToplevel,
    CTkLabel,
    CTkEntry,
    CTkButton,
    INSERT,
    END,
)


from settings import M_WIDTH, M_HEIGHT, get_percent, Sections
from latex import TexFile


class ProjectWindow(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.combo_box = None
        self.entry = Sections.INTRO
        self.active_section = None
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

        self.entry = CTkTextbox(
            main_frame,
            width=int(M_WIDTH // 2),
            height=M_HEIGHT
        )
        self.entry.place(x=0, y=0)

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
        edit.add_command(
            label="Add table", command=self.add_table
        )
        edit.add_command(
            label="Add figure", command=self.add_pic
        )
        edit.add_command(
            label="Add section", command=self.add_section
        )
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

        button = CTkButton(
            frame,
            text="Switch",
            command=lambda: self.switch(combo_box.get())
        )
        button.place(
            x=get_percent(M_WIDTH//3, 0.10),
            y=get_percent(M_HEIGHT, 0.90)
        )

        return frame

    def save(self) -> None:
        self.tex_file.text[self.active_section] =\
            self.entry.textbox.get(1.0, END)
        self.tex_file.save()

    def switch(self, section: str) -> None:
        self.save()
        self.active_section = section
        self.entry.textbox.delete(1.0, END)
        self.entry.insert(INSERT, self.tex_file.text[section])
        print(f"switch {section}")

    def new(self) -> None:
        print("new")

    def add_pic(self) -> None:
        print("add_pic")

    def add_section(self) -> None:
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
        self.tex_file.add_section(section)
        self.save()
        top.destroy()
        self.create_gui()

    def add_table(self) -> None:
        print("add_table")

    def save_as(self) -> None:
        self.tex_file.save()

    def export(self) -> None:
        print("Export")

    def open(self) -> None:
        print("Open")

    def run(self):
        self.mainloop()
