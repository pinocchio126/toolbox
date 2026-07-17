import customtkinter as ctk
from config import (
    COLORS,
    TOOLS_CONFIG,
    TOOLS_FAMTLY,
    FONT_XLARGE_BOLD,
    FONT_MEDIUM,
    FONT_LARGE_BOLD,
    FONT_SMALL_BOLD,
    FONT_SMALL,
)
from components import ToolCard
from tools import RenameTool, UploadTool, FillTool


class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("自动化工具箱 v1.0")
        self.root.geometry("1000x680")
        self.root.minsize(880, 600)
        self.root.configure(fg_color=COLORS["bg_main"])

        header = ctk.CTkFrame(self.root, fg_color=COLORS["bg_white"], corner_radius=10)
        header.pack(fill="x", padx=20, pady=(20, 0))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(padx=16, pady=12, anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="🧰 自动化工具箱",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(side="left", padx=(0, 14))
        ctk.CTkLabel(
            title_frame,
            text="选择工具模块开始工作，提升批量处理效率",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        stat_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        stat_frame.pack(fill="x", padx=20, pady=(16, 8))

        ctk.CTkLabel(
            stat_frame,
            text="全部工具（3个可用 / 6个总计）",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        tools_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        tools_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tool_classes = {
            "重命名工具": RenameTool,
            "上传工具": UploadTool,
            "填表工具": FillTool,
        }

        for i, (name, icon, desc, status) in enumerate(TOOLS_CONFIG):
            row = i // 3
            col = i % 3
            tool_class = tool_classes.get(name)
            card = ToolCard(tools_frame, icon, name, desc, status, tool_class)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            tools_frame.grid_rowconfigure(row, weight=1)
            tools_frame.grid_columnconfigure(col, weight=1)

        footer = ctk.CTkFrame(self.root, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            footer,
            text="更多工具模块持续开发中",
            font=FONT_SMALL,
            text_color=COLORS["text_hint"],
        ).pack(anchor="w")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
