"""Author Szymon Lasota"""
import os

from customtkinter import CTkToplevel

from pmenu import ProjectMenu
from pviev import ProjectWindow
from settings import SETTINGS, Active, RUN, update_settings


class MainGUI:

    def __init__(self) -> None:
        """Initialize the main GUI"""
        if SETTINGS["current"] is not None:
            self.active = Active.WINDOW
            self.window = ProjectWindow(
                SETTINGS["current"][0],
                SETTINGS["current"][1],
                self.new_project,
                self.reboot
            )
        else:
            self.active = Active.MENU
            self.window = ProjectMenu(self.new_project, self.open)

    def new_project(self, path: str, top: CTkToplevel) -> None:
        if not path:
            return
        print("Ok")
        top.destroy()
        self.window.destroy()
        try:
            os.mkdir(f"UserData/{path}/")
        except FileExistsError:   # Control flow statement, I am fully
            pass      # aware it is consider as wrong practice
        SETTINGS["current"] = [f"UserData/{path}/", f"{path}.json"]
        SETTINGS["projects"][path] = [f"UserData/{path}/", f"{path}.json"]
        update_settings(SETTINGS)
        main()

    def reboot(self) -> None:
        self.window.destroy()
        main()

    def open(self, title: str) -> None:
        SETTINGS["current"] = [f"UserData/{title}/", f"{title}.json"]
        update_settings(SETTINGS)
        self.window.destroy()
        main()

    def run(self) -> None:
        """Run the active window."""
        if self.active == Active.MENU:
            self.window.run()
        if self.active == Active.WINDOW:
            self.window.run()


def main() -> None:
    """Main function, run when __name__ is __main__."""
    if RUN:
        main_gui = MainGUI()
        main_gui.run()


if __name__ == "__main__":
    main()
