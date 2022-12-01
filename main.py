from customtkinter import CTk, CTkButton, CTkLabel


class MainWindow(CTk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.create_gui()

    def create_gui(self) -> None:
        button = CTkButton(self, text="Close", command=self.destroy)
        button.pack()
        label = CTkLabel(self, text="Hello world!")
        label.pack()

    def run(self) -> None:
        self.mainloop()


window = MainWindow()
window.geometry("200x200")
window.mainloop()
