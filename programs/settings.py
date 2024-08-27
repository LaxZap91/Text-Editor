import ttkbootstrap as ttk
from ttkbootstrap import font


class Settings(ttk.Notebook):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.create_frames()
        self.add_frames()

    def create_frames(self):
        self.create_text_formating_frame()
        self.create_frame_2()

    def add_frames(self):
        self.add(self.text_formating_frame, text="Text Formating")
        self.add(self.frame_2, text="Frame 2")

    def create_text_formating_frame(self):
        self.text_formating_frame = ttk.Frame(self)
        self.font_family_select = ttk.Combobox(
            self.text_formating_frame,
            textvariable=self.master.font_family,
            values=font.families(),
        )
        self.font_style_select = ttk.Combobox(
            self.text_formating_frame,
            textvariable=self.master.font_style,
            values=("Normal", "Bold", "Italic", "Bold Italic"),
        )

        self.font_family_select.pack()
        self.font_style_select.pack()

    def create_frame_2(self):
        self.frame_2 = ttk.Frame(self)
        self.frame_2_label = ttk.Label(self.frame_2, text="Frame 2")
        self.frame_2_label.pack()
