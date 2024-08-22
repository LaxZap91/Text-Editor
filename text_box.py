import ttkbootstrap as ttk
from tkinter.font import Font
from status_bar import StatusBar


class TextBox(ttk.Frame):
    def __init__(self, master):
        self.master = master

        self.vscroll_needed = False
        self.hscroll_needed = False
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

        self.text_box_frame = ttk.Frame(self)

        self.font = Font(family="Consolas", size=11)
        self.text = ttk.Text(
            self.text_box_frame,
            undo=True,
            maxundo=-1,
            wrap="none",
            font=self.font,
            width=1,
            height=1,
        )
        self.text.pack(anchor="nw", fill="both", expand=True, side="left")

        self.vscroll_bar = ttk.Scrollbar(self.text_box_frame)
        self.vscroll_bar.pack(anchor="ne", fill="y", side="left")
        self.vscroll_bar.configure(command=self.vscroll)
        self.text.configure(yscrollcommand=self.update_vscroll)

        self.hscroll_bar = ttk.Scrollbar(self, orient="horizontal")
        self.hscroll_bar.pack(anchor="nw", fill="x", side="bottom")
        self.hscroll_bar.configure(command=self.hscroll)
        self.text.configure(xscrollcommand=self.update_hscroll)

        self.text_box_frame.pack(fill="both", side="top", expand=True)

    def increment_zoom(self, size):
        self.font.configure(size=max(1, min(51, self.font.actual("size") + size)))

    def set_zoom(self, size):
        self.font.configure(size=max(1, min(51, int((size - 100) / 10 + 11))))

    def vscroll(self, action, position, type=None):
        self.text.yview_moveto(position)

    def hscroll(self, action, position, type=None):
        self.text.xview_moveto(position)

    def update_vscroll(self, first, last, type=None):
        self.vscroll_needed = float(first) > 0.001 or float(last) < 1
        self.change_vscroll_bar_visibility()

        self.text.yview_moveto(first)
        self.vscroll_bar.set(first, last)

    def update_hscroll(self, first, last, type=None):
        self.hscroll_needed = float(first) > 0.001 or float(last) < 1.0
        self.change_hscroll_bar_visibility()

        self.text.xview_moveto(first)
        self.hscroll_bar.set(first, last)

    def change_vscroll_bar_visibility(self):
        if self.vscroll_needed:
            self.vscroll_bar.pack(anchor="ne", fill="y", side="left")
        else:
            self.vscroll_bar.pack_forget()

    def change_hscroll_bar_visibility(self):
        if self.hscroll_needed:
            self.hscroll_bar.pack(anchor="nw", fill="x", side="bottom")
        else:
            self.hscroll_bar.pack_forget()

    def change_status_bar_visibility(self):
        if self.status_bar_enabled.get():
            self.status_bar.pack_forget()

            self.status_bar.pack(fill="x", side="bottom")
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
