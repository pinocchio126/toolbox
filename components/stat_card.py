# components/stat_card.py
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
        **kwargs
    ):
        super().__init__(
            parent, fg_color=COLORS["bg_white"], corner_radius=10, **kwargs
        )
        self.value_var = ctk.StringVar(value=initial_value)

        self.value_label = ctk.CTkLabel(
            self, textvariable=self.value_var, font=FONT_XXLARGE_BOLD, text_color=color
        )
        self.value_label.pack(pady=(12, 0))

        self.label_label = ctk.CTkLabel(
            self, text=label, font=FONT_MEDIUM, text_color=COLORS["text_secondary"]
        )
        self.label_label.pack(pady=(0, 12))

        # 如果提供了回调函数，绑定点击事件
        if command is not None:
            # 绑定整个卡片及内部控件
            self.bind("<Button-1>", lambda e: command())
            self.value_label.bind("<Button-1>", lambda e: command())
            self.label_label.bind("<Button-1>", lambda e: command())
            # 设置鼠标样式为手型
            self.configure(cursor="hand2")
            self.value_label.configure(cursor="hand2")
            self.label_label.configure(cursor="hand2")

    def set_value(self, value):
        self.value_var.set(str(value))
