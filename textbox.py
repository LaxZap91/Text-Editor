from ttkbootstrap.scrolled import ScrolledText
from tkinter.font import Font


class TextBox(ScrolledText):
    def __init__(self, master):
        self.font = Font(family="Consolas", size=11)
        self.master = master

        super().__init__(
            master,
            undo=True,
            maxundo=-1,
            autohide=True,
            wrap="none",
            height=1,
            font=self.font,
        )

    def increment_zoom(self, size):
        self.font.configure(size=max(1, min(51, self.font.actual("size") + size)))

    def set_zoom(self, size):
        self.font.configure(size=max(1, min(51, int((size - 100) / 10 + 11))))
