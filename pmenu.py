"""Author Szymon Lasota"""
import sys

from customtkinter import CTkFrame, CTk, CTkButton
from settings import WIDTH, HEIGHT, get_percent


class ProjectMenu(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.resizable(False, False)
        self.create_gui()

    def close(self) -> None:
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        self.create_leftframe()

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
            text="Settings"
        )

    def run(self) -> None:
        self.mainloop()
