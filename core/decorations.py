"""装饰模块 — 4 套装饰风格 + 通用 HTML 辅助函数

通用函数:
  student_info_html(...)   → 学生信息栏
  footer_html(...)         → 页脚
  knowledge_panel_html(...)→ 知识面板
"""

from core.theme import get_theme

STYLES = {
    "简约几何": "_geo",
    "中式古典": "_cn",
    "自然花藤": "_vine",
    "学术边框": "_acad",
}

DEFAULT_STYLE = "简约几何"


def list_styles():
    return list(STYLES.keys())


# ═══════════════════════════════════════════════════════════
#  通用 HTML 片段
# ═══════════════════════════════════════════════════════════

def student_info_html(name="", cls="", sid="", date=""):
    parts = [p for p in [name, cls, sid, date] if p]
    if not parts:
        return ""
    return (
        '<div class="student-info">'
        + " &nbsp;|&nbsp; ".join(parts)
        + "</div>"
    )


def footer_html(page_num="1", date=""):
    right = f"{date}" if date else ""
    return (
        '<div class="footer-line">'
        f'<span>第 {page_num} 页</span>'
        f'<span>{right}</span>'
        "</div>"
    )


# ═══════════════════════════════════════════════════════════
#  共用 CSS（流式布局，不依赖 A4 尺寸）
# ═══════════════════════════════════════════════════════════

def shared_css():
    return """
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.subject-label {
    font-size: 14px;
    color: var(--muted, #555);
    letter-spacing: 3px;
    padding: 6px 14px;
    border: 1px dashed var(--border, #888);
    border-radius: 14px;
    background: var(--bg, #fff);
}
.student-info {
    font-size: 11px;
    color: var(--muted, #888);
    letter-spacing: 2px;
    white-space: nowrap;
}
.footer-line {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: var(--muted, #888);
    border-top: 1px solid var(--border, #ccc);
    padding-top: 8px;
    margin-top: 20px;
}
"""


def knowledge_panel_css():
    return """
.knowledge-panel {
    border-top: 2px solid var(--border, #ddd);
    padding-top: 14px;
    margin-top: 16px;
}
.kp-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px 20px;
}
.kp-section {
    margin-bottom: 10px;
}
.kp-label {
    font-size: 12px;
    font-weight: bold;
    color: var(--primary, #333);
    letter-spacing: 3px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px dashed var(--border, #ccc);
}
.kp-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.kp-card {
    flex: 1 1 calc(50% - 6px);
    min-width: 140px;
    background: var(--light-bg, #f5f5f5);
    border: 1px solid var(--border, #ddd);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 11px;
    line-height: 1.5;
}
.kp-card .term {
    font-weight: bold;
    color: var(--primary, #222);
    font-size: 12px;
    margin-bottom: 2px;
}
.kp-card .explain {
    color: var(--text, #444);
    font-size: 11px;
}
.kp-figure {
    display: flex;
    align-items: baseline;
    gap: 6px;
    font-size: 11px;
    line-height: 1.6;
    margin-bottom: 4px;
}
.kp-figure .fname {
    font-weight: bold;
    color: var(--primary, #222);
    white-space: nowrap;
}
.kp-figure .frole {
    color: var(--muted, #888);
    white-space: nowrap;
    font-size: 10px;
}
.kp-figure .fcontrib {
    color: var(--text, #444);
    font-size: 10px;
}
.kp-list {
    font-size: 11px;
    line-height: 1.7;
    color: var(--text, #444);
    padding-left: 16px;
}
.kp-list li {
    margin-bottom: 2px;
}
.kp-exam {
    font-size: 11px;
    line-height: 1.7;
    color: var(--text, #444);
}
.kp-exam li {
    margin-bottom: 2px;
    list-style: none;
    padding-left: 0;
}
.kp-exam li::before {
    content: "\\25C6 ";
    color: var(--accent, #666);
    margin-right: 4px;
}
"""


