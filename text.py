from ttkbootstrap.scrolled import ScrolledText


class TextBox(ScrolledText):
    def __init__(self, master):
        super().__init__(master, undo=True, maxundo=-1, autohide=True, wrap='none')