"""色彩主题模块

每个主题是一组 CSS 变量，装饰和格式渲染器通过 var(--xxx) 引用。
"""

THEMES = {
    "素雅灰": {
        "primary":   "#2b2b2b",
        "accent":    "#666666",
        "border":    "#888888",
        "bg":        "#ffffff",
        "light_bg":  "#f5f5f5",
        "text":      "#222222",
        "muted":     "#888888",
    },
    "沉稳蓝": {
        "primary":   "#1e3a5f",
        "accent":    "#3d6ea5",
        "border":    "#5e83b0",
        "bg":        "#ffffff",
        "light_bg":  "#eef4fa",
        "text":      "#1a2a3d",
        "muted":     "#6a8bad",
    },
    "清新绿": {
        "primary":   "#2f5d3a",
        "accent":    "#4a8a5c",
        "border":    "#6ea87d",
        "bg":        "#ffffff",
        "light_bg":  "#eef7f0",
        "text":      "#1f3a25",
        "muted":     "#7ba586",
    },
    "暖橙": {
        "primary":   "#7a3a15",
        "accent":    "#c26a2a",
        "border":    "#d18a4e",
        "bg":        "#ffffff",
        "light_bg":  "#fbf1e6",
        "text":      "#3a2412",
        "muted":     "#b08055",
    },
}

DEFAULT_THEME = "素雅灰"


def list_themes():
    return list(THEMES.keys())


def get_theme(name):
    return THEMES.get(name, THEMES[DEFAULT_THEME])


def theme_css_vars(name):
    """生成一段 :root CSS 变量声明，供各 renderer 注入 <style> 头部"""
    t = get_theme(name)
    return (
        ":root {\n"
        f"  --primary: {t['primary']};\n"
        f"  --accent: {t['accent']};\n"
        f"  --border: {t['border']};\n"
        f"  --bg: {t['bg']};\n"
        f"  --light-bg: {t['light_bg']};\n"
        f"  --text: {t['text']};\n"
        f"  --muted: {t['muted']};\n"
        "}\n"
    )
