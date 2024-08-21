import ttkbootstrap as ttk
from tkinter.font import Font
from status_bar import StatusBar


class TextBox(ttk.Frame):
    def __init__(self, master):
        self.font = Font(family="Consolas", size=11)
        self.master = master

        self.scroll_needed = False

        super().__init__(master)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1, uniform=1)

        self.text = ttk.Text(
            self,
            undo=True,
            maxundo=-1,
            wrap="none",
            font=self.font,
            width=1,
            height=1,
        )
        self.text.pack(side="left", fill="both", expand=True)

        self.scroll_bar = ttk.Scrollbar(self)
        self.scroll_bar.pack(side="left", fill="y")
        self.scroll_bar.configure(command=self.scroll)
        self.text.configure(yscrollcommand=self.update_scroll)
        
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="both")

    def increment_zoom(self, size):
        self.font.configure(size=max(1, min(51, self.font.actual("size") + size)))

    def set_zoom(self, size):
        self.font.configure(size=max(1, min(51, int((size - 100) / 10 + 11))))

    def scroll(self, action, position, type=None):
        self.text.yview_moveto(position)

    def update_scroll(self, first, last, type=None):
        self.scroll_needed = float(first) > 0.0 or float(last) < 1.0
        self.change_scroll_bar_visibility()

        self.text.yview_moveto(first)
        self.scroll_bar.set(first, last)

    def change_scroll_bar_visibility(self):
        if self.scroll_needed:
            self.scroll_bar.pack(side="left", fill="y")
        else:
            self.scroll_bar.pack_forget()
