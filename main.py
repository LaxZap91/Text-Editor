import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from ttkbootstrap.dialogs import MessageDialog
from text_box import TextBox
from status_bar import StatusBar


class TextEditorApp(ttk.Window):
    def __init__(self):
        self.file_path = None

        super().__init__(
            "Text Editor",
            size=(500, 500),
            minsize=(250, 100),
            iconphoto="icon/icon.png",
        )
        self.word_count = ttk.StringVar(value="0 characters")
        self.zoom_level = ttk.StringVar(value="100%")
        self.is_saved = ttk.StringVar(value="Saved: False")
        self.status_bar_enabled = ttk.BooleanVar(value=True)
        self.saved_state = "\n"

        self.create_menu_bar()
        self.create_textbox()
        self.create_status_bar()
        self.create_keybinds()

        self.update_clock()

    def create_menu_bar(self):
        menu = ttk.Menu(self, tearoff=False)
        self.configure(menu=menu)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(
            label="Open", command=self.open_command, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self.save_command, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As", command=self.save_as_command, accelerator="Ctrl+Shift+O"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: self.quit())
        menu.add_cascade(label="File", menu=file_menu)

        view_menu = ttk.Menu(menu, tearoff=False)

        zoom_menu = ttk.Menu(view_menu, tearoff=False)
        zoom_menu.add_command(
            label="Zoom in",
            command=lambda: self.textbox.increment_zoom(1),
            accelerator="Ctrl+Plus",
        )
        zoom_menu.add_command(
            label="Zoom out",
            command=lambda: self.textbox.increment_zoom(-1),
            accelerator="Ctrl+Minus",
        )
        zoom_menu.add_command(
            label="Restore default zoom",
            command=lambda: self.textbox.set_zoom(100),
            accelerator="Ctrl+0",
        )
        view_menu.add_cascade(
            label="Zoom",
            menu=zoom_menu,
        )

        view_menu.add_checkbutton(
            label="Status bar",
            offvalue=False,
            onvalue=True,
            variable=self.status_bar_enabled,
            command=self.change_status_bar_visibility,
        )
        menu.add_cascade(label="View", menu=view_menu)

    def create_textbox(self):
        self.textbox = TextBox(self)
        self.textbox.pack(fill="both", expand=True)

    def create_status_bar(self):
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill="both")

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
            self.textbox.text.delete(1.0, "end")
            self.textbox.text.insert("end", file.read())
        self.status_bar.update_word_count()
        self.saved_state = self.textbox.text.get(1.0, "end")

    def save_command(self):
        if self.file_path is not None:
            with open(self.file_path, "w") as file:
                file.write(self.textbox.text.get(1.0, "end"))
        else:
            self.save_as_command()
        self.saved_state = self.textbox.text.get(1.0, "end")

    def save_as_command(self):
        file_path = asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".txt",
            filetypes=[
                ("Text documents (*.txt)", "*.txt"),
                ("Markdown documents (*.md)", "*.md"),
                ("All files (*)", "*"),
            ],
            initialfile=self.textbox.text.get(1.0, "end").split("\n")[0],
        )
        if file_path.strip() == "":
            return
        with open(file_path, mode="w") as file:
            file.write(self.text.get(1.0, "end"))

    def create_keybinds(self):
        self.bind_all("<Control-o>", lambda _: self.open_command())
        self.bind_all("<Control-s>", lambda _: self.save_command())
        self.bind_all("<Control-Shift-S>", lambda _: self.save_as_command())
        self.bind_all("<Control-=>", lambda _: self.textbox.increment_zoom(1))
        self.bind_all("<Control-minus>", lambda _: self.textbox.increment_zoom(-1))
        self.bind_all("<Control-0>", lambda _: self.textbox.set_zoom(100))
        self.bind_all("<Control-z>", lambda _: self.undo_text())
        self.bind_all("<Control-Shift-Z>", lambda _: self.redo_text())

        self.protocol("WM_DELETE_WINDOW", self.display_check_save)

    def change_status_bar_visibility(self):
        if self.status_bar_enabled.get():
            self.status_bar.pack(fill="both")
        else:
            self.status_bar.pack_forget()

    def update_clock(self):
        self.status_bar.update_word_count()
        self.status_bar.update_zoom_percent()
        self.status_bar.update_is_saved()
        self.after(10, self.update_clock)

    def undo_text(self):
        try:
            self.textbox.text.edit_undo()
        except Exception:
            pass

    def redo_text(self):
        try:
            self.textbox.text.edit_redo()
        except Exception:
            pass

    def is_not_modified(self):
        return self.saved_state == self.textbox.text.get(1.0, "end")

    def display_check_save(self):
        if not self.is_not_modified():
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
