import glob
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import SUBJECTS_DIR, DEFAULT_FORMAT, DEFAULT_THEME, DEFAULT_STYLE
from core.knowledge import load_knowledge
from core.renderer import render_html
from core.runner import run_mode_b
from core.format_manager import discover_formats, load_prompt
from core.theme import list_themes
from core.decorations import list_styles
from core.ai import load_config, save_config, test_connection, generate_json

PRESET_SUBJECTS = ["历史", "地理", "生物", "语文", "政治"]

# ── Color palette ──────────────────────────────────────────
C = {
    "bg":       "#F0F2F5",
    "card":     "#FFFFFF",
    "primary":  "#4A7DCA",
    "primary_h":"#3B6AB5",
    "accent":   "#5B9BD5",
    "border":   "#D0D5DD",
    "text":     "#1A1A2E",
    "text2":    "#4A4A6A",
    "muted":    "#8E8EA0",
    "input_bg": "#FAFBFC",
    "success":  "#2E8B57",
    "error":    "#C0392B",
    "tab_bg":   "#E8ECF1",
    "tab_sel":  "#FFFFFF",
}


def scan_json_files():
    result = {}
    pattern = os.path.join(SUBJECTS_DIR, "*", "*.json")
    for path in sorted(glob.glob(pattern)):
        subject = os.path.basename(os.path.dirname(path))
        topic = os.path.splitext(os.path.basename(path))[0]
        label = f"{subject}/{topic}"
        result[label] = path
    return result


class SubjectDrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SubjectDraw")
        self.root.geometry("620x700")
        self.root.resizable(False, False)
        self.root.configure(bg=C["bg"])

        self._apply_styles()

        self.status_var = tk.StringVar(value="就绪")

        # ── Notebook ────────────────────────────────────
        style = ttk.Style()
        style.configure("TNotebook", background=C["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=C["tab_bg"], foreground=C["text2"],
                        padding=[16, 6], font=("Microsoft YaHei UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", C["tab_sel"])],
                  foreground=[("selected", C["primary"])])

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        self.notebook = notebook

        self.tab_a = ttk.Frame(notebook, style="TFrame")
        self.tab_b = ttk.Frame(notebook, style="TFrame")
        notebook.add(self.tab_a, text="  生成提示词  ")
        notebook.add(self.tab_b, text="  生成预览  ")

        self._build_tab_a(self.tab_a)
        self._build_tab_b(self.tab_b)

        # ── Status bar ──────────────────────────────────
        status = tk.Label(
            self.root, textvariable=self.status_var,
            anchor="w", bg=C["card"], fg=C["muted"],
            font=("Microsoft YaHei UI", 9),
            padx=10, pady=4,
            borderwidth=0, highlightthickness=1,
            highlightbackground=C["border"], highlightcolor=C["border"],
        )
        status.pack(fill="x", side="bottom")

    # ── Styles ──────────────────────────────────────────
    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure(".", background=C["bg"], foreground=C["text"],
                     font=("Microsoft YaHei UI", 10))
        s.configure("TFrame", background=C["bg"])
        s.configure("Card.TFrame", background=C["card"])

        s.configure("TLabel", background=C["bg"], foreground=C["text"],
                     font=("Microsoft YaHei UI", 10))
        s.configure("Card.TLabel", background=C["card"], foreground=C["text"])
        s.configure("Title.TLabel", background=C["card"], foreground=C["primary"],
                     font=("Microsoft YaHei UI", 13, "bold"))
        s.configure("Section.TLabel", background=C["card"], foreground=C["text2"],
                     font=("Microsoft YaHei UI", 9))
        s.configure("Status.TLabel", background=C["card"], foreground=C["success"],
                     font=("Microsoft YaHei UI", 9))

        s.configure("TEntry",
                     fieldbackground=C["input_bg"], foreground=C["text"],
                     borderwidth=1, relief="solid",
                     padding=[6, 4])
        s.map("TEntry",
              bordercolor=[("focus", C["primary"])],
              relief=[("focus", "solid")])

        s.configure("TCombobox",
                     fieldbackground=C["input_bg"], foreground=C["text"],
                     borderwidth=1, relief="solid",
                     padding=[6, 4])
        s.map("TCombobox",
              bordercolor=[("focus", C["primary"])])

        s.configure("Primary.TButton",
                     background=C["primary"], foreground="#FFFFFF",
                     borderwidth=0, padding=[16, 8],
                     font=("Microsoft YaHei UI", 10, "bold"))
        s.map("Primary.TButton",
              background=[("active", C["primary_h"]), ("pressed", C["primary_h"])])

        s.configure("Secondary.TButton",
                     background=C["card"], foreground=C["primary"],
                     borderwidth=1, relief="solid",
                     padding=[12, 6],
                     font=("Microsoft YaHei UI", 9))
        s.map("Secondary.TButton",
              background=[("active", C["bg"])])

        s.configure("TLabelframe", background=C["card"], foreground=C["text2"],
                     borderwidth=1, relief="solid",
                     bordercolor=C["border"])
        s.configure("TLabelframe.Label", background=C["card"], foreground=C["text2"],
                     font=("Microsoft YaHei UI", 9, "bold"))

        s.configure("Horizontal.TScrollbar",
                     background=C["border"], troughcolor=C["bg"],
                     borderwidth=0, arrowsize=0)

    # ── Helpers ─────────────────────────────────────────
    def _card(self, parent, **kw) -> tk.Frame:
        """White rounded card container."""
        f = tk.Frame(parent, bg=C["card"], highlightthickness=1,
                     highlightbackground=C["border"], highlightcolor=C["border"],
                     **kw)
        return f

    def _section_label(self, parent, text) -> ttk.Label:
        return ttk.Label(parent, text=text, style="Section.TLabel")

    def _input(self, parent, variable, width=20, **kw) -> ttk.Entry:
        e = ttk.Entry(parent, textvariable=variable, width=width, **kw)
        return e

    def _combo(self, parent, variable, values, width=18) -> ttk.Combobox:
        return ttk.Combobox(parent, textvariable=variable,
                            values=values, width=width, state="readonly")

    # ── Tab A: Prompt ───────────────────────────────────
    def _build_tab_a(self, parent):
        outer = tk.Frame(parent, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=12, pady=12)

        card = self._card(outer)
        card.pack(fill="x")

        inner = ttk.Frame(card, style="Card.TFrame", padding=16)
        inner.pack(fill="x")

        ttk.Label(inner, text="生成提示词", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        available_formats = discover_formats() or [DEFAULT_FORMAT]

        self._section_label(inner, "格式").grid(
            row=1, column=0, sticky="w", pady=(0, 2))
        self.format_a_var = tk.StringVar(
            value=DEFAULT_FORMAT if DEFAULT_FORMAT in available_formats else available_formats[0])
        self._combo(inner, self.format_a_var, available_formats, 22).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self._section_label(inner, "学科").grid(
            row=3, column=0, sticky="w", pady=(0, 2))
        self.subject_var = tk.StringVar(value=PRESET_SUBJECTS[0])
        self._combo(inner, self.subject_var, PRESET_SUBJECTS, 22).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        self._section_label(inner, "主题").grid(
            row=5, column=0, sticky="w", pady=(0, 2))
        self.topic_var = tk.StringVar()
        topic_e = self._input(inner, self.topic_var, 24)
        topic_e.insert(0, "如 辛亥革命、光合作用")
        topic_e.config(foreground="gray")
        topic_e.bind("<FocusIn>", self._on_topic_focus_in)
        topic_e.bind("<FocusOut>", self._on_topic_focus_out)
        topic_e.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 4))

        inner.columnconfigure(0, weight=1)

        btn_frame = ttk.Frame(inner, style="Card.TFrame")
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="e", pady=(12, 0))

        ttk.Button(btn_frame, text="AI 设置", style="Secondary.TButton",
                   command=self.open_settings).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="AI 生成", style="Primary.TButton",
                   command=self.on_ai_generate).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="生成提示词", style="Primary.TButton",
                   command=self.on_generate_prompt).pack(side="left")

        # Prompt text area
        text_card = self._card(outer)
        text_card.pack(fill="both", expand=True, pady=(10, 0))

        text_inner = tk.Frame(text_card, bg=C["card"])
        text_inner.pack(fill="both", expand=True, padx=12, pady=12)

        self.prompt_text = tk.Text(
            text_inner, wrap="word", state="disabled",
            bg=C["input_bg"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            borderwidth=0, highlightthickness=1,
            highlightbackground=C["border"], highlightcolor=C["primary"],
            padx=8, pady=8)
        scrollbar = ttk.Scrollbar(text_inner, command=self.prompt_text.yview)
        self.prompt_text.configure(yscrollcommand=scrollbar.set)
        self.prompt_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_topic_focus_in(self, event):
        if self.topic_var.get() == "如 辛亥革命、光合作用":
            self.topic_var.set("")
            event.widget.config(foreground="black")

    def _on_topic_focus_out(self, event):
        if not self.topic_var.get().strip():
            self.topic_var.set("如 辛亥革命、光合作用")
            event.widget.config(foreground="gray")

    # ── Settings Dialog ────────────────────────────────
    def open_settings(self):
        cfg = load_config()

        dlg = tk.Toplevel(self.root)
        dlg.title("API 设置")
        dlg.geometry("480x340")
        dlg.resizable(False, False)
        dlg.configure(bg=C["bg"])
        dlg.transient(self.root)
        dlg.grab_set()

        card = self._card(dlg)
        card.pack(fill="both", expand=True, padx=12, pady=12)

        inner = ttk.Frame(card, style="Card.TFrame", padding=16)
        inner.pack(fill="x")

        ttk.Label(inner, text="API 设置", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        fields = [
            (1, "接口地址：", "endpoint"),
            (2, "API Key：", "key"),
            (3, "模型：", "model"),
            (4, "Temperature：", "temperature"),
            (5, "Max Tokens：", "max_tokens"),
        ]
        vars_ = {}
        for row, label, key in fields:
            self._section_label(inner, label).grid(
                row=row, column=0, sticky="w", pady=3)
            var = tk.StringVar(value=str(cfg.get(key, "")))
            vars_[key] = var
            w = 30 if key == "endpoint" else 24
            ttk.Entry(inner, textvariable=var, width=w).grid(
                row=row, column=1, sticky="ew", pady=3)

        inner.columnconfigure(1, weight=1)

        preset_frame = ttk.Frame(inner, style="Card.TFrame")
        preset_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Label(preset_frame, text="快捷填充：", style="Section.TLabel").pack(side="left")

        def fill_ollama():
            vars_["endpoint"].set("http://localhost:11434/v1/chat/completions")
            vars_["key"].set("ollama")
            vars_["model"].set("qwen2.5-coder:7b")

        def fill_openai():
            vars_["endpoint"].set("https://api.openai.com/v1/chat/completions")
            vars_["key"].set("")
            vars_["model"].set("gpt-4o-mini")

        ttk.Button(preset_frame, text="Ollama", style="Secondary.TButton",
                   command=fill_ollama).pack(side="left", padx=(0, 6))
        ttk.Button(preset_frame, text="OpenAI", style="Secondary.TButton",
                   command=fill_openai).pack(side="left")

        btn_frame = ttk.Frame(inner, style="Card.TFrame")
        btn_frame.grid(row=7, column=0, columnspan=2, sticky="e", pady=(12, 0))

        status_label = ttk.Label(inner, text="", style="Card.TLabel")
        status_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(6, 0))

        def on_test():
            status_label.config(text="测试连接中...", foreground=C["text2"])
            dlg.update_idletasks()
            test_cfg = dict(DEFAULT_CONFIG)
            for k, v in vars_.items():
                test_cfg[k] = v.get()
            try:
                test_cfg["temperature"] = float(test_cfg["temperature"])
                test_cfg["max_tokens"] = int(test_cfg["max_tokens"])
            except ValueError:
                pass
            try:
                test_connection(test_cfg)
                status_label.config(text="连接成功", foreground=C["success"])
            except Exception as e:
                status_label.config(text=f"失败: {e}", foreground=C["error"])

        def on_save():
            new_cfg = dict(DEFAULT_CONFIG)
            for k, v in vars_.items():
                val = v.get()
                if k == "temperature":
                    try:
                        val = float(val)
                    except ValueError:
                        val = 0.3
                elif k == "max_tokens":
                    try:
                        val = int(val)
                    except ValueError:
                        val = 4096
                new_cfg[k] = val
            save_config(new_cfg)
            status_label.config(text="已保存", foreground=C["success"])
            dlg.after(600, dlg.destroy)

        ttk.Button(btn_frame, text="测试连接", style="Secondary.TButton",
                   command=on_test).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="保存", style="Primary.TButton",
                   command=on_save).pack(side="left")

    # ── AI Generate ────────────────────────────────────
    def on_ai_generate(self):
        subject = self.subject_var.get().strip()
        topic = self.topic_var.get().strip()
        fmt = self.format_a_var.get().strip()

        if not subject or not topic or topic == "如 辛亥革命、光合作用":
            self.status_var.set("请填写学科和主题")
            return

        cfg = load_config()
        if not cfg.get("key"):
            self.status_var.set("请先在 API 设置中配置 Key")
            self.open_settings()
            return

        self.status_var.set("AI 生成中，请稍候...")
        self.root.update_idletasks()

        try:
            data = generate_json(subject, topic, fmt, cfg)
        except Exception as e:
            self.status_var.set(f"AI 生成失败: {e}")
            return

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", "end")
        self.prompt_text.insert("1.0", json_str)
        self.prompt_text.configure(state="disabled")

        self.json_text.delete("1.0", "end")
        self.json_text.insert("1.0", json_str)

        self.notebook.select(1)
        self.status_var.set(f"AI 已生成 {subject}/{topic}，已填入编辑器")

    def on_generate_prompt(self):
        subject = self.subject_var.get().strip()
        topic = self.topic_var.get().strip()
        fmt = self.format_a_var.get().strip()

        if not subject or not topic or topic == "如 辛亥革命、光合作用":
            self.status_var.set("请填写学科和主题")
            return

        try:
            text = load_prompt(fmt, subject, topic)
        except Exception as e:
            self.status_var.set(f"错误: {e}")
            return

        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", "end")
        self.prompt_text.insert("1.0", text)
        self.prompt_text.configure(state="disabled")

        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("已生成提示词，已复制到剪贴板")

    # ── Tab B: Preview ──────────────────────────────────
    def _build_tab_b(self, parent):
        outer = tk.Frame(parent, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=12, pady=12)

        # ── Top card: file selection + settings ─────────
        card = self._card(outer)
        card.pack(fill="x")

        inner = ttk.Frame(card, style="Card.TFrame", padding=16)
        inner.pack(fill="x")

        ttk.Label(inner, text="生成预览", style="Title.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        available_formats = discover_formats() or [DEFAULT_FORMAT]

        # Row: format
        self._section_label(inner, "格式").grid(
            row=1, column=0, sticky="w", pady=(0, 2))
        self.format_b_var = tk.StringVar(
            value=DEFAULT_FORMAT if DEFAULT_FORMAT in available_formats else available_formats[0])
        self._combo(inner, self.format_b_var, available_formats, 18).grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=(0, 12), pady=(0, 10))

        # Row: JSON file
        self._section_label(inner, "JSON 文件").grid(
            row=1, column=2, sticky="w", pady=(0, 2))
        self.json_map = scan_json_files()
        self.json_choice_var = tk.StringVar()
        self.json_combo = ttk.Combobox(
            inner, textvariable=self.json_choice_var,
            values=list(self.json_map.keys()), width=18, state="readonly")
        self.json_combo.grid(row=2, column=2, sticky="ew", padx=(0, 4), pady=(0, 10))
        self.json_combo.bind("<<ComboboxSelected>>", self.on_select_json)

        browse_btn = ttk.Button(inner, text="浏览", style="Secondary.TButton",
                                command=self.on_browse_json)
        browse_btn.grid(row=2, column=3, sticky="w", pady=(0, 10))

        inner.columnconfigure(0, weight=0)
        inner.columnconfigure(2, weight=1)

        # ── Settings panel ─────────────────────────────
        settings = ttk.LabelFrame(inner, text=" 页面设置 ", padding=10)
        settings.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(4, 0))
        settings.columnconfigure(1, weight=1)
        settings.columnconfigure(3, weight=1)

        fields = [
            (0, "姓名：", "name_var"),
            (0, "班级：", "cls_var", 2),
            (1, "学号：", "sid_var"),
            (1, "日期：", "date_var", 2),
        ]
        for item in fields:
            row, label, var_name = item[0], item[1], item[2]
            col = item[3] if len(item) > 3 else 0
            self._section_label(settings, label).grid(
                row=row, column=col, sticky="w", padx=(0, 4), pady=3)
            setattr(self, var_name, tk.StringVar())
            self._input(settings, getattr(self, var_name), 14).grid(
                row=row, column=col + 1, sticky="ew", padx=(0, 12), pady=3)

        self._section_label(settings, "色彩主题：").grid(
            row=2, column=0, sticky="w", padx=(0, 4), pady=3)
        self.theme_var = tk.StringVar(value=DEFAULT_THEME)
        self._combo(settings, self.theme_var, list_themes(), 14).grid(
            row=2, column=1, sticky="ew", padx=(0, 12), pady=3)

        self._section_label(settings, "装饰风格：").grid(
            row=2, column=2, sticky="w", padx=(0, 4), pady=3)
        self.style_var = tk.StringVar(value=DEFAULT_STYLE)
        self._combo(settings, self.style_var, list_styles(), 14).grid(
            row=2, column=3, sticky="ew", pady=3)

        self._section_label(settings, "水印文字：").grid(
            row=3, column=0, sticky="w", padx=(0, 4), pady=3)
        self.watermark_var = tk.StringVar()
        self._input(settings, self.watermark_var, 14).grid(
            row=3, column=1, sticky="ew", padx=(0, 12), pady=3)

        # ── JSON editor card ───────────────────────────
        edit_card = self._card(outer)
        edit_card.pack(fill="both", expand=True, pady=(10, 0))

        edit_inner = tk.Frame(edit_card, bg=C["card"])
        edit_inner.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        ttk.Label(edit_inner, text="JSON 内容（可编辑）",
                  style="Section.TLabel").pack(anchor="w", pady=(0, 4))

        text_container = tk.Frame(edit_inner, bg=C["card"])
        text_container.pack(fill="both", expand=True)

        self.json_text = tk.Text(
            text_container, wrap="none",
            bg=C["input_bg"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            borderwidth=0, highlightthickness=1,
            highlightbackground=C["border"], highlightcolor=C["primary"],
            padx=8, pady=8)
        json_scroll = ttk.Scrollbar(text_container, command=self.json_text.yview)
        self.json_text.configure(yscrollcommand=json_scroll.set)
        self.json_text.pack(side="left", fill="both", expand=True)
        json_scroll.pack(side="right", fill="y")

        ttk.Button(edit_inner, text="生成预览", style="Primary.TButton",
                   command=self.on_generate_preview).pack(anchor="e", pady=(8, 0))

    def on_select_json(self, event=None):
        label = self.json_choice_var.get()
        path = self.json_map.get(label)
        if path:
            self._load_json_into_editor(path)

    def on_browse_json(self):
        path = filedialog.askopenfilename(
            initialdir=SUBJECTS_DIR,
            title="选择知识库 JSON",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
        )
        if not path:
            return
        self.json_choice_var.set(os.path.basename(path))
        self._load_json_into_editor(path)

    def _load_json_into_editor(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.status_var.set(f"错误: 无法读取文件 ({e})")
            return

        self.json_text.delete("1.0", "end")
        self.json_text.insert("1.0", content)
        self.status_var.set(f"已加载: {os.path.basename(path)}")

    def on_generate_preview(self):
        raw = self.json_text.get("1.0", "end").strip()
        if not raw:
            self.status_var.set("错误: JSON 内容为空")
            return

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            self.status_var.set(f"错误: JSON 格式无效 ({e})")
            messagebox.showerror("JSON 解析失败", str(e))
            return

        try:
            from config import OUTPUT_DIR
            import webbrowser

            fmt = self.format_b_var.get().strip() or DEFAULT_FORMAT
            fmt_opts = dict(
                theme=self.theme_var.get().strip() or DEFAULT_THEME,
                style=self.style_var.get().strip() or DEFAULT_STYLE,
                student_name=self.name_var.get().strip(),
                cls=self.cls_var.get().strip(),
                student_id=self.sid_var.get().strip(),
                date=self.date_var.get().strip(),
                watermark=self.watermark_var.get().strip(),
            )
            html = render_html(data, fmt=fmt, **fmt_opts)
            os.makedirs(OUTPUT_DIR, exist_ok=True)

            center = data.get("center", "output")
            subject = data.get("subject", "")
            filename = f"{subject}_{center}.html" if subject else f"{center}.html"
            out_path = os.path.join(OUTPUT_DIR, filename)

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)

            webbrowser.open("file:///" + os.path.abspath(out_path).replace("\\", "/"))
            self.status_var.set(f"已生成: {filename}")
        except Exception as e:
            self.status_var.set(f"错误: {e}")


def run():
    root = tk.Tk()
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    if os.path.isfile(icon_path):
        icon_img = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon_img)
    SubjectDrawGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()
