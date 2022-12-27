"""Author Szymon Lasota"""
from pviev import ProjectWindow
from pmenu import ProjectMenu
from settings import SETTINGS, Active


class MainGUI:

    def __init__(self) -> None:
        """Initialize the main GUI"""
        if SETTINGS["current"] is not None:
            self.active = Active.WINDOW
            self.window = ProjectWindow(
                SETTINGS["current"][0],
                SETTINGS["current"][1],
                self.new_project
            )
        else:
            self.active = Active.MENU
            self.menu = ProjectMenu()

    def new_project(self) -> None:
        ...

    def run(self) -> None:
        """Run the active window."""
        if self.active == Active.WINDOW:
            self.window.run()
        else:
            self.menu.run()


def main() -> None:
    """Main function, run when __name__ is __main__."""
    main_gui = MainGUI()
    main_gui.run()


if __name__ == "__main__":
    main()
