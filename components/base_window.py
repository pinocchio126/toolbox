import customtkinter as ctk

from config import COLORS


class BaseToolWindow:
    def __init__(self, parent, title, subtitle=""):
        self.parent = parent
        self.title = title
        self.subtitle = subtitle
        self.window = None

    def open(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.focus_force()
            return

        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("1100x780")
        self.window.minsize(920, 640)
        self.window.configure(fg_color=COLORS["bg_main"])
        self.window.transient(self.parent)
        self.window.focus_force()
        self.window.grab_set()

        self.setup_ui()

        def on_close():
            if self.window:
                self.window.grab_release()
                self.window.destroy()
                self.window = None

        self.window.protocol("WM_DELETE_WINDOW", on_close)

    def setup_ui(self):
        raise NotImplementedError
