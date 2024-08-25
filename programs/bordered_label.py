import ttkbootstrap as ttk


class BorderedLabel(ttk.Frame):
    def __init__(self, master, border_width, textvariable, state="normal"):
        self.master = master
        self.border_width = border_width
        super().__init__(master, borderwidth=1, relief="solid")
        self.propagate(False)

        self.label = ttk.Label(self, textvariable=textvariable, state=state)
        self.label.pack(fill="x", anchor="center", padx=3)

        self.configure(width=self.label.winfo_reqwidth() + border_width)
        self.configure(height=self.label.winfo_reqheight())

    def update_width(self):
        self.configure(width=self.label.winfo_reqwidth() + self.border_width)
