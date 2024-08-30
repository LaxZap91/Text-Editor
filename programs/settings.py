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

        self.font_family = ttk.StringVar(value="Consolas")
        self.families = sorted(
            set(
                font
                for font in font.families()
                if ("emoji" not in font.lower()) and (not font.startswith("@"))
            )
        )
        self.font_family_frame = ttk.Frame(self.text_formating_frame)
        self.font_family_label = ttk.Label(self.font_family_frame, text="Family")
        self.font_family_select = ttk.Combobox(
            self.font_family_frame, textvariable=self.font_family, values=self.families
        )
        self.font_family_frame.pack()
        self.font_family_label.pack(padx=20, pady=10, side="left")
        self.font_family_select.pack(padx=20, pady=10, side="right")

        self.font_weight = ttk.StringVar(value="Normal")
        self.font_weight_frame = ttk.Frame(self.text_formating_frame)
        self.font_weight_label = ttk.Label(self.font_weight_frame, text="Weight")
        self.font_weight_select = ttk.Combobox(
            self.font_weight_frame,
            textvariable=self.font_weight,
            values=("Normal", "Bold"),
        )
        self.font_weight_frame.pack()
        self.font_weight_label.pack(padx=20, pady=10, side="left")
        self.font_weight_select.pack(padx=20, pady=10, side="right")

        self.font_slant = ttk.StringVar(value="Roman")
        self.font_slant_frame = ttk.Frame(self.text_formating_frame)
        self.font_slant_label = ttk.Label(self.font_slant_frame, text="Slant")
        self.font_slant_select = ttk.Combobox(
            self.font_slant_frame,
            textvariable=self.font_slant,
            values=("Roman", "Italic"),
        )
        self.font_slant_frame.pack()
        self.font_slant_label.pack(padx=20, pady=10, side="left")
        self.font_slant_select.pack(padx=20, pady=10, side="right")

        self.font_size = ttk.IntVar(value=11)
        self.font_size_frame = ttk.Frame(self.text_formating_frame)
        self.font_size_label = ttk.Label(self.font_size_frame, text="Size")
        self.font_size_select = ttk.Spinbox(
            self.font_size_frame,
            textvariable=self.font_size,
            name="test",
            to=100,
            from_=1,
        )
        self.font_size_frame.pack()
        self.font_size_label.pack(padx=20, pady=10, side="left")
        self.font_size_select.pack(padx=20, pady=10, side="right")

    def create_frame_2(self):
        self.frame_2 = ttk.Frame(self)
        self.frame_2_label = ttk.Label(self.frame_2, text="Frame 2")
        self.frame_2_label.pack()
