"""Author Szymon Lasota"""
from pviev import ProjectWindow
from pmenu import ProjectMenu
from settings import SETTINGS


class MainGUI:

    def __init__(self) -> None:
        """Initialize the main GUI"""
        self.window = ProjectWindow(
            SETTINGS["current"][0],
            SETTINGS["current"][1],
            self.new_project
        )
        # self.menu = ProjectMenu()

    def new_project(self) -> None:
        ...

    def run(self) -> None:
        self.window.run()


def main() -> None:
    main_gui = MainGUI()
    main_gui.run()


if __name__ == "__main__":
    main()
