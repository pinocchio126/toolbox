# 自动化工具箱

一个基于 Python + customtkinter 的 Windows 桌面工具箱，用来集中管理常用批处理任务。

## 功能

- **批量重命名**：自动识别单剧目录或多剧目录，提取集数并生成统一文件名预览。
- **可视化统计**：展示总文件、待处理、已完成、失败数量，点击统计卡片可查看明细。
- **模块化结构**：工具入口、统计卡片、窗口基类独立封装，方便继续扩展新工具。
- **现代化 UI**：统一配色、字体、卡片状态和占位工具提示。

## 快速开始

```bash
pip install customtkinter
python main.py
```

## 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="自动化工具箱" --hidden-import=customtkinter main.py
```

也可以直接运行：

```bash
build.bat
```

## 项目结构

```text
MyToolbox/
├── main.py                 # 主入口
├── config.py               # 全局配置：颜色、字体、工具列表
├── components/             # 可复用 UI 组件
│   ├── stat_card.py        # 统计卡片
│   ├── tool_card.py        # 工具卡片
│   └── base_window.py      # 工具窗口基类
├── tools/                  # 各工具实现
│   ├── rename_tool.py      # 批量重命名工具
│   ├── upload_tool.py      # 上传工具占位
│   └── fill_tool.py        # 填表工具占位
└── build.bat               # 打包脚本
```
