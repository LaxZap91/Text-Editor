import ttkbootstrap as ttk


class StatusBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        word_count_label = ttk.Label(self, textvariable=master.word_count)
        word_count_label.pack(side="left")
