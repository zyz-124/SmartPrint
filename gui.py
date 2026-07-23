# -*- coding: utf-8 -*-
import glob
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import (SUBJECTS_DIR, DEFAULT_FORMAT, DEFAULT_THEME,
                    DEFAULT_STYLE, GUI_SETTINGS_PATH, DEFAULT_GUI_THEME)
from core.gui_themes import THEMES, list_gui_themes
from core.renderer import render_html
from core.format_manager import discover_formats, load_prompt
from core.theme import list_themes
from core.decorations import list_styles
from core.prompts import PROMPT_STYLES

PRESET_SUBJECTS = ["历史", "地理", "生物", "语文", "政治"]


COLOR_GROUPS = [
    ("侧边栏", [("背景", "sidebar_bg"), ("文字", "sidebar_fg"),
                ("悬停", "sidebar_active"), ("强调", "sidebar_accent")]),
    ("内容区", [("背景", "bg"), ("卡片", "card"), ("边框", "border")]),
    ("文字",   [("主文字", "text"), ("次文字", "text2"), ("辅助", "muted")]),
    ("强调色", [("主色", "primary"), ("悬停", "primary_h"), ("强调", "accent")]),
    ("输入框", [("背景", "input_bg")]),
    ("按钮",   [("主按钮背景", "btn_primary_bg"), ("主按钮文字", "btn_primary_fg"),
                ("次按钮背景", "btn_secondary_bg"), ("次按钮文字", "btn_secondary_fg")]),
    ("滚动条", [("背景", "scrollbar_bg"), ("滑块", "scrollbar_fg")]),
    ("其他",   [("链接", "link"), ("悬停背景", "hover_bg"),
                ("成功", "success"), ("错误", "error")]),
]


def load_gui_settings():
    if os.path.isfile(GUI_SETTINGS_PATH):
        try:
            with open(GUI_SETTINGS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"gui_theme": DEFAULT_GUI_THEME}


