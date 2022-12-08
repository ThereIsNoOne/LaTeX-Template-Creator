from customtkinter import CTk, CTkButton, CTkLabel

from settings import WIDTH, HEIGHT


class ProjectMenu(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.create_gui()

    def create_gui(self) -> None:
        button = CTkButton(self, text="Close", command=self.destroy)
        button.pack()
        label = CTkLabel(self, text="Hello world!")
        label.pack()

    def run(self) -> None:
        self.mainloop()


window = ProjectMenu()
