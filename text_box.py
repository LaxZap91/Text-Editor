import ttkbootstrap as ttk
from tkinter.font import Font
from status_bar import StatusBar
from math import log10


class TextBox(ttk.Frame):
    def __init__(self, master):
        self.master = master

        self.vscroll_needed = False
        self.hscroll_needed = False
        self.saved_state = "\n"

        super().__init__(master)

        self.status_bar_enabled = ttk.BooleanVar(value=True)
        self.line_numbers_enabled = ttk.BooleanVar(value=True)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1, uniform=1)

        self.font = Font(family="Consolas", size=11)

        self.create_wigits()
        self.pack_wigits()
        self.configure_wigits()

    def create_wigits(self):
        self.text = ttk.Text(
            self,
            undo=True,
            maxundo=-1,
            wrap="none",
            font=self.font,
            width=1,
            height=1,
        )
        self.line_numbers = ttk.Text(
            self,
            wrap="none",
            font=self.font,
            width=2,
            height=1,
            state="disabled",
        )
        self.vscroll_bar = ttk.Scrollbar(self)
        self.hscroll_bar = ttk.Scrollbar(self, orient="horizontal")

        self.status_bar = StatusBar(self, self.master)

    def pack_wigits(self):
        self.status_bar.pack(
            anchor="sw", fill="x", side="bottom"  # , before=self.line_numbers
        )
        self.line_numbers.pack(
            anchor="nw",
            fill="both",
            side="left",
            after=self.status_bar,
            # before=self.vscroll_bar,
        )
        self.vscroll_bar.pack(
            anchor="ne",
            fill="y",
            side="right",
            after=self.line_numbers,
            # before=self.hscroll_bar,
        )
        self.hscroll_bar.pack(
            anchor="sw",
            fill="x",
            side="bottom",
            after=self.vscroll_bar,
            # before=self.text,
        )
        self.text.pack(
            anchor="ne", fill="both", expand=True, side="top", after=self.hscroll_bar
        )

    def configure_wigits(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.insert("end", "1")
        self.line_numbers.configure(state="disabled")
        self.line_numbers.tag_add("line", 1.0, "end")
        self.line_numbers.tag_configure("line", justify="right")

        self.vscroll_bar.configure(command=self.vscroll)
        self.text.configure(yscrollcommand=self.update_vscroll)
        self.line_numbers.configure(yscrollcommand=self.update_vscroll)

        self.hscroll_bar.configure(command=self.hscroll)
        self.text.configure(xscrollcommand=self.update_hscroll)

    def increment_zoom(self, size):
        self.font.configure(size=max(1, min(51, self.font.actual("size") + size)))

    def set_zoom(self, size):
        self.font.configure(size=max(1, min(51, int((size - 100) / 10 + 11))))

    def vscroll(self, action, position, type=None):
        self.text.yview_moveto(position)
        self.line_numbers.yview_moveto(position)

    def hscroll(self, action, position, type=None):
        self.text.xview_moveto(position)

    def update_vscroll(self, first, last, type=None):
        self.vscroll_needed = float(first) > 0.001 or float(last) < 1.0
        self.change_vscroll_bar_visibility()

        self.text.yview_moveto(first)
        self.line_numbers.yview_moveto(first)
        self.vscroll_bar.set(first, last)

    def update_hscroll(self, first, last, type=None):
        self.hscroll_needed = float(first) > 0.001 or float(last) < 1.0
        self.change_hscroll_bar_visibility()

        self.text.xview_moveto(first)
        self.hscroll_bar.set(first, last)

    def change_vscroll_bar_visibility(self):
        if self.vscroll_needed:
            self.vscroll_bar.pack(
                anchor="ne",
                fill="y",
                side="right",
                # after=self.line_numbers,
                before=self.text,
            )
            if self.hscroll_needed:
                print("pack box")
        else:
            self.vscroll_bar.pack_forget()
            print("pack_forget box")

    def change_hscroll_bar_visibility(self):
        if self.hscroll_needed:
            self.hscroll_bar.pack(
                anchor="sw",
                fill="x",
                side="bottom",
                # after=self.vscroll_bar,
                before=self.text,
            )
            if self.vscroll_needed:
                print("pack box")
        else:
            self.hscroll_bar.pack_forget()
            print("pack_forget box")

    def change_status_bar_visibility(self):
        if self.status_bar_enabled.get():
            self.status_bar.pack(
                anchor="sw", fill="x", side="bottom", before=self.hscroll_bar
            )
            self.line_numbers.pack_configure(after=self.status_bar)
        else:
            self.status_bar.pack_forget()

    def change_line_numbers_visibility(self):
        if self.line_numbers_enabled.get():
            self.line_numbers.pack(
                anchor="nw",
                fill="both",
                side="left",
                after=self.status_bar,
                # before=self.vscroll_bar,
            )
        else:
            self.line_numbers.pack_forget()

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

    def get_line_number(self):
        return int(self.text.index("end-1c").split(".")[0])

    def get_line_number_digits(self):
        return int(log10(self.get_line_number())) + 1

    def set_line_number(self):
        self.line_numbers.configure(
            state="normal", width=self.get_line_number_digits() + 1
        )
        self.line_numbers.delete(1.0, "end")
        self.line_numbers.insert(
            "end", "\n".join(map(str, range(1, self.get_line_number() + 1)))
        )
        self.line_numbers.tag_add("line", 1.0, "end")
        self.line_numbers.configure(state="disabled")
