import ttkbootstrap as ttk


class Settings(ttk.Notebook):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.create_frames()
        self.add_frames()

    def create_frames(self):
        self.create_frame_1()
        self.create_frame_2()

    def add_frames(self):
        self.add(self.frame_1, text="Frame 1")
        self.add(self.frame_2, text="Frame 2")

    def create_frame_1(self):
        self.frame_1 = ttk.Frame(self)
        self.frame_1_label = ttk.Label(self.frame_1, text="Frame 1")
        self.frame_1_label.pack()

    def create_frame_2(self):
        self.frame_2 = ttk.Frame(self)
        self.frame_2_label = ttk.Label(self.frame_2, text="Frame 2")
        self.frame_2_label.pack()
