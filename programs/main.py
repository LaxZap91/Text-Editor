import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ttkbootstrap.dialogs import MessageDialog
from text_box import TextBox
from menu_bar import MenuBar

from os.path import basename


class TextEditorApp(ttk.Window):
    def __init__(self):

        self.file_path = None
        self.allowed_file_types = [
            ("Text documents (*.txt)", "*.txt"),
            ("Markdown documents (*.md)", "*.md"),
            ("All files (*)", "*"),
        ]

        super().__init__(
            "New File - Text Editor",
            size=(750, 600),
            minsize=(300, 150),
        )

        self.create_plain_text_editor()

        self.update_clock()

    def create_plain_text_editor(self):
        self.textbox = TextBox(self)
        self.menu = MenuBar(self)
        self.place_plain_text_editor()

    def place_plain_text_editor(self):
        self.textbox.pack(fill="both", expand=True)
        self.configure(menu=self.menu)
        self.create_keybinds()

    def remove_plain_text_editor(self):
        self.textbox.pack_forget()
        self.configure(menu="")
        self.remove_keybinds()

    def new_file_command(self):
        if self.save_prompt() == "Cancel":
            return

        self.textbox.clear_text()
        self.file_path = None
        self.textbox.status_bar.update_word_count()
        self.textbox.saved_state = "\n"
        self.textbox.status_bar.update_file_path()
        self.title("New File - Text Editor")
        self.textbox.set_line_number()

    def open_command(self):
        if self.save_prompt() == "Cancel":
            return
        file_path = askopenfilename(
            defaultextension=".txt",
            filetypes=self.allowed_file_types,
        )
        if file_path.strip() == "":
            return
        self.file_path = file_path

        with open(self.file_path, mode="r") as file:
            self.textbox.clear_text()
            self.textbox.text.insert("end", file.read())
        self.textbox.status_bar.update_word_count()
        self.textbox.saved_state = self.textbox.get_text()
        self.textbox.status_bar.update_file_path()
        self.set_title()
        self.textbox.text.edit_reset()
        self.textbox.set_line_number()

    def save_command(self):
        if self.file_path is not None:
            self.save()
        else:
            self.save_as_command()

    def save_as_command(self):
        file_path = asksaveasfilename(
            title="Save as",
            confirmoverwrite=True,
            defaultextension=".txt",
            filetypes=self.allowed_file_types,
            initialfile=self.textbox.get_text().split("\n")[0],
        )
        if file_path.strip() == "":
            return
        self.file_path = file_path
        self.save()

    def save(self):
        with open(self.file_path, mode="w") as file:
            file.write(self.textbox.get_text())
        self.textbox.saved_state = self.textbox.get_text()
        self.textbox.status_bar.update_file_path()
        self.set_title()

    def create_keybinds(self):
        self.bind_all("<Control-o>", lambda _: self.open_command())
        self.bind_all("<Control-s>", lambda _: self.save_command())
        self.bind_all("<Control-Shift-S>", lambda _: self.save_as_command())
        self.bind_all("<Control-=>", lambda _: self.textbox.increment_zoom(1))
        self.bind_all("<Control-minus>", lambda _: self.textbox.increment_zoom(-1))
        self.bind_all("<Control-0>", lambda _: self.textbox.set_zoom(100))
        self.bind_all("<Control-z>", lambda _: self.textbox.undo_text())
        self.bind_all("<Control-Shift-Z>", lambda _: self.textbox.redo_text())

        self.protocol("WM_DELETE_WINDOW", self.plain_text_editor_on_close)

    def remove_keybinds(self):
        self.unbind_all("<Control-o>")
        self.unbind_all("<Control-s>")
        self.unbind_all("<Control-Shift-S>")
        self.unbind_all("<Control-=>")
        self.unbind_all("<Control-minus>")
        self.unbind_all("<Control-0>")
        self.unbind_all("<Control-z>")
        self.unbind_all("<Control-Shift-Z>")

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def update_clock(self):
        self.textbox.status_bar.update_word_count()
        self.textbox.status_bar.update_zoom_percent()
        self.textbox.status_bar.update_is_saved()
        # self.textbox.update_line_numbers()
        self.after(10, self.update_clock)

    def plain_text_editor_on_close(self):
        if self.save_prompt() == "Cancel":
            return
        self.destroy()

    def save_prompt(self):
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
                return "Cancel"

    def set_title(self):
        self.title(
            f"{'.'.join(basename(self.file_path).split('.')[:-1])} - Text Editor"
        )


if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
