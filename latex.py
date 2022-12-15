"""Author Szymon Lasota"""
from settings import settings_path


class TexFile:

    def __init__(
            self,
            text: str = "",
            title: str = "untitled.tex",
            path: str = None
    ) -> None:
        self.title = title
        if path is not None:
            self.path = path + "/" + self.title
        self.text = self.setup(text)

    def save(self) -> None:
        with open(self.path, "wt") as file:
            file.write(self.text)

    @staticmethod
    def setup(self, text: str) -> str:
        with open(settings_path+"start.txt", "rt") as file:
            output = file.read()
        output += "\n" + text + "\\end{document}"
        return output
