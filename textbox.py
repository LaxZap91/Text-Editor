import ttkbootstrap as ttk
from tkinter.font import Font


class TextBox(ttk.Frame):
    def __init__(self, master):
        self.font = Font(family="Consolas", size=11)
        self.master = master

        self.first = 1
        self.last = 0
        
        super().__init__(master)
        
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1, uniform=1)

        # self.text_frame = ttk.Frame(self)
        self.text = ttk.Text(
            self,
            undo=True,
            maxundo=-1,
            wrap="none",
            font=self.font,
            width=1,
            height=1,
        )
        # self.text.grid(column=0, row=0, sticky='nsew')
        self.text.pack(side='left', fill='both', expand=True)
        
        # self.text_frame.grid(column=0, row=0, sticky='nsew')

        self.scroll_bar = ttk.Scrollbar(self)
        # self.scroll_bar.grid(column=1, row=0, sticky='nsw')
        self.scroll_bar.pack(side='left', fill='y')
        self.scroll_bar.configure(command=self.scroll)
        self.text.configure(yscrollcommand=self.update_scroll)
        

    def increment_zoom(self, size):
        self.font.configure(size=max(1, min(51, self.font.actual("size") + size)))

    def set_zoom(self, size):
        self.font.configure(size=max(1, min(51, int((size - 100) / 10 + 11))))
    
    def scroll(self, action, position, type=None):
        self.text.yview_moveto(position)
    
    def update_scroll(self, first, last, type=None):
        self.first = first
        self.last = last
        
        self.text.yview_moveto(first)
        self.scroll_bar.set(first, last)
    
    def is_scroll_needed(self):
        #print(float(self.first) > 0.0 or float(self.last) < 1.0)
        return float(self.first) > 0.0 or float(self.last) < 1.0
