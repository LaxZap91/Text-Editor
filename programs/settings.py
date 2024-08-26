import ttkbootstrap as ttk


class SettingsMenu(ttk.Menu):
    def __init__(self, master):
        self.master = master
        super().__init__(master, tearoff=False)

        self.add_command(label="Back", command=self.master.goto_plain_text_editor)
