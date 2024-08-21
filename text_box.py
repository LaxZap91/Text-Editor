import ttkbootstrap as ttk
from tkinter.font import Font
from status_bar import StatusBar


class TextBox(ttk.Frame):
    def __init__(self, master):
        self.master = master

        self.scroll_needed = False
        self.saved_state = "\n"

        super().__init__(master)

        self.word_count = ttk.StringVar(value="0 characters")
        self.zoom_level = ttk.StringVar(value="100%")
        self.is_saved = ttk.StringVar(value="Saved: False")
        self.status_bar_enabled = ttk.BooleanVar(value=True)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1, uniform=1)
        
        self.status_bar = StatusBar(self, master)
        self.status_bar.pack(fill="x", side="bottom")

        self.font = Font(family="Consolas", size=11)
        self.text = ttk.Text(
            self,
            undo=True,
            maxundo=-1,
            wrap="none",
            font=self.font,
            width=1,
            height=1,
        )
        self.text.pack(anchor="nw", fill="both", expand=True, side="left")

        self.scroll_bar = ttk.Scrollbar(self)
        self.scroll_bar.pack(anchor="ne", fill="y", side="left")
        self.scroll_bar.configure(command=self.scroll)
        self.text.configure(yscrollcommand=self.update_scroll)


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
            self.scroll_bar.pack(anchor="ne", fill="y", side="left")
        else:
            self.scroll_bar.pack_forget()

    def change_status_bar_visibility(self):
        if self.status_bar_enabled.get():
            self.status_bar.pack_forget()
            self.text.pack_forget()
            self.scroll_bar.pack_forget()
            
            
            self.status_bar.pack(fill="x", side="bottom")
            self.text.pack(anchor="nw", fill="both", expand=True, side="left")
            self.scroll_bar.pack(anchor="ne", fill="y", side="left")
        else:
            self.status_bar.pack_forget()

    def get_text(self):
        return self.text.get(1.0, "end")

    def clear_text(self):
        self.text.delete(1.0, "end")

    def is_not_modified(self):
        return self.saved_state == self.get_text()

    def undo_text(self):
        try:
            self.text.edit_undo()
        except Exception:
            pass

    def redo_text(self):
        try:
            self.text.edit_redo()
        except Exception:
            pass
