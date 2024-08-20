import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename
from text import TextBox


class TextEditorApp(ttk.Window):
    def __init__(self):
        self.file_path = None

        super().__init__("Text Editor", size=(500, 500))

        self.create_menu_bar()

    def create_menu_bar(self):
        menu = ttk.Menu(self, tearoff=False)
        self.configure(menu=menu)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Save", command=self.save_command)
        file_menu.add_command(label="Load", command=self.load_command)
        menu.add_cascade(label="File", menu=file_menu)

    def create_text(self):
        self.text = TextBox(self)
        self.text.pack(fill="both")

    def load_command(self):
        new_file_path = askopenfilename(filetypes=[("Text files", '.txt')])
        if new_file_path.strip() == "":
            return
        self.file_path = new_file_path

        with open(self.file_path, mode='r') as file:
            self.text.delete(1.0, "end")
            self.text.insert("end", file.read())
    
    def save_command(self):
        if self.file_path is not None:    
            with open(self.file_path, 'w') as file:
                file.write(self.text.get(1.0, 'end'))


if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
