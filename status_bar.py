import ttkbootstrap as ttk


class StatusBar(ttk.Frame):
    def __init__(self, master, window):
        self.master = master
        self.window = window
        
        super().__init__(master)

        word_count_label = ttk.Label(self, textvariable=master.word_count)
        word_count_label.grid(row=0, column=0, sticky='nsew')

        zoom_label = ttk.Label(self, textvariable=master.zoom_level)
        zoom_label.grid(row=0, column=1, sticky='nsew')

        is_saved_label = ttk.Label(self, textvariable=master.is_saved)
        is_saved_label.grid(row=0, column=2, sticky='nsew')

    def update_word_count(self):
        text = self.master.get_text()
        self.master.word_count.set(f'{len(text)-sum(map(text.count, ('\n', '\t')))} characters')
    
    def update_zoom_percent(self):
        self.master.zoom_level.set(f"{(self.master.font.actual("size") - 11) * 10 + 100}%")
    
    def update_is_saved(self):
        self.master.is_saved.set(f"Saved: {'True' if self.master.is_not_modified() else 'False'}")
        
