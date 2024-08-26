import ttkbootstrap as ttk


class MenuBar(ttk.Menu):
    def __init__(self, master):
        self.master = master
        super().__init__(master, tearoff=False)

        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()

    def create_view_menu(self):
        view_menu = ttk.Menu(self, tearoff=False)

        zoom_menu = ttk.Menu(view_menu, tearoff=False)
        zoom_menu.add_command(
            label="Zoom in",
            command=lambda: self.master.textbox.increment_zoom(1),
            accelerator="Ctrl+Plus",
        )
        zoom_menu.add_command(
            label="Zoom out",
            command=lambda: self.master.textbox.increment_zoom(-1),
            accelerator="Ctrl+Minus",
        )
        zoom_menu.add_command(
            label="Restore default zoom",
            command=lambda: self.master.textbox.set_zoom(100),
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
            variable=self.master.textbox.status_bar_enabled,
            command=self.master.textbox.change_status_bar_visibility,
        )
        view_menu.add_checkbutton(
            label="File path",
            offvalue=False,
            onvalue=True,
            variable=self.master.textbox.status_bar.file_path_enabled,
            command=self.master.textbox.status_bar.change_file_path_visiblilty,
        )
        view_menu.add_checkbutton(
            label="Line numbers",
            offvalue=False,
            onvalue=True,
            variable=self.master.textbox.line_numbers_enabled,
            command=self.master.textbox.change_line_numbers_visibility,
        )
        self.add_cascade(label="View", menu=view_menu)

    def create_edit_menu(self):
        edit_menu = ttk.Menu(self, tearoff=False)

        edit_menu.add_checkbutton(
            label="Space Indentation",
            offvalue=False,
            onvalue=True,
            variable=self.master.textbox.no_tabs,
            command=self.master.textbox.change_tab_to_space,
        )
        edit_menu.add_command(
            label="Revert to save", command=self.master.textbox.revert_to_save
        )
        self.add_cascade(label="Edit", menu=edit_menu)

    def create_file_menu(self):
        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="New file", command=self.master.new_file_command, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open", command=self.master.open_command, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self.master.save_command, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save as",
            command=self.master.save_as_command,
            accelerator="Ctrl+Shift+O",
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Settings", command=lambda: print("Settings!"), accelerator="Ctrl+,"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)
        self.add_cascade(label="File", menu=file_menu)
