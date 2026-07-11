# tools/fill_tool.py - 填表工具占位
import customtkinter as ctk
from config import COLORS
from components import BaseToolWindow


class FillTool(BaseToolWindow):
    def setup_ui(self):
        main = self.window
        center = ctk.CTkFrame(main, fg_color="transparent")
        center.pack(expand=True)

        card = ctk.CTkFrame(center, fg_color=COLORS["bg_white"], corner_radius=10)
        card.pack(padx=48, pady=40)

        ctk.CTkLabel(card, text="✍️", font=("微软雅黑", 40)).pack(pady=(0, 12))
        ctk.CTkLabel(
            card,
            text="填表工具",
            font=("微软雅黑", 18, "bold"),
            text_color=COLORS["text_primary"],
        ).pack()
        ctk.CTkLabel(
            card,
            text="配置表单字段，批量自动填写目标表单",
            font=("微软雅黑", 12),
            text_color=COLORS["text_secondary"],
        ).pack(pady=(4, 0))
        ctk.CTkLabel(
            card,
            text="🚧 功能开发中",
            font=("微软雅黑", 11),
            text_color=COLORS["primary"],
        ).pack(pady=(16, 0))
