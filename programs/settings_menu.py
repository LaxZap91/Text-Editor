import ttkbootstrap as ttk


class SettingsMenu(ttk.Menu):
    def __init__(self, master):
        self.master = master
        super().__init__(master, tearoff=False)

        self.add_command(label="Back", command=self.master.goto_editor)
        self.add_command(label="Frame 1", command=self.place_setting_frame_1)
        self.add_command(label="Frame 2", command=self.place_setting_frame_2)

        self.create_setting_frames()

        self.current_frame = None

    def create_setting_frames(self):
        self.create_setting_frame_1()
        self.create_setting_frame_2()

    def create_setting_frame_1(self):
        self.frame_1 = ttk.Frame(self.master)
        self.label_1 = ttk.Label(self.frame_1, text="Frame 1")
        self.label_1.pack()

    def create_setting_frame_2(self):
        self.frame_2 = ttk.Frame(self.master)
        self.label_2 = ttk.Label(self.frame_2, text="Frame 2")
        self.label_2.pack()

    def place_setting_frame_1(self):
        if self.current_frame != self.frame_1:
            self.remove_current_frame()
            self.frame_1.pack()
            self.current_frame = self.frame_1

    def place_setting_frame_2(self):
        if self.current_frame != self.frame_2:
            self.remove_current_frame()
            self.frame_2.pack()
            self.current_frame = self.frame_2

    def remove_setting_frame_1(self):
        self.frame_1.pack_forget()

    def remove_setting_frame_2(self):
        self.frame_2.pack_forget()

    def remove_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
