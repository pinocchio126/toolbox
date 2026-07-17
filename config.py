# config.py - 全局配置与飞书主题
import customtkinter as ctk

# 设置全局主题（飞书风格）
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# 飞书官方色系
COLORS = {
    "primary": "#2584FF",
    "primary_hover": "#1976E8",
    "success": "#00B42A",
    "warning": "#FFAA00",
    "danger": "#F53F3F",
    "bg_main": "#F7F8FA",
    "bg_white": "#FFFFFF",
    "bg_card_hover": "#F2F3F5",
    "border": "#E5E7EB",
    "text_primary": "#1F2937",
    "text_secondary": "#6B7280",
    "text_hint": "#9CA3AF",
}

# ===== 全局字体配置（支持多语言切换） =====
# 可根据系统语言或用户设置动态切换，此处预设中文与英文备选
# FONT_FAMILY = "微软雅黑"  # 中文系统默认；英文环境可改为 "Segoe UI"
FONT_FAMILY = "Segoe UI"  # 取消注释以切换到英文风格

# 字号层级
FONT_SIZE_SMALL = 10
FONT_SIZE_MEDIUM = 12
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 18
FONT_SIZE_XXLARGE = 22

# 字重
FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_BOLD = "bold"

# 便捷字体组合（供各控件直接使用）
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

# 工具配置（不变）
TOOLS_CONFIG = [
    ("重命名工具", "📁", "批量重命名影视文件，支持集数自动识别与预览", "可用"),
    ("上传工具", "📤", "拖拽或选择文件，批量上传到目标位置", "可用"),
    ("填表工具", "✍️", "配置表单字段，批量自动填写目标表单", "可用"),
    ("文件转换", "🔄", "批量转换文件格式，支持文档与图片类型", "即将上线"),
    ("批量下载", "⬇️", "从链接列表批量下载文件到本地目录", "即将上线"),
    ("数据清洗", "🧹", "批量清洗和格式化数据，支持正则替换规则", "即将上线"),
]

TOOLS_FAMTLY = [
    (
        "ReName",
        "📁",
        "Rename video files by weight, supporting automatic episode number recognition and preview",
        "workable",
    ),
    (
        "UploadTool",
        "📤",
        "Drag and drop or select the files, and upload them in batches to the target location.",
        "workable",
    ),
    (
        "Fill",
        "✍️",
        "Configure form fields and automatically fill in the target form in batches",
        "workable",
    ),
]