def knowledge_panel_html(data, style_name):
    concepts = data.get("key_concepts", [])
    figures = data.get("key_figures", [])
    marginalia = data.get("marginalia", [])
    exam_focus = data.get("exam_focus", [])

    if not concepts and not figures and not marginalia and not exam_focus:
        return ""

    left_parts = []
    right_parts = []

    if concepts:
        cards = ""
        for c in concepts:
            cards += (
                f'<div class="kp-card">'
                f'<div class="term">{c.get("term", "")}</div>'
                f'<div class="explain">{c.get("explain", "")}</div>'
                f'</div>'
            )
        left_parts.append(
            f'<div class="kp-section">'
            f'<div class="kp-label">核心概念</div>'
            f'<div class="kp-cards">{cards}</div>'
            f'</div>'
        )

    if figures:
        items = ""
        for f in figures:
            name = f.get("name", "")
            title = f.get("title", "")
            contrib = f.get("contribution", "")
            items += (
                f'<div class="kp-figure">'
                f'<span class="fname">{bullet_svg(style_name)} {name}</span>'
                f'<span class="frole">{title}</span>'
                f'<span class="fcontrib">— {contrib}</span>'
                f'</div>'
            )
        right_parts.append(
            f'<div class="kp-section">'
            f'<div class="kp-label">关键人物</div>'
            f'{items}'
            f'</div>'
        )

    if marginalia:
        lis = "".join(f"<li>{m}</li>" for m in marginalia)
        left_parts.append(
            f'<div class="kp-section">'
            f'<div class="kp-label">知识拓展</div>'
            f'<ul class="kp-list">{lis}</ul>'
            f'</div>'
        )

    if exam_focus:
        lis = "".join(f"<li>{e}</li>" for e in exam_focus)
        right_parts.append(
            f'<div class="kp-section">'
            f'<div class="kp-label">考点聚焦</div>'
            f'<ul class="kp-exam">{lis}</ul>'
            f'</div>'
        )

    return (
        '<div class="knowledge-panel">'
        + divider_html(style_name)
        + '<div class="kp-grid">'
        + '<div>' + "".join(left_parts) + '</div>'
        + '<div>' + "".join(right_parts) + '</div>'
        + '</div>'
        + '</div>'
    )


# ═══════════════════════════════════════════════════════════
#  风格 1：简约几何
# ═══════════════════════════════════════════════════════════

def _geo_divider():
    return (
        '<svg width="100%" height="12" viewBox="0 0 600 12" xmlns="http://www.w3.org/2000/svg">'
        '<line x1="0" y1="6" x2="280" y2="6" stroke="var(--border,#888)" stroke-width="1"/>'
        '<polygon points="300,0 306,6 300,12 294,6" fill="var(--accent,#666)"/>'
        '<line x1="320" y1="6" x2="600" y2="6" stroke="var(--border,#888)" stroke-width="1"/>'
        '</svg>'
    )


def _geo_title_ornament():
    return '<span class="title-ornament" style="color:var(--accent,#666);font-size:11px;letter-spacing:6px">&nbsp;&#9670;&nbsp;</span>'


def _geo_bullet_svg(color="var(--accent, #666)"):
    return f'<svg width="8" height="8" viewBox="0 0 8 8" style="vertical-align:middle;margin-right:4px"><circle cx="4" cy="4" r="3" fill="{color}"/></svg>'


def _geo_css():
    return ""


# ═══════════════════════════════════════════════════════════
#  风格 2：中式古典
# ═══════════════════════════════════════════════════════════

def _cn_divider():
    c1 = "var(--border, #888)"
    c2 = "var(--accent, #666)"
    return (
        '<svg width="100%" height="16" viewBox="0 0 600 16" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="20" y1="5" x2="270" y2="5" stroke="{c1}" stroke-width="1"/>'
        f'<line x1="20" y1="11" x2="270" y2="11" stroke="{c1}" stroke-width="1"/>'
        f'<path d="M280,8 Q290,2 300,8 Q310,14 320,8" fill="none" stroke="{c2}" stroke-width="1.5"/>'
        f'<line x1="330" y1="5" x2="580" y2="5" stroke="{c1}" stroke-width="1"/>'
        f'<line x1="330" y1="11" x2="580" y2="11" stroke="{c1}" stroke-width="1"/>'
        '</svg>'
    )


def _cn_title_ornament():
    return '<span class="title-ornament" style="color:var(--accent,#666);font-size:13px;letter-spacing:4px">&nbsp;&#9775;&nbsp;</span>'


def _cn_bullet_svg(color="var(--accent, #666)"):
    return f'<svg width="9" height="9" viewBox="0 0 9 9" style="vertical-align:middle;margin-right:4px"><rect x="1.5" y="1.5" width="6" height="6" fill="none" stroke="{color}" stroke-width="1.2" transform="rotate(45 4.5 4.5)"/></svg>'


