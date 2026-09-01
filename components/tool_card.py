import customtkinter as ctk

from config import COLORS, FONT_XXLARGE_BOLD, FONT_LARGE_BOLD, FONT_SMALL, FONT_SMALL_BOLD


class ToolCard(ctk.CTkFrame):
    def __init__(self, parent, icon, name, description, status, tool_class=None, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_white"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )
        self.tool_class = tool_class
        self.status = status
        self.name = name

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(top, text=icon, font=FONT_XXLARGE_BOLD).pack(side="left")
        status_text = "可用" if status == "available" else "即将上线"
        status_color = COLORS["success"] if status == "available" else COLORS["text_hint"]
        ctk.CTkLabel(
            top,
            text=status_text,
            font=FONT_SMALL_BOLD,
            text_color=status_color,
        ).pack(side="right")

        ctk.CTkLabel(
            inner,
            text=name,
            font=FONT_LARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(14, 0))
        ctk.CTkLabel(
            inner,
            text=description,
            font=FONT_SMALL,
            text_color=COLORS["text_secondary"],
            wraplength=240,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        bottom = ctk.CTkFrame(inner, fg_color="transparent")
        bottom.pack(fill="x", side="bottom", pady=(18, 0))

        if status == "available":
            self.open_btn = ctk.CTkButton(
                bottom,
                text="打开",
                width=90,
                height=32,
                corner_radius=8,
                font=FONT_SMALL_BOLD,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                command=self._open_tool,
            )
            self.open_btn.pack(side="right")
        else:
            ctk.CTkButton(
                bottom,
                text="敬请期待",
                state="disabled",
                width=90,
                height=32,
                corner_radius=8,
                font=FONT_SMALL,
                fg_color=COLORS["border"],
                text_color=COLORS["text_hint"],
            ).pack(side="right")

    def _on_enter(self, _event):
        self.configure(fg_color=COLORS["bg_card_hover"])

    def _on_leave(self, _event):
        self.configure(fg_color=COLORS["bg_white"])

    def _open_tool(self):
        if self.tool_class and self.status == "available":
            root = self.winfo_toplevel()
            tool = self.tool_class(root)
            tool.open()
