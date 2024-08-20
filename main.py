import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from text import TextBox


class TextEditorApp(ttk.Window):
    def __init__(self):
        self.file_path = None

        super().__init__("Text Editor", size=(500, 500), minsize=(250, 100))

        self.create_menu_bar()
        self.create_text()

    def create_menu_bar(self):
        menu = ttk.Menu(self, tearoff=False)
        self.configure(menu=menu)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Open", command=self.open_command)
        file_menu.add_command(label="Save", command=self.save_command)
        file_menu.add_command(label="Save As", command=self.save_as_command)
        menu.add_cascade(label="File", menu=file_menu)

    def create_text(self):
        self.text = TextBox(self)
        self.text.pack(fill="both", expand=True)

    def open_command(self):
        file_path = askopenfilename(
            defaultextension=".txt", filetypes=[("Text documents (*.txt)", "*.txt")]
        )
        if file_path.strip() == "":
            return
        self.file_path = file_path

        with open(self.file_path, mode="r") as file:
            self.text.delete(1.0, "end")
            self.text.insert("end", file.read())

    def save_command(self):
        if self.file_path is not None:
            with open(self.file_path, "w") as file:
                file.write(self.text.get(1.0, "end"))
        else:
            self.save_as_command()

    def save_as_command(self):
        file_path = asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".txt",
            filetypes=[("Text documents (*.txt)", "*.txt")],
        )
        if file_path.strip() == "":
            return
        with open(file_path, mode="w") as file:
            file.write(self.text.get(1.0, "end"))


if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
