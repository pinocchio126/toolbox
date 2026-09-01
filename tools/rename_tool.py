import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from config import (
    COLORS,
    FONT_LARGE_BOLD,
    FONT_MEDIUM,
    FONT_MEDIUM_BOLD,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    FONT_XLARGE_BOLD,
)
from components import BaseToolWindow, StatCard


class RenameTool(BaseToolWindow):
    def __init__(self, parent):
        super().__init__(
            parent,
            "批量重命名",
            "选择剧集目录，自动识别单剧或多剧目录并生成重命名预览",
        )
        self.selected_path = None
        self.mode = None
        self.file_data = []
        self.stat_cards = {}

    def setup_ui(self):
        main = self.window
        pad = 20

        header = ctk.CTkFrame(main, fg_color=COLORS["bg_white"], corner_radius=10)
        header.pack(fill="x", padx=pad, pady=(pad, 0))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            title_frame,
            text="📁 批量重命名",
            font=FONT_XLARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_frame,
            text=self.subtitle,
            font=FONT_MEDIUM,
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(6, 0))

        stats_frame = ctk.CTkFrame(main, fg_color="transparent")
        stats_frame.pack(fill="x", padx=pad, pady=pad)

        stat_configs = [
            ("总文件", COLORS["text_secondary"], "total"),
            ("待处理", COLORS["warning"], "pending"),
            ("已完成", COLORS["success"], "done"),
            ("失败", COLORS["danger"], "failed"),
        ]
        for label, color, filter_type in stat_configs:
            card = StatCard(
                stats_frame,
                label,
                color=color,
                command=lambda current_filter=filter_type: self._show_result_list(current_filter),
            )
            card.pack(side="left", padx=(0, 12), fill="x", expand=True)
            self.stat_cards[filter_type] = card

        settings_frame = ctk.CTkFrame(main, fg_color=COLORS["bg_white"], corner_radius=10)
        settings_frame.pack(fill="x", padx=pad, pady=(0, pad))

        settings_inner = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(
            settings_inner,
            text="目标路径",
            font=FONT_MEDIUM_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        self.path_display = ctk.CTkLabel(
            settings_inner,
            text="未选择",
            font=FONT_MEDIUM,
            text_color=COLORS["text_hint"],
        )
        self.path_display.pack(side="left", padx=(12, 12), fill="x", expand=True, anchor="w")

        ctk.CTkButton(
            settings_inner,
            text="选择路径",
            width=110,
            height=34,
            corner_radius=8,
            font=FONT_SMALL_BOLD,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self.select_path,
        ).pack(side="right")

        self.mode_label = ctk.CTkLabel(
            settings_inner,
            text="",
            font=FONT_MEDIUM_BOLD,
            text_color=COLORS["primary"],
        )
        self.mode_label.pack(side="right", padx=(0, 16))

        action_frame = ctk.CTkFrame(main, fg_color="transparent")
        action_frame.pack(fill="x", padx=pad, pady=(0, 12))

        button_style = {
            "width": 108,
            "height": 34,
            "corner_radius": 8,
            "font": FONT_SMALL_BOLD,
        }

        ctk.CTkButton(
            action_frame,
            text="预览",
            **button_style,
            fg_color=COLORS["warning"],
            hover_color="#D97706",
            command=self.preview,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            action_frame,
            text="刷新",
            **button_style,
            fg_color=COLORS["text_hint"],
            hover_color="#64748B",
            command=self.preview,
        ).pack(side="left")

        ctk.CTkButton(
            action_frame,
            text="执行重命名",
            **button_style,
            fg_color=COLORS["success"],
            hover_color="#15803D",
            command=self.execute,
        ).pack(side="right")

        self._build_table(main, pad)

        self.status_label = ctk.CTkLabel(
            main,
            text="选择路径后会自动分析目录，点击预览查看即将处理的文件。",
            font=FONT_SMALL,
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=pad, pady=(0, 12))

        result_frame = ctk.CTkFrame(main, fg_color="transparent")
        result_frame.pack(fill="x", padx=pad, pady=(0, pad))

        for text, color, filter_type in [
            ("查看成功", COLORS["success"], "done"),
            ("查看失败", COLORS["danger"], "failed"),
            ("查看全部结果", COLORS["primary"], "all_done"),
        ]:
            ctk.CTkButton(
                result_frame,
                text=text,
                width=120,
                height=30,
                corner_radius=8,
                font=FONT_SMALL_BOLD,
                fg_color=color,
                hover_color=COLORS["primary_hover"] if color == COLORS["primary"] else color,
                command=lambda current_filter=filter_type: self._show_result_list(current_filter),
            ).pack(side="left", padx=(0, 10))

    def _build_table(self, main, pad):
        table_container = ctk.CTkFrame(main, fg_color=COLORS["bg_white"], corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=pad, pady=(0, 12))

        tree_frame = tk.Frame(table_container, bg=COLORS["bg_white"])
        tree_frame.pack(fill="both", expand=True, padx=6, pady=6)

        columns = ("old", "episode", "new", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", height=10)

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
        style.map("Treeview", background=[("selected", "#DBEAFE")])

        headings = {
            "#0": "",
            "old": "原文件名",
            "episode": "集数",
            "new": "新文件名",
            "status": "状态",
        }
        for column, text in headings.items():
            self.tree.heading(column, text=text)

        self.tree.column("#0", width=36, minwidth=36, stretch=False)
        self.tree.column("old", width=260)
        self.tree.column("episode", width=70, anchor="center")
        self.tree.column("new", width=360)
        self.tree.column("status", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_path(self):
        path = filedialog.askdirectory(title="选择文件夹或根目录")
        if path:
            self.selected_path = path
            self.path_display.configure(text=path, text_color=COLORS["text_secondary"])
            self.preview()

    def _analyze_path(self):
        if not self.selected_path or not os.path.isdir(self.selected_path):
            return None, {}

        direct_files = [
            filename
            for filename in os.listdir(self.selected_path)
            if os.path.isfile(os.path.join(self.selected_path, filename))
        ]
        has_video_directly = any(self._is_video(filename) for filename in direct_files)
        if has_video_directly:
            return "single", {self.selected_path: os.path.basename(self.selected_path)}

        folders = [
            os.path.join(self.selected_path, name)
            for name in os.listdir(self.selected_path)
            if os.path.isdir(os.path.join(self.selected_path, name))
        ]
        folder_map = {folder: os.path.basename(folder) for folder in folders}
        return ("batch", folder_map) if folder_map else (None, {})

    def preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.file_data.clear()

        if not self.selected_path:
            messagebox.showwarning("提示", "请先选择路径。")
            return

        mode, folder_map = self._analyze_path()
        if mode is None:
            self.mode_label.configure(text="未找到视频文件", text_color=COLORS["danger"])
            self.update_stats()
            messagebox.showwarning("提示", "所选路径下没有找到可处理的视频文件。")
            return

        self.mode = mode
        mode_text = "单剧目录" if mode == "single" else f"批量目录：{len(folder_map)} 个剧目"
        self.mode_label.configure(text=mode_text, text_color=COLORS["primary"])

        for folder, drama_name in folder_map.items():
            parent_iid = ""
            if mode == "batch":
                parent_iid = f"folder_{folder}"
                self.tree.insert(
                    "",
                    "end",
                    iid=parent_iid,
                    values=(os.path.basename(folder), "", "", ""),
                    tags=("folder",),
                )

            folder_count = 0
            for filename in sorted(os.listdir(folder), key=self._natural_key):
                if not self._is_video(filename):
                    continue

                folder_count += 1
                match = re.search(r"\d+", filename)
                if not match:
                    self._append_file_row(parent_iid, folder, filename, None, None, "跳过：未识别集数")
                    continue

                episode = int(match.group())
                new_name = f"{drama_name} - 第{episode}集.mp4"
                target_path = os.path.join(folder, new_name)
                status = "跳过：目标已存在" if os.path.exists(target_path) else "待处理"
                self._append_file_row(parent_iid, folder, filename, episode, new_name, status)

            if mode == "batch":
                self.tree.item(parent_iid, values=(os.path.basename(folder), "", f"{folder_count} 个视频", ""))

        self.update_stats()
        self.status_label.configure(
            text=f"预览完成：{len(folder_map)} 个目录，{len(self.file_data)} 个视频文件。",
            text_color=COLORS["success"],
        )

    def _append_file_row(self, parent_iid, folder, old_name, episode, new_name, status):
        skipped = status.startswith("跳过")
        exists = status == "跳过：目标已存在"
        self.tree.insert(
            parent_iid,
            "end",
            values=(old_name, episode if episode is not None else "-", new_name or "-", status),
            tags=("file",),
        )
        self.file_data.append(
            {
                "folder": folder,
                "old": old_name,
                "num": episode,
                "new": new_name,
                "exists": exists,
                "done": False,
                "failed": False,
                "skipped": skipped,
                "status": status,
            }
        )

    def execute(self):
        if not self.file_data:
            messagebox.showwarning("提示", "请先预览文件列表。")
            return

        pending = [
            item
            for item in self.file_data
            if not item["skipped"] and not item["done"] and not item["failed"]
        ]
        if not pending:
            messagebox.showinfo("提示", "没有待处理的文件。")
            return

        success = 0
        failed = 0
        skipped = 0

        for item in pending:
            old_path = os.path.join(item["folder"], item["old"])
            new_path = os.path.join(item["folder"], item["new"])

            if not os.path.exists(old_path):
                item["failed"] = True
                item["status"] = "失败：源文件不存在"
                failed += 1
                self._update_tree_status(item, item["status"])
                continue

            if os.path.exists(new_path):
                item["done"] = True
                item["status"] = "已存在：跳过"
                skipped += 1
                self._update_tree_status(item, item["status"])
                continue

            try:
                os.rename(old_path, new_path)
                item["done"] = True
                item["status"] = "已完成"
                success += 1
            except OSError as error:
                item["failed"] = True
                item["error"] = str(error)
                item["status"] = f"失败：{str(error)[:24]}"
                failed += 1
            self._update_tree_status(item, item["status"])

        self.update_stats()
        self.status_label.configure(
            text=f"执行完成：成功 {success} 个，失败 {failed} 个，跳过 {skipped} 个。",
            text_color=COLORS["success"] if failed == 0 else COLORS["warning"],
        )
        messagebox.showinfo(
            "完成",
            f"成功：{success} 个\n失败：{failed} 个\n跳过：{skipped} 个",
        )

    def update_stats(self):
        total = len(self.file_data)
        done = sum(1 for item in self.file_data if item["done"])
        failed = sum(1 for item in self.file_data if item["failed"])
        skipped = sum(1 for item in self.file_data if item["skipped"])
        pending = total - done - failed - skipped

        self.stat_cards["total"].set_value(total)
        self.stat_cards["pending"].set_value(max(pending, 0))
        self.stat_cards["done"].set_value(done)
        self.stat_cards["failed"].set_value(failed)

    def _update_tree_status(self, item, status):
        parent_iid = ""
        for node in self.tree.get_children():
            if node == f"folder_{item['folder']}":
                parent_iid = node
                break

        children = self.tree.get_children(parent_iid) if parent_iid else self.tree.get_children()
        for child in children:
            values = list(self.tree.item(child, "values"))
            if values and values[0] == item["old"]:
                values[3] = status
                self.tree.item(child, values=tuple(values))
                break

    def _show_result_list(self, filter_type):
        items, title = self._filter_items(filter_type)
        if not items:
            messagebox.showinfo("提示", f"没有{title}记录。")
            return

        win = ctk.CTkToplevel(self.window)
        win.title(title)
        win.geometry("860x460")
        win.minsize(720, 320)
        win.transient(self.window)
        win.focus_force()
        win.grab_set()

        main_frame = ctk.CTkFrame(win, fg_color=COLORS["bg_white"], corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            main_frame,
            text=title,
            font=FONT_LARGE_BOLD,
            text_color=COLORS["text_primary"],
        ).pack(pady=(12, 6))

        tree_frame = tk.Frame(main_frame, bg=COLORS["bg_white"])
        tree_frame.pack(fill="both", expand=True, padx=8, pady=8)

        columns = ("old", "new", "status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=14)
        for column, text in {"old": "原文件名", "new": "新文件名", "status": "状态"}.items():
            tree.heading(column, text=text)
        tree.column("old", width=300)
        tree.column("new", width=360)
        tree.column("status", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in items:
            tree.insert("", "end", values=(item["old"], item["new"] or "-", item["status"]))

        ctk.CTkButton(
            main_frame,
            text="关闭",
            command=win.destroy,
            width=100,
            height=32,
            corner_radius=8,
            font=FONT_SMALL_BOLD,
            fg_color=COLORS["text_hint"],
            hover_color="#64748B",
        ).pack(pady=(0, 12))

    def _filter_items(self, filter_type):
        if filter_type == "total":
            return self.file_data, "全部文件"
        if filter_type == "pending":
            return [
                item
                for item in self.file_data
                if not item["done"] and not item["failed"] and not item["skipped"]
            ], "待处理文件"
        if filter_type == "done":
            return [item for item in self.file_data if item["done"] and not item["failed"]], "已完成文件"
        if filter_type == "failed":
            return [item for item in self.file_data if item["failed"]], "失败文件"
        if filter_type == "all_done":
            return [item for item in self.file_data if item["done"] or item["failed"]], "全部结果"
        return [], ""

    @staticmethod
    def _is_video(filename):
        return filename.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".m4v"))

    @staticmethod
    def _natural_key(value):
        return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]
