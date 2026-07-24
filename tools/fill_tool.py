import customtkinter as ctk

from config import COLORS, FONT_XXLARGE_BOLD, FONT_XLARGE_BOLD, FONT_MEDIUM, FONT_MEDIUM_BOLD
from components import BaseToolWindow


class FillTool(BaseToolWindow):
    def __init__(self, parent):
        super().__init__(parent, "填表工具", "配置字段并批量自动填写目标表单")

    def setup_ui(self):
        main = self.window
        center = ctk.CTkFrame(main, fg_color="transparent")
        center.pack(expand=True)

        card = ctk.CTkFrame(
            center,
            fg_color=COLORS["bg_white"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(padx=48, pady=40)

        ctk.CTkLabel(card, text="✍️", font=FONT_XXLARGE_BOLD).pack(pady=(26, 12))
        ctk.CTkLabel(
            card,
            text="填表工具",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack()
        ctk.CTkLabel(
            card,
            text="配置表单字段，批量自动填写目标表单",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(padx=48, pady=(6, 0))
        ctk.CTkLabel(
            card,
            text="功能开发中",
            font=FONT_MEDIUM_BOLD,
            text_color=COLORS["primary"],
        ).pack(pady=(18, 26))