def _cn_css():
    return ""


# ═══════════════════════════════════════════════════════════
#  风格 3：自然花藤
# ═══════════════════════════════════════════════════════════

def _vine_divider():
    c = "var(--accent, #666)"
    leaf = "var(--accent, #4a8a5c)"
    return (
        '<svg width="100%" height="18" viewBox="0 0 600 18" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M30,9 Q80,2 140,9 Q200,16 260,9 Q300,4 340,9 Q400,16 460,9 Q520,2 570,9" '
        f'fill="none" stroke="{c}" stroke-width="1.2" stroke-linecap="round"/>'
        f'<ellipse cx="140" cy="6" rx="5" ry="3" fill="{leaf}" opacity="0.5" transform="rotate(-20 140 6)"/>'
        f'<ellipse cx="300" cy="5" rx="5" ry="3" fill="{leaf}" opacity="0.5" transform="rotate(15 300 5)"/>'
        f'<ellipse cx="460" cy="6" rx="5" ry="3" fill="{leaf}" opacity="0.5" transform="rotate(-10 460 6)"/>'
        '</svg>'
    )


def _vine_title_ornament():
    return '<span class="title-ornament" style="color:var(--accent,#4a8a5c);font-size:12px;letter-spacing:4px">&nbsp;&#10048;&nbsp;</span>'


def _vine_bullet_svg(color="var(--accent, #4a8a5c)"):
    return f'<svg width="10" height="10" viewBox="0 0 10 10" style="vertical-align:middle;margin-right:3px"><circle cx="5" cy="5" r="4" fill="{color}" opacity="0.7"/><circle cx="5" cy="5" r="2" fill="{color}"/></svg>'


def _vine_css():
    return ""


# ═══════════════════════════════════════════════════════════
#  风格 4：学术边框
# ═══════════════════════════════════════════════════════════

def _acad_divider():
    c = "var(--border, #888)"
    return (
        '<svg width="100%" height="12" viewBox="0 0 600 12" xmlns="http://www.w3.org/2000/svg">'
        f'<line x1="30" y1="3" x2="570" y2="3" stroke="{c}" stroke-width="2"/>'
        f'<line x1="30" y1="9" x2="570" y2="9" stroke="{c}" stroke-width="2"/>'
        '</svg>'
    )


def _acad_title_ornament():
    return '<span class="title-ornament" style="color:var(--primary,#333);font-size:10px;letter-spacing:4px">&nbsp;&#9632;&nbsp;</span>'


def _acad_bullet_svg(color="var(--primary, #333)"):
    return f'<svg width="8" height="8" viewBox="0 0 8 8" style="vertical-align:middle;margin-right:4px"><rect x="1" y="1" width="6" height="6" fill="none" stroke="{color}" stroke-width="1.2"/></svg>'


def _acad_css():
    return ""


# ═══════════════════════════════════════════════════════════
#  统一调度接口
# ═══════════════════════════════════════════════════════════

_DISPATCH = {
    "简约几何": {
        "divider":    _geo_divider,
        "title_orn":  _geo_title_ornament,
        "bullet":     _geo_bullet_svg,
        "css":        _geo_css,
    },
    "中式古典": {
        "divider":    _cn_divider,
        "title_orn":  _cn_title_ornament,
        "bullet":     _cn_bullet_svg,
        "css":        _cn_css,
    },
    "自然花藤": {
        "divider":    _vine_divider,
        "title_orn":  _vine_title_ornament,
        "bullet":     _vine_bullet_svg,
        "css":        _vine_css,
    },
    "学术边框": {
        "divider":    _acad_divider,
        "title_orn":  _acad_title_ornament,
        "bullet":     _acad_bullet_svg,
        "css":        _acad_css,
    },
}


def _get(style_name):
    return _DISPATCH.get(style_name, _DISPATCH[DEFAULT_STYLE])


def divider_html(style_name):
    return _get(style_name)["divider"]()


def title_ornament(style_name):
    return _get(style_name)["title_orn"]()


def bullet_svg(style_name, color=None):
    fn = _get(style_name)["bullet"]
    return fn(color) if color else fn()


def decoration_css(style_name):
    return _get(style_name)["css"]()


def corner_ornaments(style_name, w, h):
    return ""
