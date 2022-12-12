"""Author Szymon Lasota"""
import sys

from customtkinter import CTk, CTkFrame, CTkTextbox

from settings import M_WIDTH, M_HEIGHT


class ProjectWindow(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{M_WIDTH}x{M_HEIGHT}")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.create_gui()

    def close(self) -> None:
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        frame = self.mainframe_setup()
        frame.place(x=M_WIDTH//3, y=0)

    def mainframe_setup(self):
        main_frame = CTkFrame(
            self,
            width=M_WIDTH//3,
            height=M_HEIGHT
        )

        entry = CTkTextbox(
            main_frame,
            width=M_WIDTH//3,
            height=M_HEIGHT
        )
        entry.place(x=0, y=0)

        return main_frame

    def run(self):
        self.mainloop()
