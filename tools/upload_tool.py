import customtkinter as ctk
from config import (
    COLORS,
    FONT_XXLARGE_BOLD,
    FONT_XLARGE_BOLD,
    FONT_MEDIUM,
    FONT_MEDIUM_BOLD,
    FONT_SMALL,
)
from components import BaseToolWindow


class UploadTool(BaseToolWindow):
    def setup_ui(self):
        main = self.window
        center = ctk.CTkFrame(main, fg_color="transparent")
        center.pack(expand=True)

        card = ctk.CTkFrame(center, fg_color=COLORS["bg_white"], corner_radius=10)
        card.pack(padx=48, pady=40)

        ctk.CTkLabel(card, text="📤", font=FONT_XXLARGE_BOLD).pack(pady=(0, 12))
        ctk.CTkLabel(
            card,
            text="上传工具",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack()
        ctk.CTkLabel(
            card,
            text="拖拽或选择文件，批量上传到目标位置",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(pady=(4, 0))
        ctk.CTkLabel(
            card,
            text="🚧 功能开发中",
            font=FONT_MEDIUM_BOLD,
            text_color=COLORS["primary"],
        ).pack(pady=(16, 0))
