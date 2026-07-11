# 🧰 自动化工具箱

一个基于 Python + customtkinter 的 Windows 桌面自动化工具集，用于批量处理影视文件重命名等任务，界面采用飞书（Lark）风格。

## ✨ 功能特性

- 📁 **批量重命名**：自动识别单剧目/多剧目模式，支持集数提取和统一命名
- 📊 **可视化统计**：实时显示总文件、待处理、已完成、失败数量，点击卡片可查看详情
- 🧩 **模块化设计**：易于扩展新工具（上传、填表等）
- 🎨 **飞书风格 UI**：统一圆角、配色、字体，提供现代化交互体验
- 📦 **单文件打包**：支持打包为独立 `.exe`，无需安装 Python 即可运行

## 🚀 快速开始

### 环境要求
- Python 3.10+
- 安装依赖：
```bash
pip install customtkinter CTkTable

#运行
python main.py

# 安装 PyInstaller
pip install pyinstaller

# 执行打包（单文件，无控制台）
pyinstaller --onefile --windowed --name="自动化工具箱" --hidden-import=customtkinter --hidden-import=CTkTable main.py


MyToolbox/
├── main.py                 # 主入口
├── config.py               # 全局配置（颜色、字体、工具列表）
├── components/             # 可复用 UI 组件
│   ├── stat_card.py        # 统计卡片（支持点击回调）
│   ├── tool_card.py        # 工具卡片
│   └── base_window.py      # 工具窗口基类
├── tools/                  # 各工具实现
│   ├── rename_tool.py      # 重命名工具（核心）
│   ├── upload_tool.py      # 上传工具（占位）
│   └── fill_tool.py        # 填表工具（占位）
└── build.bat               # 一键打包脚本