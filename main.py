import customtkinter as ctk

from config import COLORS, TOOLS_CONFIG, FONT_XLARGE_BOLD, FONT_MEDIUM, FONT_SMALL
from components import ToolCard
from tools import FillTool, RenameTool, UploadTool


class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("自动化工具箱 v1.1")
        self.root.geometry("1040x700")
        self.root.minsize(900, 620)
        self.root.configure(fg_color=COLORS["bg_main"])

        available_count = sum(1 for tool in TOOLS_CONFIG if tool[4] == "available")

        header = ctk.CTkFrame(self.root, fg_color=COLORS["bg_white"], corner_radius=10)
        header.pack(fill="x", padx=24, pady=(24, 0))

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=16)

        title_block = ctk.CTkFrame(header_inner, fg_color="transparent")
        title_block.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_block,
            text="🧰 自动化工具箱",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="把常用批处理能力集中到一个清爽入口，少点重复操作。",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(6, 0))

        summary = ctk.CTkFrame(header_inner, fg_color=COLORS["bg_main"], corner_radius=8)
        summary.pack(side="right", padx=(16, 0))
        ctk.CTkLabel(
            summary,
            text=f"{available_count}/{len(TOOLS_CONFIG)}",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["primary"],
        ).pack(padx=18, pady=(10, 0))
        ctk.CTkLabel(
            summary,
            text="可用工具",
            font=FONT_SMALL,
            text_color=COLORS["text_secondary"],
        ).pack(padx=18, pady=(0, 10))

        section = ctk.CTkFrame(self.root, fg_color="transparent")
        section.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(
            section,
            text="工具列表",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        tools_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        tools_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        tool_classes = {
            "rename": RenameTool,
            "upload": UploadTool,
            "fill": FillTool,
        }

        for index, (tool_id, icon, name, description, status) in enumerate(TOOLS_CONFIG):
            row = index // 3
            column = index % 3
            card = ToolCard(
                tools_frame,
                icon,
                name,
                description,
                status,
                tool_classes.get(tool_id),
            )
            card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            tools_frame.grid_rowconfigure(row, weight=1, uniform="tool_row")
            tools_frame.grid_columnconfigure(column, weight=1, uniform="tool_col")

        footer = ctk.CTkFrame(self.root, fg_color="transparent")
        footer.pack(fill="x", padx=24, pady=(0, 20))

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
