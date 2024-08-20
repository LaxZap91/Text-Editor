from ttkbootstrap.scrolled import ScrolledText
import random

class TextBox(ScrolledText):
    def __init__(self, master):
        super().__init__(master, undo=True, maxundo=-1, autohide=True, wrap='none', height=1)
        self.master = master
    
    def update_word_count(self):
        text = self.get(1.0, 'end')
        self.master.word_count.set(f'{len(text)-sum(map(text.count, ('\n', '\t')))} characters')