def save_gui_settings(settings):
    with open(GUI_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def _load_theme_colors(theme_name):
    base = dict(THEMES.get(theme_name, THEMES[DEFAULT_GUI_THEME]))
    settings = load_gui_settings()
    custom = settings.get("custom_colors", {})
    if custom:
        base.update(custom)
    for key in ("font_family", "font_size", "sidebar_width", "card_radius"):
        if key in settings:
            base[key] = settings[key]
    base["_name"] = theme_name
    return base


def scan_json_files():
    result = {}
    pattern = os.path.join(SUBJECTS_DIR, "*", "*.json")
    for path in sorted(glob.glob(pattern)):
        subject = os.path.basename(os.path.dirname(path))
        topic = os.path.splitext(os.path.basename(path))[0]
        result[f"{subject}/{topic}"] = path
    return result


class SidebarItem(tk.Frame):
    def __init__(self, parent, text, command, colors):
        super().__init__(parent, bg=colors["sidebar_bg"], cursor="hand2")
        self.colors = colors
        self.command = command
        self.is_active = False
        ff = colors.get("font_family", "Microsoft YaHei UI")
        self.bar = tk.Frame(self, bg=colors["sidebar_bg"], width=3)
        self.bar.pack(side="left", fill="y")
        self.label = tk.Label(
            self, text=text,
            bg=colors["sidebar_bg"], fg=colors["sidebar_fg"],
            font=(ff, 11),
            anchor="w", padx=16, pady=10,
        )
        self.label.pack(side="left", fill="both", expand=True)
        for w_ in (self, self.label):
            w_.bind("<Enter>", self._on_enter)
            w_.bind("<Leave>", self._on_leave)
            w_.bind("<Button-1>", self._on_click)

    def _on_enter(self, _):
        if not self.is_active:
            bg = self.colors["sidebar_active"]
            self.configure(bg=bg)
            self.bar.configure(bg=bg)
            self.label.configure(bg=bg)

    def _on_leave(self, _):
        if not self.is_active:
            bg = self.colors["sidebar_bg"]
            self.configure(bg=bg)
            self.bar.configure(bg=bg)
            self.label.configure(bg=bg)

    def _on_click(self, _):
        self.command()

    def set_active(self, active):
        self.is_active = active
        if active:
            self.configure(bg=self.colors["sidebar_active"])
            self.bar.configure(bg=self.colors["sidebar_accent"])
            self.label.configure(
                bg=self.colors["sidebar_active"],
                fg=self.colors["sidebar_accent"],
            )
        else:
            self.configure(bg=self.colors["sidebar_bg"])
            self.bar.configure(bg=self.colors["sidebar_bg"])
            self.label.configure(
                bg=self.colors["sidebar_bg"],
                fg=self.colors["sidebar_fg"],
            )


class SubjectDrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SubjectDraw")
        self.root.geometry("850x650")
        self.root.resizable(True, True)
        self.root.minsize(700, 500)

        gui_settings = load_gui_settings()
        theme_name = gui_settings.get("gui_theme", DEFAULT_GUI_THEME)
        if theme_name not in THEMES:
            theme_name = DEFAULT_GUI_THEME
        self.C = _load_theme_colors(theme_name)
        self.root.configure(bg=self.C["bg"])

        self.status_var = tk.StringVar(value="就绪")
        self.current_page = "prompt"
        self._prompt_text_content = ""
        self._json_text_content = ""

        avail = discover_formats() or [DEFAULT_FORMAT]
        default_fmt = DEFAULT_FORMAT if DEFAULT_FORMAT in avail else avail[0]

        self.format_a_var = tk.StringVar(value=default_fmt)
        self.subject_var = tk.StringVar(value=PRESET_SUBJECTS[0])
        self.topic_var = tk.StringVar()
        self.prompt_style_var = tk.StringVar(value="简约")
        self.format_b_var = tk.StringVar(value=default_fmt)
        self.json_choice_var = tk.StringVar()
        self.theme_var = tk.StringVar(value=DEFAULT_THEME)
        self.style_var = tk.StringVar(value=DEFAULT_STYLE)


        self._apply_styles()
        self._build_status_bar()
        self._build_sidebar()
        self._build_content_area()
        self._switch_page("prompt")

    def _rebuild_gui(self):
        for w in self.root.winfo_children():
            w.destroy()
        gui_settings = load_gui_settings()
        theme_name = gui_settings.get("gui_theme", DEFAULT_GUI_THEME)
        if theme_name not in THEMES:
            theme_name = DEFAULT_GUI_THEME
        self.C = _load_theme_colors(theme_name)
        self.root.configure(bg=self.C["bg"])
        self._apply_styles()
        self._build_status_bar()
        self._build_sidebar()
        self._build_content_area()
        self._switch_page(self.current_page)

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        C = self.C
        ff = C.get("font_family", "Microsoft YaHei UI")
        fs = C.get("font_size", 10)
        s.configure(".", background=C["bg"], foreground=C["text"],
                     font=(ff, fs))
        s.configure("TFrame", background=C["bg"])
        s.configure("Card.TFrame", background=C["card"])
        s.configure("TLabel", background=C["bg"], foreground=C["text"],
                     font=(ff, fs))
        s.configure("Card.TLabel", background=C["card"], foreground=C["text"])
        s.configure("TEntry", fieldbackground=C["input_bg"], foreground=C["text"],
                     borderwidth=1, relief="solid", padding=[6, 4])
        s.map("TEntry", bordercolor=[("focus", C["primary"])],
              relief=[("focus", "solid")])
        s.configure("TCombobox", fieldbackground=C["input_bg"], foreground=C["text"],
                     borderwidth=1, relief="solid", padding=[6, 4])
        s.map("TCombobox", bordercolor=[("focus", C["primary"])])
        s.configure("Primary.TButton", background=C.get("btn_primary_bg", C["primary"]),
                     foreground=C.get("btn_primary_fg", "#FFFFFF"),
                     borderwidth=0, padding=[14, 7],
                     font=(ff, fs, "bold"))
        s.map("Primary.TButton",
              background=[("active", C["primary_h"]), ("pressed", C["primary_h"])])
        s.configure("Secondary.TButton", background=C.get("btn_secondary_bg", C["card"]),
                     foreground=C.get("btn_secondary_fg", C["primary"]),
                     borderwidth=1, relief="solid", padding=[10, 5],
                     font=(ff, fs - 1))
        s.map("Secondary.TButton", background=[("active", C["bg"])])
        s.configure("Link.TButton", background=C["card"], foreground=C["muted"],
                     borderwidth=0, padding=[6, 4],
                     font=(ff, fs - 1))
        s.map("Link.TButton", foreground=[("active", C["primary"])])
        s.configure("Horizontal.TScrollbar",
                     background=C.get("scrollbar_bg", C["border"]),
                     troughcolor=C["bg"],
                     borderwidth=0, arrowsize=0)

    def _build_status_bar(self):
        C = self.C
        ff = C.get("font_family", "Microsoft YaHei UI")
        tk.Label(
            self.root, textvariable=self.status_var,
            anchor="w", bg=C["card"], fg=C["muted"],
            font=(ff, 9),
            padx=12, pady=5,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["border"],
        ).pack(fill="x", side="bottom")

    def _build_sidebar(self):
        C = self.C
        ff = C.get("font_family", "Microsoft YaHei UI")
        sidebar_w = C.get("sidebar_width", 180)
        self.sidebar = tk.Frame(self.root, bg=C["sidebar_bg"], width=sidebar_w)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tf = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        tf.pack(fill="x", pady=(24, 0))
        tk.Label(tf, text="SubjectDraw",
                 bg=C["sidebar_bg"], fg=C["sidebar_fg"],
                 font=(ff, 15, "bold"),
                 anchor="w", padx=20).pack(fill="x")
        tk.Label(tf, text="知识卡片排版工具",
                 bg=C["sidebar_bg"], fg=C["muted"],
                 font=(ff, 8),
                 anchor="w", padx=20).pack(fill="x", pady=(2, 0))
        tk.Frame(self.sidebar, bg=C["sidebar_bg"], height=24).pack()
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(fill="x", padx=20)
        nf = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        nf.pack(fill="x", pady=(12, 0))
        self.prompt_item = SidebarItem(nf, "  生成提示词",
                                       lambda: self._switch_page("prompt"), C)
        self.prompt_item.pack(fill="x")
        self.preview_item = SidebarItem(nf, "  生成预览",
                                        lambda: self._switch_page("preview"), C)
        self.preview_item.pack(fill="x")
        tk.Frame(self.sidebar, bg=C["sidebar_bg"]).pack(fill="both", expand=True)
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(fill="x", padx=20)
        sf = tk.Frame(self.sidebar, bg=C["sidebar_bg"], cursor="hand2")
        sf.pack(fill="x", pady=(10, 24))
        sl = tk.Label(sf, text="  设置",
                      bg=C["sidebar_bg"], fg=C["sidebar_fg"],
                      font=("Microsoft YaHei UI", 10),
                      anchor="w", padx=20, pady=8)
        sl.pack(fill="x")
        def se(_): sf.configure(bg=C["sidebar_active"]); sl.configure(bg=C["sidebar_active"])
        def slv(_): sf.configure(bg=C["sidebar_bg"]); sl.configure(bg=C["sidebar_bg"])
        for w_ in (sf, sl):
            w_.bind("<Enter>", se)
            w_.bind("<Leave>", slv)
            w_.bind("<Button-1>", lambda _: self.open_settings())

    def _build_content_area(self):
        self.content = tk.Frame(self.root, bg=self.C["bg"])
        self.content.pack(side="left", fill="both", expand=True)

    def _switch_page(self, page):
        if hasattr(self, "prompt_text") and self.prompt_text.winfo_exists():
            self._prompt_text_content = self.prompt_text.get("1.0", "end").strip()
        if hasattr(self, "json_text") and self.json_text.winfo_exists():
            self._json_text_content = self.json_text.get("1.0", "end").strip()
        for w_ in self.content.winfo_children():
            w_.destroy()
        self.current_page = page
        self.prompt_item.set_active(page == "prompt")
        self.preview_item.set_active(page == "preview")
        if page == "prompt":
            self._build_page_prompt()
        else:
            self._build_page_preview()

    def _card(self, parent, **kw):
        return tk.Frame(parent, bg=self.C["card"],
                        highlightthickness=1,
                        highlightbackground=self.C["border"],
                        highlightcolor=self.C["border"], **kw)

    def _lbl(self, parent, text):
        ff = self.C.get("font_family", "Microsoft YaHei UI")
        return tk.Label(parent, text=text,
                        bg=self.C["card"], fg=self.C["text2"],
                        font=(ff, 9))

    def _input(self, parent, variable, width=20, **kw):
        return ttk.Entry(parent, textvariable=variable, width=width, **kw)

    def _combo(self, parent, variable, values, width=18):
        return ttk.Combobox(parent, textvariable=variable,
                            values=values, width=width, state="readonly")

    def _build_page_prompt(self):
        C = self.C
        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=20, pady=16)
        c1 = self._card(outer)
        c1.pack(fill="x")
        i1 = tk.Frame(c1, bg=C["card"])
        i1.pack(fill="x", padx=16, pady=14)
        tk.Label(i1, text="基本信息", bg=C["card"], fg=C["primary"],
                 font=("Microsoft YaHei UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        g = tk.Frame(i1, bg=C["card"])
        g.pack(fill="x")
        g.columnconfigure(1, weight=1)
        g.columnconfigure(3, weight=1)
        avail = discover_formats() or [DEFAULT_FORMAT]
        self._lbl(g, "格式").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g, self.format_a_var, avail, 16).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=(0, 16), pady=(0, 8))
        self._lbl(g, "学科").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g, self.subject_var, PRESET_SUBJECTS, 16).grid(
            row=1, column=2, columnspan=2, sticky="ew", pady=(0, 8))
        self._lbl(g, "主题").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=(0, 2))
        self._input(g, self.topic_var, 16).grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 16), pady=(0, 4))
        self._lbl(g, "提示词风格").grid(row=2, column=2, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g, self.prompt_style_var, PROMPT_STYLES, 16).grid(
            row=3, column=2, columnspan=2, sticky="ew", pady=(0, 4))

        c2 = self._card(outer)
        c2.pack(fill="x", pady=(10, 0))
        i2 = tk.Frame(c2, bg=C["card"])
        i2.pack(fill="x", padx=16, pady=12)
        bf = tk.Frame(i2, bg=C["card"])
        bf.pack(fill="x")
        ttk.Button(bf, text="生成提示词", style="Primary.TButton",
                   command=self.on_generate_prompt).pack(side="left", padx=(0, 8))
        ttk.Button(bf, text="设置", style="Link.TButton",
                   command=self.open_settings).pack(side="right")

        c3 = self._card(outer)
        c3.pack(fill="both", expand=True, pady=(10, 0))
        i3 = tk.Frame(c3, bg=C["card"])
        i3.pack(fill="both", expand=True, padx=12, pady=(8, 12))
        self.prompt_text = tk.Text(
            i3, wrap="word", state="disabled",
            bg=C["input_bg"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            borderwidth=0, highlightthickness=1,
            highlightbackground=C["border"], highlightcolor=C["primary"],
            padx=8, pady=8)
        sb = ttk.Scrollbar(i3, command=self.prompt_text.yview)
        self.prompt_text.configure(yscrollcommand=sb.set)
        self.prompt_text.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        if self._prompt_text_content:
            self.prompt_text.configure(state="normal")
            self.prompt_text.insert("1.0", self._prompt_text_content)
            self.prompt_text.configure(state="disabled")

    def _build_page_preview(self):
        C = self.C
        outer = tk.Frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True, padx=20, pady=16)
        c1 = self._card(outer)
        c1.pack(fill="x")
        i1 = tk.Frame(c1, bg=C["card"])
        i1.pack(fill="x", padx=16, pady=12)
        self._lbl(i1, "JSON 文件").pack(anchor="w", pady=(0, 4))
        ff = tk.Frame(i1, bg=C["card"])
        ff.pack(fill="x")
        self.json_map = scan_json_files()
        self.json_combo = ttk.Combobox(
            ff, textvariable=self.json_choice_var,
            values=list(self.json_map.keys()), width=30, state="readonly")
        self.json_combo.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.json_combo.bind("<<ComboboxSelected>>", self.on_select_json)
        ttk.Button(ff, text="浏览", style="Secondary.TButton",
                   command=self.on_browse_json).pack(side="left")

        c2 = self._card(outer)
        c2.pack(fill="x", pady=(10, 0))
        i2 = tk.Frame(c2, bg=C["card"])
        i2.pack(fill="x", padx=16, pady=12)
        tk.Label(i2, text="样式设置", bg=C["card"], fg=C["primary"],
                 font=("Microsoft YaHei UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        g2 = tk.Frame(i2, bg=C["card"])
        g2.pack(fill="x")
        g2.columnconfigure(1, weight=1)
        g2.columnconfigure(3, weight=1)
        avail = discover_formats() or [DEFAULT_FORMAT]
        self._lbl(g2, "格式").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g2, self.format_b_var, avail, 14).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=(0, 16), pady=(0, 8))
        self._lbl(g2, "色彩主题").grid(row=0, column=2, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g2, self.theme_var, list_themes(), 14).grid(
            row=1, column=2, columnspan=2, sticky="ew", pady=(0, 8))
        self._lbl(g2, "装饰风格").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=(0, 2))
        self._combo(g2, self.style_var, list_styles(), 14).grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=(0, 16), pady=(0, 4))

        c4 = self._card(outer)
        c4.pack(fill="both", expand=True, pady=(10, 0))
        i4 = tk.Frame(c4, bg=C["card"])
        i4.pack(fill="both", expand=True, padx=12, pady=(8, 12))
        bf = tk.Frame(i4, bg=C["card"])
        bf.pack(fill="x", pady=(0, 8))
        ttk.Button(bf, text="生成预览", style="Primary.TButton",
                   command=self.on_generate_preview).pack(side="right")
        tk.Label(i4, text="在此粘贴 AI 生成的 JSON", bg=C["card"], fg=C["text2"],
                 font=("Microsoft YaHei UI", 9)).pack(anchor="w", pady=(0, 4))
        self.json_text = tk.Text(
            i4, wrap="none",
            bg=C["input_bg"], fg=C["text"],
            font=("Consolas", 10), relief="flat",
            borderwidth=0, highlightthickness=1,
            highlightbackground=C["border"], highlightcolor=C["primary"],
            padx=8, pady=8)
        js = ttk.Scrollbar(i4, command=self.json_text.yview)
        self.json_text.configure(yscrollcommand=js.set)
        self.json_text.pack(side="left", fill="both", expand=True)
        js.pack(side="right", fill="y")
        if self._json_text_content:
            self.json_text.insert("1.0", self._json_text_content)

    def open_settings(self):
        gui_settings = load_gui_settings()
        C = self.C
        theme_name = C.get("_name", DEFAULT_GUI_THEME)

        dlg = tk.Toplevel(self.root)
        dlg.title("设置")
        dlg.geometry("500x520")
        dlg.resizable(False, False)
        dlg.configure(bg=C["bg"])
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 520) // 2
        dlg.geometry(f"+{x}+{y}")

        canvas = tk.Canvas(dlg, bg=C["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(dlg, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=C["bg"])
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable.bind("<MouseWheel>", _on_mousewheel)

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas.find_all()[-1], width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        tc = self._card(scrollable)
        tc.pack(fill="x", padx=12, pady=(12, 0))
        ti = tk.Frame(tc, bg=C["card"])
        ti.pack(fill="x", padx=16, pady=14)
        tk.Label(ti, text="界面设置", bg=C["card"], fg=C["primary"],
                 font=("Microsoft YaHei UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        tf = tk.Frame(ti, bg=C["card"])
        tf.pack(fill="x")
        self._lbl(tf, "界面主题").pack(anchor="w", pady=(0, 2))
        gui_theme_var = tk.StringVar(value=gui_settings.get("gui_theme", DEFAULT_GUI_THEME))
        ttk.Combobox(tf, textvariable=gui_theme_var,
                     values=list_gui_themes(), width=20, state="readonly").pack(fill="x", pady=(0, 6))
        tk.Label(ti, text="切换后立即生效",
                 bg=C["card"], fg=C["muted"],
                 font=("Microsoft YaHei UI", 8)).pack(anchor="w")

        lf = tk.Frame(ti, bg=C["card"])
        lf.pack(fill="x", pady=(8, 0))
        lf.columnconfigure(1, weight=1)
        self._lbl(lf, "字体").grid(row=0, column=0, sticky="w", padx=(0, 6))
        theme_def = THEMES.get(gui_settings.get("gui_theme", DEFAULT_GUI_THEME), {})
        font_family_var = tk.StringVar(value=gui_settings.get("font_family", theme_def.get("font_family", "Microsoft YaHei UI")))
        ttk.Combobox(lf, textvariable=font_family_var, width=18, state="readonly",
                     values=["Microsoft YaHei UI", "SimHei", "SimSun", "KaiTi",
                             "Arial", "Consolas", "Segoe UI", "PingFang SC"]).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=(0, 16))
        self._lbl(lf, "字号").grid(row=0, column=2, sticky="w", padx=(0, 6))
        font_size_var = tk.StringVar(value=str(gui_settings.get("font_size", theme_def.get("font_size", 10))))
        ttk.Combobox(lf, textvariable=font_size_var, width=6, state="readonly",
                     values=["8", "9", "10", "11", "12", "14", "16"]).grid(
            row=1, column=2, sticky="ew")

        sf = tk.Frame(ti, bg=C["card"])
        sf.pack(fill="x", pady=(8, 0))
        sf.columnconfigure(1, weight=1)
        self._lbl(sf, "侧边栏宽度").grid(row=0, column=0, sticky="w", padx=(0, 6))
        sidebar_width_var = tk.StringVar(value=str(gui_settings.get("sidebar_width", theme_def.get("sidebar_width", 180))))
        ttk.Combobox(sf, textvariable=sidebar_width_var, width=6, state="readonly",
                     values=["140", "160", "180", "200", "220", "240"]).grid(
            row=1, column=0, sticky="ew", padx=(0, 16))
        self._lbl(sf, "卡片圆角").grid(row=0, column=2, sticky="w", padx=(0, 6))
        card_radius_var = tk.StringVar(value=str(gui_settings.get("card_radius", theme_def.get("card_radius", 8))))
        ttk.Combobox(sf, textvariable=card_radius_var, width=6, state="readonly",
                     values=["0", "4", "6", "8", "10", "12", "16"]).grid(
            row=1, column=2, sticky="ew")

        custom_colors = gui_settings.get("custom_colors", {})
        color_vars = {}

        cc_card = self._card(scrollable)
        cc_card.pack(fill="x", padx=12, pady=(10, 0))
        cc_inner = tk.Frame(cc_card, bg=C["card"])
        cc_inner.pack(fill="x", padx=16, pady=14)
        tk.Label(cc_inner, text="自定义颜色", bg=C["card"], fg=C["primary"],
                 font=("Microsoft YaHei UI", 11, "bold")).pack(anchor="w", pady=(0, 2))
        tk.Label(cc_inner, text="留空使用主题默认色，输入 #RRGGBB 格式",
                 bg=C["card"], fg=C["muted"],
                 font=("Microsoft YaHei UI", 8)).pack(anchor="w", pady=(0, 10))

        for group_name, fields in COLOR_GROUPS:
            tk.Label(cc_inner, text=group_name, bg=C["card"], fg=C["text2"],
                     font=("Microsoft YaHei UI", 9, "bold")).pack(anchor="w", pady=(8, 2))
            row_frame = tk.Frame(cc_inner, bg=C["card"])
            row_frame.pack(fill="x")
            for i, (label_text, key) in enumerate(fields):
                r = i // 2
                c = (i % 2) * 3
                current_val = custom_colors.get(key, "")
                default_val = THEMES.get(theme_name, {}).get(key, "#FFFFFF")
                var = tk.StringVar(value=current_val)
                color_vars[key] = var

                preview = tk.Frame(row_frame, bg=current_val or default_val,
                                   width=16, height=16,
                                   highlightthickness=1,
                                   highlightbackground=C["border"])
                preview.grid(row=r, column=c, padx=(0, 3), pady=2, sticky="w")

                tk.Label(row_frame, text=label_text, bg=C["card"], fg=C["text2"],
                         font=("Microsoft YaHei UI", 9)).grid(
                    row=r, column=c+1, sticky="w", padx=(0, 3))

                entry = ttk.Entry(row_frame, textvariable=var, width=9)
                entry.grid(row=r, column=c+2, sticky="w", padx=(0, 12), pady=2)

                def make_update(p, k, v, tn=theme_name):
                    def update(*_):
                        val = v.get().strip()
                        default = THEMES.get(tn, {}).get(k, "#FFFFFF")
                        try:
                            p.configure(bg=val if val else default)
                        except Exception:
                            pass
                    return update
                var.trace_add("write", make_update(preview, key, var))

        def reset_colors():
            for key, var in color_vars.items():
                var.set("")

        tk.Button(cc_inner, text="恢复默认颜色", bg=C["card"], fg=C["primary"],
                  font=("Microsoft YaHei UI", 9), bd=0, cursor="hand2",
                  command=reset_colors).pack(anchor="w", pady=(8, 0))

        def on_save():
            custom = {}
            for key, var in color_vars.items():
                val = var.get().strip()
                if val:
                    custom[key] = val
            settings = {"gui_theme": gui_theme_var.get()}
            if custom:
                settings["custom_colors"] = custom
            settings["font_family"] = font_family_var.get()
            settings["font_size"] = int(font_size_var.get())
            settings["sidebar_width"] = int(sidebar_width_var.get())
            settings["card_radius"] = int(card_radius_var.get())
            save_gui_settings(settings)
            dlg.destroy()
            self._rebuild_gui()

        bf2 = tk.Frame(scrollable, bg=C["bg"])
        bf2.pack(fill="x", padx=12, pady=(12, 16))
        ttk.Button(bf2, text="保存", style="Primary.TButton",
                   command=on_save).pack(side="left")

    def on_generate_prompt(self):
        subject = self.subject_var.get().strip()
        topic = self.topic_var.get().strip()
        fmt = self.format_a_var.get().strip()
        style = self.prompt_style_var.get().strip()
        if not subject or not topic:
            self.status_var.set("请填写学科和主题")
            return
        try:
            text = load_prompt(fmt, subject, topic, style=style)
        except Exception as e:
            self.status_var.set(f"错误: {e}")
            return
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", "end")
        self.prompt_text.insert("1.0", text)
        self.prompt_text.configure(state="disabled")
        self._prompt_text_content = text
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("提示词已复制，粘贴到 AI 聊天中，再点「粘贴 JSON」")

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
        self._json_text_content = content
        self.status_var.set(f"已加载: {os.path.basename(path)}")

    def on_generate_preview(self):
        raw = self.json_text.get("1.0", "end").strip()
        if not raw:
            self.status_var.set("错误: JSON 内容为空")
            return
        try:
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(raw)
        except (json.JSONDecodeError, ValueError) as e:
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