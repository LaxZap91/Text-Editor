import ttkbootstrap as ttk


class StatusBar(ttk.Frame):
    def __init__(self, master):
        self.master = master
        
        super().__init__(master)

        word_count_label = ttk.Label(self, textvariable=master.word_count)
        word_count_label.pack(side="left")

        zoom_label = ttk.Label(self, textvariable=master.zoom_level)
        zoom_label.pack(side="left")

    def update_word_count(self):
        text = self.master.text.get(1.0, "end")
        self.master.word_count.set(f'{len(text)-sum(map(text.count, ('\n', '\t')))} characters')
    
    def update_zoom_percent(self):
        self.master.zoom_level.set(f"{(self.master.text.font.actual("size") - 11) * 10 + 100}%")
