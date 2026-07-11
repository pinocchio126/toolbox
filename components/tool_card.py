# components/tool_card.py
import customtkinter as ctk
from config import (
    COLORS,
    FONT_XXLARGE_BOLD,
    FONT_LARGE_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
)


class ToolCard(ctk.CTkFrame):
    def __init__(
        self, parent, icon, name, description, status, tool_class=None, **kwargs
    ):
        super().__init__(
            parent, fg_color=COLORS["bg_white"], corner_radius=10, **kwargs
        )
        self.tool_class = tool_class
        self.status = status

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        ctk.CTkLabel(inner, text=icon, font=FONT_XXLARGE_BOLD).pack(anchor="w")
        ctk.CTkLabel(
            inner, text=name, font=FONT_LARGE_BOLD, text_color=COLORS["text_primary"]
        ).pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(
            inner,
            text=description,
            font=FONT_SMALL,
            text_color=COLORS["text_secondary"],
            wraplength=230,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        bottom = ctk.CTkFrame(inner, fg_color="transparent")
        bottom.pack(fill="x", pady=(14, 0))

        if status == "可用":
            ctk.CTkLabel(
                bottom,
                text="● 可用",
                font=FONT_SMALL_BOLD,
                text_color=COLORS["success"],
            ).pack(side="left")
            self.open_btn = ctk.CTkButton(
                bottom,
                text="打开工具",
                width=80,
                height=30,
                corner_radius=8,
                font=FONT_SMALL,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                command=self._open_tool,
            )
            self.open_btn.pack(side="right")
        else:
            ctk.CTkLabel(
                bottom,
                text="⏳ 即将上线",
                font=FONT_SMALL,
                text_color=COLORS["text_hint"],
            ).pack(side="left")
            ctk.CTkButton(
                bottom,
                text="敬请期待",
                state="disabled",
                width=80,
                height=30,
                corner_radius=8,
                font=FONT_SMALL,
                fg_color=COLORS["border"],
                text_color=COLORS["text_hint"],
            ).pack(side="right")

    def _open_tool(self):
        if self.tool_class and self.status == "可用":
            root = self.winfo_toplevel()
            tool = self.tool_class(root)
            tool.open()
