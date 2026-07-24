import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORS = {
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "bg_main": "#F6F7FB",
    "bg_white": "#FFFFFF",
    "bg_card_hover": "#F1F5F9",
    "border": "#E2E8F0",
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
    "text_hint": "#94A3B8",
}

FONT_FAMILY = "Microsoft YaHei UI"

FONT_SIZE_SMALL = 11
FONT_SIZE_MEDIUM = 13
FONT_SIZE_LARGE = 15
FONT_SIZE_XLARGE = 20
FONT_SIZE_XXLARGE = 30

FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_BOLD = "bold"

FONT_SMALL = (FONT_FAMILY, FONT_SIZE_SMALL)
FONT_MEDIUM = (FONT_FAMILY, FONT_SIZE_MEDIUM)
FONT_LARGE = (FONT_FAMILY, FONT_SIZE_LARGE)
FONT_XLARGE = (FONT_FAMILY, FONT_SIZE_XLARGE)
FONT_XXLARGE = (FONT_FAMILY, FONT_SIZE_XXLARGE)
FONT_SMALL_BOLD = (FONT_FAMILY, FONT_SIZE_SMALL, FONT_WEIGHT_BOLD)
FONT_MEDIUM_BOLD = (FONT_FAMILY, FONT_SIZE_MEDIUM, FONT_WEIGHT_BOLD)
FONT_LARGE_BOLD = (FONT_FAMILY, FONT_SIZE_LARGE, FONT_WEIGHT_BOLD)
FONT_XLARGE_BOLD = (FONT_FAMILY, FONT_SIZE_XLARGE, FONT_WEIGHT_BOLD)
FONT_XXLARGE_BOLD = (FONT_FAMILY, FONT_SIZE_XXLARGE, FONT_WEIGHT_BOLD)

TOOLS_CONFIG = [
    ("rename", "📁", "批量重命名", "批量重命名影视文件，自动识别集数并生成预览", "available"),
    ("upload", "⬆️", "上传工具", "选择文件并批量上传到目标位置", "available"),
    ("fill", "✍️", "填表工具", "配置表单字段，批量自动填写目标表单", "available"),
    ("convert", "🔁", "文件转换", "批量转换文档、图片等常用文件格式", "soon"),
    ("download", "⬇️", "批量下载", "从链接列表批量下载文件到本地目录", "soon"),
    ("clean", "🧹", "数据清洗", "批量清洗、格式化数据，支持正则替换规则", "soon"),
]
