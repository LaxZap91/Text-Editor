import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ttkbootstrap.dialogs import MessageDialog
from text_box import TextBox
from menu_bar import MenuBar


class TextEditorApp(ttk.Window):
    def __init__(self):

        self.file_path = None

        super().__init__(
            "Text Editor",
            size=(500, 500),
            minsize=(250, 100),
            iconphoto="icon/icon.png",
        )

        self.create_textbox()
        self.create_menu_bar()
        self.create_keybinds()

        self.update_clock()

    def create_menu_bar(self):
        self.menu = MenuBar(self)
        self.configure(menu=self.menu)

    def create_textbox(self):
        self.textbox = TextBox(self)
        self.textbox.pack(fill="both", expand=True)

    def open_command(self):
        file_path = askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text documents (*.txt)", "*.txt"),
                ("Markdown documents (*.md)", "*.md"),
                ("All files (*)", "*"),
            ],
        )
        if file_path.strip() == "":
            return
        self.file_path = file_path

        with open(self.file_path, mode="r") as file:
            self.textbox.clear_text()
            self.textbox.text.insert("end", file.read())
        self.textbox.status_bar.update_word_count()
        self.textbox.saved_state = self.textbox.get_text()

    def save_command(self):
        if self.file_path is not None:
            with open(self.file_path, "w") as file:
                file.write(self.textbox.get_text())
            self.textbox.saved_state = self.textbox.get_text()
        else:
            self.save_as_command()

    def save_as_command(self):
        file_path = asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".txt",
            filetypes=[
                ("Text documents (*.txt)", "*.txt"),
                ("Markdown documents (*.md)", "*.md"),
                ("All files (*)", "*"),
            ],
            initialfile=self.textbox.get_text().split("\n")[0],
        )
        if file_path.strip() == "":
            return
        with open(file_path, mode="w") as file:
            file.write(self.textbox.get_text())
        self.textbox.saved_state = self.textbox.get_text()

    def create_keybinds(self):
        self.bind_all("<Control-o>", lambda _: self.open_command())
        self.bind_all("<Control-s>", lambda _: self.save_command())
        self.bind_all("<Control-Shift-S>", lambda _: self.save_as_command())
        self.bind_all("<Control-=>", lambda _: self.textbox.increment_zoom(1))
        self.bind_all("<Control-minus>", lambda _: self.textbox.increment_zoom(-1))
        self.bind_all("<Control-0>", lambda _: self.textbox.set_zoom(100))
        self.bind_all("<Control-z>", lambda _: self.textbox.undo_text())
        self.bind_all("<Control-Shift-Z>", lambda _: self.textbox.redo_text())

        self.protocol("WM_DELETE_WINDOW", self.display_check_save)

    def update_clock(self):
        self.textbox.status_bar.update_word_count()
        self.textbox.status_bar.update_zoom_percent()
        self.textbox.status_bar.update_is_saved()
        self.after(10, self.update_clock)

    def display_check_save(self):
        if not self.textbox.is_not_modified():
            msg_box = MessageDialog(
                "Do you want to save changes?",
                buttons=["Save:primary", "Don't save", "Cancel"],
                default="Save",
            )
            msg_box.show()
            result = msg_box.result
            if result == "Save":
                self.save_command()
            elif result == "Cancel":
                return
        self.destroy()


if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
