"""Author Szymon Lasota"""
from pviev import ProjectWindow


class MainGUI:

    def __init__(self) -> None:
        """Initialize the main GUI"""
        self.window = ProjectWindow()

    def run(self) -> None:
        self.window.run()


def main() -> None:
    main_gui = MainGUI()
    main_gui.run()


if __name__ == "__main__":
    main()
