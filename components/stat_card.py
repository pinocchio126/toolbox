import customtkinter as ctk

from config import COLORS, FONT_XXLARGE_BOLD, FONT_MEDIUM


class StatCard(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        label,
        initial_value="0",
        color=COLORS["text_primary"],
        command=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            fg_color=COLORS["bg_white"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )
        self.value_var = ctk.StringVar(value=initial_value)

        self.value_label = ctk.CTkLabel(
            self,
            textvariable=self.value_var,
            font=FONT_XXLARGE_BOLD,
            text_color=color,
        )
        self.value_label.pack(pady=(12, 0))

        self.label_label = ctk.CTkLabel(
            self,
            text=label,
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        )
        self.label_label.pack(pady=(0, 12))

        if command is not None:
            self.bind("<Button-1>", lambda _event: command())
            self.value_label.bind("<Button-1>", lambda _event: command())
            self.label_label.bind("<Button-1>", lambda _event: command())
            self.configure(cursor="hand2")
            self.value_label.configure(cursor="hand2")
            self.label_label.configure(cursor="hand2")

    def set_value(self, value):
        self.value_var.set(str(value))
