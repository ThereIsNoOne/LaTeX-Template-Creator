"""Author Szymon Lasota"""
import sys

from tkinter import Tk, Button, Label

from settings import WIDTH, HEIGHT


class ProjectMenu(Tk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.create_gui()

    def close(self) -> None:
        self.destroy()
        sys.exit()

    def create_gui(self) -> None:
        button = Button(self, text="Close", command=self.destroy)
        button.pack()
        label = Label(self, text="Hello world!")
        label.pack()

    def run(self) -> None:
        self.mainloop()
