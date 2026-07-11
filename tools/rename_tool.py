# tools/rename_tool.py - 重命名工具（支持统计卡片点击查看详情，按钮右对齐）
import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from config import (
    COLORS,
    FONT_XLARGE_BOLD,
    FONT_MEDIUM,
    FONT_SMALL,
    FONT_MEDIUM_BOLD,
    FONT_SMALL_BOLD,
    FONT_LARGE_BOLD,
    FONT_LARGE,
    FONT_XXLARGE_BOLD,
)
from components import BaseToolWindow, StatCard


class RenameTool(BaseToolWindow):
    def __init__(self, parent):
        super().__init__(
            parent, "重命名工具", "选择文件夹或根目录，自动识别模式并批量重命名"
        )
        self.selected_path = None
        self.mode = None
        self.file_data = []
        self.folder_stats = {}
        self.stat_cards = {}

    def setup_ui(self):
        main = self.window
        pad = 20

        # ----- 顶部标题 -----
        header = ctk.CTkFrame(main, fg_color=COLORS["bg_white"], corner_radius=10)
        header.pack(fill="x", padx=pad, pady=(pad, 0))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(padx=16, pady=12, anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="📁 重命名工具",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(
            title_frame,
            text=self.subtitle,
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        # ----- 统计卡片行（可点击）-----
        stats_frame = ctk.CTkFrame(main, fg_color="transparent")
        stats_frame.pack(fill="x", padx=pad, pady=pad)

        stat_configs = [
            ("📄 总文件", COLORS["text_secondary"], "total"),
            ("⏳ 待处理", COLORS["warning"], "pending"),
            ("✅ 已完成", COLORS["success"], "done"),
            ("❌ 失败", COLORS["danger"], "failed"),
        ]
        for label, color, filter_type in stat_configs:
            card = StatCard(
                stats_frame,
                label,
                color=color,
                command=lambda ft=filter_type: self._show_result_list(ft),
            )
            card.pack(side="left", padx=(0, 12), fill="x", expand=True)
            self.stat_cards[label] = card

        # ----- 设置区域（路径选择 + 模式提示）-----
        settings_frame = ctk.CTkFrame(
            main, fg_color=COLORS["bg_white"], corner_radius=10
        )
        settings_frame.pack(fill="x", padx=pad, pady=(0, pad))

        settings_inner = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            settings_inner,
            text="目标路径",
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        self.path_display = ctk.CTkLabel(
            settings_inner,
            text="未选择",
            font=FONT_MEDIUM,
            text_color=COLORS["text_hint"],
        )
        self.path_display.pack(side="left", padx=(10, 12))

        self.select_btn = ctk.CTkButton(
            settings_inner,
            text="选择路径",
            width=120,
            height=34,
            corner_radius=8,
            font=FONT_SMALL_BOLD,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.select_path,
        )
        self.select_btn.pack(side="left")

        self.mode_label = ctk.CTkLabel(
            settings_inner, text="", font=FONT_MEDIUM_BOLD, text_color=COLORS["primary"]
        )
        self.mode_label.pack(side="left", padx=(20, 0))

        # ----- 操作按钮（调整布局：左侧预览+刷新，右侧执行重命名）-----
        action_frame = ctk.CTkFrame(main, fg_color="transparent")
        action_frame.pack(fill="x", padx=pad, pady=(0, 12))

        btn_style = {
            "width": 100,
            "height": 34,
            "corner_radius": 8,
            "font": FONT_SMALL_BOLD,
        }

        # 左侧按钮组（预览 + 刷新）
        left_btns = ctk.CTkFrame(action_frame, fg_color="transparent")
        left_btns.pack(side="left", fill="x", expand=True)

        self.preview_btn = ctk.CTkButton(
            left_btns,
            text="预览",
            **btn_style,
            fg_color=COLORS["warning"],
            hover_color="#E6A000",
            command=self.preview,
        )
        self.preview_btn.pack(side="left", padx=(0, 10))

        self.refresh_btn = ctk.CTkButton(
            left_btns,
            text="刷新",
            **btn_style,
            fg_color=COLORS["text_hint"],
            hover_color="#7A8794",
            command=self.preview,
        )
        self.refresh_btn.pack(side="left")

        # 右侧按钮（执行重命名）
        self.execute_btn = ctk.CTkButton(
            action_frame,
            text="执行重命名",
            **btn_style,
            fg_color=COLORS["success"],
            hover_color="#009A27",
            command=self.execute,
        )
        self.execute_btn.pack(side="right")

        # ----- 文件列表表格（ttk.Treeview）-----
        table_container = ctk.CTkFrame(
            main, fg_color=COLORS["bg_white"], corner_radius=10
        )
        table_container.pack(fill="both", expand=True, padx=pad, pady=(0, 12))

        tree_frame = tk.Frame(table_container, bg=COLORS["bg_white"])
        tree_frame.pack(fill="both", expand=True, padx=4, pady=4)

        columns = ("原文件名", "集数", "新文件名", "状态")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="tree headings", height=10
        )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=COLORS["bg_white"],
            foreground=COLORS["text_primary"],
            rowheight=34,
            font=FONT_SMALL,
            borderwidth=0,
            fieldbackground=COLORS["bg_white"],
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["bg_main"],
            foreground=COLORS["text_secondary"],
            font=FONT_MEDIUM_BOLD,
            borderwidth=0,
            relief="flat",
        )
        style.map("Treeview", background=[("selected", COLORS["primary"] + "33")])

        self.tree.heading("#0", text="")
        self.tree.heading("原文件名", text="文件")
        self.tree.heading("集数", text="集数")
        self.tree.heading("新文件名", text="新文件名")
        self.tree.heading("状态", text="状态")

        self.tree.column("#0", width=40, minwidth=40, stretch=False)
        self.tree.column("原文件名", width=200)
        self.tree.column("集数", width=70, anchor="center")
        self.tree.column("新文件名", width=300)
        self.tree.column("状态", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ----- 底部状态 -----
        status_frame = ctk.CTkFrame(main, fg_color="transparent")
        status_frame.pack(fill="x", padx=pad, pady=(0, 8))

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="💡 选择路径后自动识别模式，点击「预览」查看文件列表",
            font=FONT_SMALL,
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self.status_label.pack(fill="x")

        # ----- 查看结果按钮（底部）-----
        result_btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        result_btn_frame.pack(fill="x", padx=pad, pady=(0, pad))

        btn_res_style = {
            "width": 120,
            "height": 30,
            "corner_radius": 8,
            "font": FONT_SMALL_BOLD,
        }

        ctk.CTkButton(
            result_btn_frame,
            text="查看成功列表",
            **btn_res_style,
            fg_color=COLORS["success"],
            hover_color="#009A27",
            command=lambda: self._show_result_list("success"),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            result_btn_frame,
            text="查看失败列表",
            **btn_res_style,
            fg_color=COLORS["danger"],
            hover_color="#D93636",
            command=lambda: self._show_result_list("failed"),
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            result_btn_frame,
            text="查看全部完成",
            **btn_res_style,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=lambda: self._show_result_list("all_done"),
        ).pack(side="left")

    # ---------- 核心方法（保持不变） ----------
    def select_path(self):
        path = filedialog.askdirectory(title="选择文件夹或根目录")
        if path:
            self.selected_path = path
            self.path_display.configure(text=path, text_color=COLORS["text_secondary"])
            self.preview()

    def _analyze_path(self):
        if not self.selected_path:
            return None, {}

        has_mp4_direct = any(
            f.lower().endswith(".mp4")
            for f in os.listdir(self.selected_path)
            if os.path.isfile(os.path.join(self.selected_path, f))
        )

        if has_mp4_direct:
            drama_name = os.path.basename(self.selected_path)
            return "single", {self.selected_path: drama_name}
        else:
            subdirs = [
                os.path.join(self.selected_path, d)
                for d in os.listdir(self.selected_path)
                if os.path.isdir(os.path.join(self.selected_path, d))
            ]
            if not subdirs:
                return None, {}
            folder_map = {d: os.path.basename(d) for d in subdirs}
            return "batch", folder_map

    def preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.file_data.clear()
        self.folder_stats.clear()

        if not self.selected_path:
            messagebox.showwarning("提示", "请先选择路径！")
            return

        mode, folder_map = self._analyze_path()
        if mode is None:
            messagebox.showwarning("提示", "所选路径下没有找到任何子文件夹，请检查。")
            self.mode_label.configure(text="未找到文件夹", text_color=COLORS["danger"])
            return

        self.mode = mode
        if mode == "single":
            self.mode_label.configure(text="单剧目模式", text_color=COLORS["primary"])
        else:
            self.mode_label.configure(
                text=f"批量模式（{len(folder_map)} 个剧目）",
                text_color=COLORS["primary"],
            )

        for folder, drama_name in folder_map.items():
            if mode == "batch":
                folder_name = os.path.basename(folder)
                parent_iid = f"folder_{folder}"
                self.tree.insert(
                    "",
                    "end",
                    iid=parent_iid,
                    values=(folder_name, "", "", ""),
                    tags=("folder",),
                )
            else:
                parent_iid = ""

            for f in os.listdir(folder):
                if not f.lower().endswith(".mp4"):
                    continue

                match = re.search(r"\d+", f)
                if not match:
                    self.tree.insert(
                        parent_iid,
                        "end",
                        values=(f, "—", "跳过", "⏭️ 已跳过"),
                        tags=("file",),
                    )
                    self.file_data.append(
                        {
                            "folder": folder,
                            "old": f,
                            "num": None,
                            "new": None,
                            "exists": False,
                            "done": False,
                            "failed": False,
                            "skipped": True,
                        }
                    )
                    continue

                num = int(match.group())
                num_str = f"{num:02d}" if num < 10 else str(num)
                new_name = f"{drama_name} - 第{num_str}集.mp4"
                full_new_path = os.path.join(folder, new_name)
                exists = os.path.exists(full_new_path)

                status = "⚠️ 文件已存在" if exists else "✅ 待处理"
                self.tree.insert(
                    parent_iid,
                    "end",
                    values=(f, num_str, new_name, status),
                    tags=("file",),
                )
                self.file_data.append(
                    {
                        "folder": folder,
                        "old": f,
                        "num": num,
                        "new": new_name,
                        "exists": exists,
                        "done": False,
                        "failed": False,
                        "skipped": False,
                    }
                )

            if mode == "batch":
                total_files = sum(
                    1
                    for d in self.file_data
                    if d["folder"] == folder and not d.get("skipped", False)
                )
                self.tree.item(
                    parent_iid,
                    values=(os.path.basename(folder), "", f"{total_files} 个文件", ""),
                )

        self.update_stats()
        self.status_label.configure(
            text=f"✅ 预览完成：{len(folder_map)} 个剧目，共 {len(self.file_data)} 个文件",
            text_color=COLORS["success"],
        )

    def update_stats(self):
        total = len(self.file_data)
        done = sum(1 for d in self.file_data if d.get("done", False))
        failed = sum(1 for d in self.file_data if d.get("failed", False))
        skipped = sum(1 for d in self.file_data if d.get("skipped", False))
        pending = total - done - failed - skipped

        self.stat_cards["📄 总文件"].set_value(total)
        self.stat_cards["⏳ 待处理"].set_value(pending)
        self.stat_cards["✅ 已完成"].set_value(done)
        self.stat_cards["❌ 失败"].set_value(failed)

    def execute(self):
        if not self.file_data:
            messagebox.showwarning("提示", "请先预览！")
            return

        pending = [
            d
            for d in self.file_data
            if not d.get("skipped", False) and not d.get("done", False)
        ]
        if not pending:
            messagebox.showinfo("提示", "没有待处理的文件！")
            return

        has_conflict = any(d.get("exists", False) for d in pending)
        if has_conflict and not messagebox.askyesno(
            "确认覆盖", "部分文件已存在，是否覆盖？"
        ):
            return

        folder_groups = {}
        for d in pending:
            folder_groups.setdefault(d["folder"], []).append(d)

        success = 0
        fail = 0

        for folder, files in folder_groups.items():
            for data in files:
                old_path = os.path.join(folder, data["old"])
                new_path = os.path.join(folder, data["new"])
                try:
                    if data.get("exists", False) and os.path.exists(new_path):
                        os.remove(new_path)
                    os.rename(old_path, new_path)
                    data["done"] = True
                    data["exists"] = False
                    success += 1
                    self._update_tree_status(data["old"], folder, "✅ 已完成")
                except Exception as e:
                    data["failed"] = True
                    fail += 1
                    self._update_tree_status(data["old"], folder, f"❌ {str(e)[:20]}")

        self.update_stats()
        messagebox.showinfo("完成", f"成功：{success} 个，失败：{fail} 个")
        self.status_label.configure(
            text=f"✅ 完成：成功 {success} 个，失败 {fail} 个",
            text_color=COLORS["success"] if fail == 0 else COLORS["warning"],
        )

    def _update_tree_status(self, old_filename, folder, new_status):
        parent_iid = ""
        for item in self.tree.get_children():
            tags = self.tree.item(item, "tags")
            if "folder" in tags:
                if item == f"folder_{folder}":
                    parent_iid = item
                    break
        children = (
            self.tree.get_children(parent_iid)
            if parent_iid
            else self.tree.get_children()
        )
        for child in children:
            vals = self.tree.item(child, "values")
            if vals[0] == old_filename:
                vals = list(vals)
                vals[3] = new_status
                self.tree.item(child, values=tuple(vals))
                break

    # ---------- 查看结果列表 ----------
    def _show_result_list(self, filter_type):
        if filter_type == "total":
            items = self.file_data
            title = "📄 全部文件"
        elif filter_type == "pending":
            items = [
                d
                for d in self.file_data
                if not d.get("done", False)
                and not d.get("failed", False)
                and not d.get("skipped", False)
            ]
            title = "⏳ 待处理文件"
        elif filter_type == "done" or filter_type == "success":
            items = [
                d
                for d in self.file_data
                if d.get("done", False) and not d.get("failed", False)
            ]
            title = "✅ 已完成文件"
        elif filter_type == "failed":
            items = [d for d in self.file_data if d.get("failed", False)]
            title = "❌ 失败文件"
        elif filter_type == "all_done":
            items = [
                d
                for d in self.file_data
                if d.get("done", False) or d.get("failed", False)
            ]
            title = "📋 全部完成列表"
        else:
            return

        if not items:
            messagebox.showinfo("提示", f"没有 {title} 记录。")
            return

        win = ctk.CTkToplevel(self.window)
        win.title(title)
        win.geometry("850x450")
        win.minsize(700, 300)
        win.transient(self.window)
        win.focus_force()
        win.grab_set()

        main_frame = ctk.CTkFrame(win, fg_color=COLORS["bg_white"], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            main_frame,
            text=title,
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(pady=(10, 5))

        tree_frame = tk.Frame(main_frame, bg=COLORS["bg_white"])
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("原文件名", "新文件名", "状态")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        tree.heading("原文件名", text="原文件名")
        tree.heading("新文件名", text="新文件名")
        tree.heading("状态", text="状态")
        tree.column("原文件名", width=280)
        tree.column("新文件名", width=350)
        tree.column("状态", width=120, anchor="center")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Result.Treeview",
            background=COLORS["bg_white"],
            foreground=COLORS["text_primary"],
            rowheight=30,
            font=FONT_SMALL,
            borderwidth=0,
            fieldbackground=COLORS["bg_white"],
        )
        style.configure(
            "Result.Treeview.Heading",
            background=COLORS["bg_main"],
            foreground=COLORS["text_secondary"],
            font=FONT_MEDIUM_BOLD,
            borderwidth=0,
            relief="flat",
        )
        tree.configure(style="Result.Treeview")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for d in items:
            if d.get("done", False) and not d.get("failed", False):
                status_text = "✅ 成功"
            elif d.get("failed", False):
                status_text = "❌ 失败"
            elif d.get("skipped", False):
                status_text = "⏭️ 跳过"
            else:
                status_text = "⏳ 待处理"
            tree.insert(
                "",
                "end",
                values=(d["old"], d["new"] if d.get("new") else "-", status_text),
            )

        ctk.CTkButton(
            main_frame,
            text="关闭",
            command=win.destroy,
            width=100,
            height=32,
            corner_radius=8,
            font=FONT_SMALL_BOLD,
            fg_color=COLORS["text_hint"],
            hover_color="#7A8794",
        ).pack(pady=10)
