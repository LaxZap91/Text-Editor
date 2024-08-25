import ttkbootstrap as ttk
from bordered_label import BorderedLabel


class StatusBar(ttk.Frame):
    def __init__(self, master, window):
        self.master = master
        self.window = window

        super().__init__(master)

        self.word_count = ttk.StringVar(value="0 characters")
        self.zoom_level = ttk.StringVar(value="100%")
        self.is_saved = ttk.StringVar(value="Saved: False")
        self.path_to_file = ttk.StringVar(value="Path: None")

        self.file_path_enabled = ttk.BooleanVar(value=False)

        self.create_wigits()
        self.pack_wigits()

    def create_wigits(self):
        self.word_count_label = BorderedLabel(
            self,
            30,
            textvariable=self.word_count,
            state="disabled",
        )
        self.zoom_label = BorderedLabel(
            self,
            30,
            textvariable=self.zoom_level,
            state="disabled",
        )
        self.is_saved_label = BorderedLabel(
            self,
            30,
            textvariable=self.is_saved,
            state="disabled",
        )
        self.file_path_label = BorderedLabel(
            self,
            30,
            textvariable=self.path_to_file,
            state="disabled",
        )

    def pack_wigits(self):
        self.word_count_label.grid(row=0, column=0, sticky="nsew")
        self.zoom_label.grid(row=0, column=1, sticky="nsew")
        self.is_saved_label.grid(row=0, column=2, sticky="nsew")

    def update_word_count(self):
        text = self.master.get_text()
        self.word_count.set(
            f'{len(text)-sum(map(text.count, ('\n', '\t')))} characters'
        )
        self.word_count_label.update_width()

    def update_zoom_percent(self):
        self.zoom_level.set(f"{(self.master.font.actual("size") - 11) * 10 + 100}%")

    def update_is_saved(self):
        self.is_saved.set(
            f"Saved: {'True' if self.master.is_not_modified() else 'False'}"
        )
        self.is_saved_label.update_width()

    def update_file_path(self):
        self.path_to_file.set(f"Path: {self.window.file_path}")
        self.file_path_label.update_width()

    def change_file_path_visiblilty(self):
        if self.file_path_enabled.get():
            self.file_path_label.grid(row=0, column=3, sticky="nsew")
        else:
            self.file_path_label.grid_forget()
