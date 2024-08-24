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
        self.current_line_numbers = 1

        super().__init__(master)

        self.status_bar_enabled = ttk.BooleanVar(value=True)
        self.line_numbers_enabled = ttk.BooleanVar(value=True)
        self.no_tabs = ttk.BooleanVar(value=False)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1, uniform=1)

        self.font = Font(family="Consolas", size=11)

        self.create_wigits()
        self.configure_wigits()
        self.pack_wigits()

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
        self.status_bar.pack(anchor="sw", fill="x", side="bottom")
        self.line_numbers.pack(
            anchor="nw",
            fill="both",
            side="left",
            after=self.status_bar,
        )
        self.vscroll_bar.pack(
            anchor="ne",
            fill="y",
            side="right",
            after=self.line_numbers,
        )
        self.hscroll_bar.pack(
            anchor="sw",
            fill="x",
            side="bottom",
            after=self.vscroll_bar,
        )
        self.text.pack(
            anchor="ne", fill="both", expand=True, side="top", after=self.hscroll_bar
        )

    def configure_wigits(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.insert("end", "1")
        self.line_numbers.configure(state="disabled")
        self.line_numbers.tag_add("line", "1.0", "end")
        self.line_numbers.tag_configure("line", justify="right")

        self.vscroll_bar.configure(command=self.vscroll)
        self.text.configure(yscrollcommand=self.update_vscroll)
        self.line_numbers.configure(yscrollcommand=self.update_vscroll)

        self.hscroll_bar.configure(command=self.hscroll)
        self.text.configure(xscrollcommand=self.update_hscroll)

        self.text.bindtags((".!textbox.!text", "Text", "post-text", ".", "all"))
        self.text.bind_class(
            "post-text", "<KeyPress>", lambda _: self.update_line_numbers(), add="+"
        )
        self.text.bind_class(
            "post-text", "<KeyRelease>", lambda _: self.update_line_numbers(), add="+"
        )
        self.text.bind_class(
            "post-text", "<Control-v>", lambda _: self.update_line_numbers(), add="+"
        )

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
            if self.hscroll_needed:
                self.vscroll_bar.pack(
                    anchor="ne",
                    fill="y",
                    side="right",
                    before=self.text,
                    pady=0,
                )
                self.hscroll_bar.pack_configure(padx=(0, 11))
            else:
                self.vscroll_bar.pack(
                    anchor="ne",
                    fill="y",
                    side="right",
                    before=self.text,
                    pady=0,
                )
        else:
            self.vscroll_bar.pack_forget()

    def change_hscroll_bar_visibility(self):
        if self.hscroll_needed:
            if self.vscroll_needed:
                self.hscroll_bar.pack(
                    anchor="sw",
                    fill="x",
                    side="bottom",
                    before=self.text,
                    padx=0,
                )
                self.vscroll_bar.pack_configure(pady=(0, 11))
            else:
                self.hscroll_bar.pack(
                    anchor="sw",
                    fill="x",
                    side="bottom",
                    before=self.text,
                    padx=0,
                )
            if self.line_numbers_enabled.get():
                self.line_numbers.pack_configure(pady=(0, 11))
        else:
            self.hscroll_bar.pack_forget()
            if self.line_numbers_enabled.get():
                self.line_numbers.pack_configure(pady=0)

    def change_status_bar_visibility(self):
        if self.status_bar_enabled.get():
            if self.hscroll_needed:
                self.status_bar.pack(
                    anchor="sw", fill="x", side="bottom", before=self.hscroll_bar
                )
            else:
                self.status_bar.pack(
                    anchor="sw", fill="x", side="bottom", before=self.text
                )
        else:
            self.status_bar.pack_forget()

    def change_line_numbers_visibility(self):
        if self.line_numbers_enabled.get():
            if self.status_bar_enabled.get():
                self.line_numbers.pack(
                    anchor="nw",
                    fill="both",
                    side="left",
                    after=self.status_bar,
                )
            else:
                self.line_numbers.pack(
                    anchor="nw",
                    fill="both",
                    side="left",
                    before=self.text,
                )
        else:
            self.line_numbers.pack_configure(pady=0)
            self.line_numbers.pack_forget()

    def get_text(self):
        return self.text.get("1.0", "end")

    def clear_text(self):
        self.text.delete("1.0", "end")

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
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert(
            "end", "\n".join(map(str, range(1, self.get_line_number() + 1)))
        )
        self.line_numbers.tag_add("line", "1.0", "end")
        self.line_numbers.configure(state="disabled")

    def update_line_numbers(self):
        self.line_numbers.configure(
            state="normal", width=self.get_line_number_digits() + 1
        )

        new_line_numbers = self.get_line_number()
        difference = new_line_numbers - self.current_line_numbers
        if difference == 1:
            self.line_numbers.insert(
                "end",
                f"\n{new_line_numbers}",
            )
        elif difference > 1:
            self.line_numbers.insert(
                "end",
                f"\n{"\n".join(map(str, range(self.current_line_numbers, new_line_numbers)))}",
            )
        elif difference < 0:
            self.line_numbers.delete(float(new_line_numbers + 1), "end")

        self.line_numbers.tag_add("line", "1.0", "end")
        self.line_numbers.configure(state="disabled")
        self.current_line_numbers = self.get_line_number()

    def change_tab_to_space(self):
        if self.no_tabs.get():
            self.text.bind("<Tab>", lambda _: self.tab_to_space())
        else:
            self.text.unbind("<Tab>")

    def tab_to_space(self):
        self.text.insert("insert", "    ")
        return "break"
