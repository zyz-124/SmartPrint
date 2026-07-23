from core.theme import theme_css_vars
from core.decorations import (
    divider_html, title_ornament, bullet_svg,
    shared_css, decoration_css, student_info_html, footer_html,
    knowledge_panel_html, knowledge_panel_css, base_page_css,
)


def render_html(data, **fmt_opts):
    theme = fmt_opts.get("theme", "素雅灰")
    style = fmt_opts.get("style", "简约几何")

    center = data.get("center", "")
    subtitle = data.get("subtitle", "")
    subject = data.get("subject", "")
    branches = data.get("branches", [])

    student_html = student_info_html(
        fmt_opts.get("student_name", ""),
        fmt_opts.get("cls", ""),
        fmt_opts.get("student_id", ""),
        fmt_opts.get("date", ""),
    )
    footer = footer_html("1", fmt_opts.get("date", ""))
    divider = divider_html(style)
    title_dec = title_ornament(style)

    items_html = ""
    for i, branch in enumerate(branches):
        title = branch.get("title", "")
        points = branch.get("points", [])
        points_html = ""
        for p in points:
            points_html += (
                f'<li class="point">{bullet_svg(style)} {p}</li>'
            )
        items_html += f"""
        <div class="item">
            <div class="level1">
                <span class="num">{i+1}</span>
                <span class="title">{title}</span>
            </div>
            <ul class="level2">
                {points_html}
            </ul>
        </div>"""

    kp_html = knowledge_panel_html(data, style)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{center}</title>
<style>
{theme_css_vars(theme)}
{shared_css()}
{decoration_css(style)}
{knowledge_panel_css()}
{base_page_css()}
.outline-grid {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:16px 32px;
    margin-bottom:20px;
}}
.item {{
    padding-left:18px;
    border-left:3px solid var(--accent, #aaa);
}}
.level1 {{
    display:flex;
    align-items:center;
    margin-bottom:8px;
}}
.num {{
    width:26px;
    height:26px;
    border:1.5px solid var(--primary, #333);
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:13px;
    font-weight:bold;
    margin-right:10px;
    flex-shrink:0;
    color:var(--primary, #333);
}}
.level1 .title {{
    font-size:16px;
    font-weight:bold;
    letter-spacing:2px;
    color:var(--primary, #222);
}}
.level2 {{
    list-style:none;
    padding-left:36px;
}}
.point {{
    font-size:13px;
    color:var(--text, #333);
    padding:4px 0;
    border-bottom:1px dashed var(--border, #ccc);
    letter-spacing:1px;
    line-height:1.6;
}}
.point:last-child {{
    border-bottom:none;
}}
</style>
</head>
<body>
<div class="page">
    <div class="top-bar">
        <div class="subject-label">{subject}</div>
        {student_html}
    </div>
    <div class="header">
        <h1>{title_dec} {center} {title_dec}</h1>
        <div class="subtitle">{subtitle}</div>
        <div class="divider-wrap">{divider}</div>
    </div>
    <div class="outline-grid">
        {items_html}
    </div>
    {kp_html}
    {footer}
</div>
</body>
</html>"""
    return html
