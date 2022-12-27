"""Author Szymon Lasota"""
import sys

from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel

from settings import HEIGHT, SETTINGS, WIDTH, get_percent
from toplevel import SettingsHandling


class ProjectMenu(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)
        self.projects = SETTINGS["projects"]
        self.prj_keys = list(self.projects.keys())
        self.start = 0
        self.create_gui()

    def close(self) -> None:
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

        project_button = CTkButton(
            frame,
            text="Projects"
        )
        project_button.place(x=10, y=10)

        settings_button = CTkButton(
            frame,
            text="Settings",
            command=self.open_settings
        )
        settings_button.place(x=10, y=get_percent(HEIGHT, 7))

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
                text="Open",
                command=lambda num=i: self.open_project(
                    self.prj_keys[num]
                )
            ).place(x=4*WIDTH//6, y=10+num*50)

    def next(self) -> None:
        self.start += 10
        try:
            self.prj_keys[self.start]
        except IndexError:
            self.start = 0
        print(self.start)
        self.create_main_frame()

    def previous(self) -> None:
        self.start -= 10
        if self.start < 0:
            self.start = 0
        self.create_main_frame()

    def open_project(self, key) -> None:
        print(key)

    def open_settings(self) -> None:
        SettingsHandling()

    def run(self) -> None:
        self.mainloop()
