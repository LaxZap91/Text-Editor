import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText




class TextBox(ScrolledText):
    def __init__(self, master):
        super().__init__(master)