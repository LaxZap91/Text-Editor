import ttkbootstrap as ttk


class MenuBar(ttk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)

        self.create_file_menu(master)
        self.create_edit_menu(master)
        self.create_view_menu(master)

    def create_view_menu(self, master):
        view_menu = ttk.Menu(self, tearoff=False)

        zoom_menu = ttk.Menu(view_menu, tearoff=False)
        zoom_menu.add_command(
            label="Zoom in",
            command=lambda: master.textbox.increment_zoom(1),
            accelerator="Ctrl+Plus",
        )
        zoom_menu.add_command(
            label="Zoom out",
            command=lambda: master.textbox.increment_zoom(-1),
            accelerator="Ctrl+Minus",
        )
        zoom_menu.add_command(
            label="Restore default zoom",
            command=lambda: master.textbox.set_zoom(100),
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
            variable=master.textbox.status_bar_enabled,
            command=master.textbox.change_status_bar_visibility,
        )
        view_menu.add_checkbutton(
            label="File path",
            offvalue=False,
            onvalue=True,
            variable=master.textbox.status_bar.file_path_enabled,
            command=master.textbox.status_bar.change_file_path_visiblilty,
        )
        view_menu.add_checkbutton(
            label="Line numbers",
            offvalue=False,
            onvalue=True,
            variable=master.textbox.line_numbers_enabled,
            command=master.textbox.change_line_numbers_visibility,
        )
        self.add_cascade(label="View", menu=view_menu)

    def create_edit_menu(self, master):
        edit_menu = ttk.Menu(self, tearoff=False)

        edit_menu.add_checkbutton(
            label="Space Indentation",
            offvalue=False,
            onvalue=True,
            variable=master.textbox.no_tabs,
            command=master.textbox.change_tab_to_space,
        )
        self.add_cascade(label="Edit", menu=edit_menu)

    def create_file_menu(self, master):
        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="New file", command=master.new_file_command, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open", command=master.open_command, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=master.save_command, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save as", command=master.save_as_command, accelerator="Ctrl+Shift+O"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Settings", command=lambda: print("Settings!"), accelerator="Ctrl+,"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.destroy)
        self.add_cascade(label="File", menu=file_menu)
