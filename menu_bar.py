import ttkbootstrap as ttk


class MenuBar(ttk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)

        file_menu = ttk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Open", command=master.open_command, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=master.save_command, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As", command=master.save_as_command, accelerator="Ctrl+Shift+O"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: master.quit())
        self.add_cascade(label="File", menu=file_menu)

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
        self.add_cascade(label="View", menu=view_menu)
