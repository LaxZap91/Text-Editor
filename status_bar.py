import ttkbootstrap as ttk


class StatusBar(ttk.Frame):
    def __init__(self, master, window):
        self.master = master
        self.window = window
        
        super().__init__(master)
        
        self.word_count = ttk.StringVar(value="0 characters")
        self.zoom_level = ttk.StringVar(value="100%")
        self.is_saved = ttk.StringVar(value="Saved: False")
        self.path_to_file = ttk.StringVar(value="Path: None")
        
        self.file_path_enabled = ttk.BooleanVar(value=True)

        self.word_count_label = ttk.Label(self, textvariable=self.word_count)
        self.word_count_label.grid(row=0, column=0, sticky='nsew')

        self.zoom_label = ttk.Label(self, textvariable=self.zoom_level)
        self.zoom_label.grid(row=0, column=1, sticky='nsew')

        self.is_saved_label = ttk.Label(self, textvariable=self.is_saved)
        self.is_saved_label.grid(row=0, column=2, sticky='nsew')
        
        self.file_path_label = ttk.Label(self, textvariable=self.path_to_file)
        self.file_path_label.grid(row=0, column=3, sticky='nsew')

    def update_word_count(self):
        text = self.master.get_text()
        self.word_count.set(f'{len(text)-sum(map(text.count, ('\n', '\t')))} characters')
    
    def update_zoom_percent(self):
        self.zoom_level.set(f"{(self.master.font.actual("size") - 11) * 10 + 100}%")
    
    def update_is_saved(self):
        self.is_saved.set(f"Saved: {'True' if self.master.is_not_modified() else 'False'}")
    
    def update_file_path(self):
        self.path_to_file.set(f"Path: {self.window.file_path}")
    
    def change_file_path_visiblilty(self):
        if self.file_path_enabled.get():
            self.file_path_label.grid(row=0, column=3, sticky='nsew')
        else:
            self.file_path_label.grid_forget()
