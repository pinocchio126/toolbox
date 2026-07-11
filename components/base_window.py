# components/base_window.py - 工具窗口基类（customtkinter）
import customtkinter as ctk
from config import COLORS


class BaseToolWindow:
    """所有工具窗口的基类（使用 CTkToplevel）"""

    def __init__(self, parent, title, subtitle=""):
        self.parent = parent
        self.title = title
        self.subtitle = subtitle
        self.window = None

    def open(self):
        """打开工具窗口，确保默认尺寸足够显示全部内容"""
        if self.window is not None and self.window.winfo_exists():
            self.window.focus_force()
            return

        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("1100x800")  # 默认高度800，确保底部内容可见
        self.window.minsize(900, 650)  # 最小高度650，防止内容被完全遮挡
        self.window.configure(fg_color=COLORS["bg_main"])
        self.window.transient(self.parent)
        self.window.focus_force()
        self.window.grab_set()

        self.setup_ui()

        # 窗口关闭时释放 grab
        def on_close():
            if self.window:
                self.window.grab_release()
                self.window.destroy()
                self.window = None

        self.window.protocol("WM_DELETE_WINDOW", on_close)

    def setup_ui(self):
        """子类重写此方法构建界面"""
        raise NotImplementedError
