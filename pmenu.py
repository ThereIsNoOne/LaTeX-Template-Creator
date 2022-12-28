"""Author Szymon Lasota"""
import sys
from typing import Callable
from shutil import rmtree

from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel, CTkToplevel

from settings import HEIGHT, SETTINGS, WIDTH, get_percent, update_settings
from toplevel import NewProject


class ProjectMenu(CTk):

    def __init__(
            self,
            new_project: Callable[[str, CTkToplevel], None],
            open_project: Callable[[str], None],
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.title("Project menu")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)
        self.projects = SETTINGS["projects"]
        self.prj_keys = list(self.projects.keys())
        self.start = 0
        self.new_project = new_project
        self.open_project = open_project
        self.create_gui()

    def close(self) -> None:
        update_settings(SETTINGS)
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        self.create_leftframe()
        self.create_main_frame()

    def create_leftframe(self) -> None:
        frame = CTkFrame(
            self,
            width=WIDTH//6,
            height=HEIGHT
        )
        frame.place(x=0, y=0)

        new_project_button = CTkButton(
            frame,
            text="New project",
            command=self.handle_new_project
        )
        new_project_button.place(x=10, y=10)

        next_button = CTkButton(
            frame,
            text="Next page",
            command=self.next
        )
        next_button.place(x=10, y=get_percent(HEIGHT, 14))

        previous_button = CTkButton(
            frame,
            text="Previous page",
            command=self.previous
        )
        previous_button.place(x=10, y=get_percent(HEIGHT, 19))

    def handle_new_project(self) -> None:
        NewProject(self.new_project)

    def create_main_frame(self) -> None:
        frame = CTkFrame(
            self,
            width=5*WIDTH//6,
            height=HEIGHT
        )
        frame.place(x=WIDTH//6, y=0)

        items = zip(
            range(len(self.prj_keys)), range(self.start, self.start + 10)
        )
        for num, i in items:
            try:
                key = self.prj_keys[i]
            except IndexError:
                break
            CTkLabel(frame, text=key, height=50).place(
                x=10, y=10+num*50
            )

            CTkButton(
                frame,
                text="Remove",
                command=lambda num=i: self.rm_project(
                    self.prj_keys[num]
                )
            ).place(x=3*WIDTH//6, y=10+num*50)

            CTkButton(
                frame,
                text="Open",
                command=lambda num=i: self.open_project(
                    self.prj_keys[num]
                )
            ).place(x=4*WIDTH//6, y=10+num*50)

    def rm_project(self, key: str) -> None:
        rmtree(SETTINGS["projects"][key][0])
        del SETTINGS["projects"][key]
        update_settings(SETTINGS)
        self.projects = SETTINGS["projects"]
        self.prj_keys = list(self.projects.keys())
        self.create_main_frame()

    def next(self) -> None:
        self.start += 10
        try:
            self.prj_keys[self.start]
        except IndexError:
            self.start = 0
        self.create_main_frame()

    def previous(self) -> None:
        self.start -= 10
        if self.start < 0:
            self.start = 0
        self.create_main_frame()

    def run(self) -> None:
        self.mainloop()
