from core.theme import theme_css_vars
from core.decorations import (
    divider_html, title_ornament, bullet_svg,
    shared_css, decoration_css, student_info_html, footer_html,
    knowledge_panel_html, knowledge_panel_css,
)


def render_html(data, **fmt_opts):
    theme = fmt_opts.get("theme", "素雅灰")
    style = fmt_opts.get("style", "简约几何")

    center = data.get("center", "")
    subtitle = data.get("subtitle", "")
    subject = data.get("subject", "")
    branches = data.get("branches", [])
    timeline = data.get("timeline", [])

    student_html = student_info_html(
        fmt_opts.get("student_name", ""),
        fmt_opts.get("cls", ""),
        fmt_opts.get("student_id", ""),
        fmt_opts.get("date", ""),
    )
    footer = footer_html("1", fmt_opts.get("date", ""))
    divider = divider_html(style)
    title_dec = title_ornament(style)

    branch_cards = ""
    for b in branches:
        title = b.get("title", "")
        points = b.get("points", [])
        points_html = ""
        for p in points:
            points_html += (
                f'<li class="branch-point">{bullet_svg(style)} {p}</li>'
            )
        branch_cards += f"""
        <div class="branch-card">
            <div class="branch-title">{title}</div>
            <ul class="branch-points">{points_html}</ul>
        </div>"""

    timeline_html = ""
    if timeline:
        tl_items = ""
        for t in timeline:
            tl_items += (
                f'<div class="tl-item">'
                f'<div class="tl-date">{t.get("date", "")}</div>'
                f'<div class="tl-event">{t.get("event", "")}</div>'
                f'</div>'
            )
        timeline_html = (
            f'<div class="timeline-section">'
            f'<div class="section-title">{title_dec} 时间线 {title_dec}</div>'
            f'<div class="timeline-flow">{tl_items}</div>'
            f'</div>'
        )

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
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ background:#f5f5f5; font-family:"KaiTi","楷体","STKaiti","Microsoft YaHei","SimSun",serif; color:var(--text, #222); }}
body {{ display:flex; justify-content:center; padding:24px 0; }}
.page {{
    width:794px;
    min-height:auto;
    background:var(--bg, #fff);
    padding:40px 55px;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
}}
.header {{
    text-align:center;
    margin-bottom:28px;
}}
.header h1 {{
    font-size:28px;
    letter-spacing:5px;
    margin-bottom:10px;
    color:var(--primary, #222);
}}
.header .subtitle {{
    font-size:14px;
    color:var(--muted, #666);
}}
.divider-wrap {{
    margin: 12px auto;
    max-width:400px;
}}
.branches-grid {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:16px;
    margin-bottom:24px;
}}
.branch-card {{
    border:1.5px dashed var(--border, #888);
    border-radius:12px;
    padding:14px 18px;
    background:var(--bg, #fff);
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
}}
.branch-card .branch-title {{
    font-size:16px;
    font-weight:bold;
    color:var(--primary, #222);
    letter-spacing:2px;
    padding-bottom:8px;
    border-bottom:1px solid var(--border, #ddd);
    margin-bottom:8px;
}}
.branch-points {{
    list-style:none;
    padding:0;
}}
.branch-point {{
    font-size:13px;
    color:var(--text, #333);
    line-height:1.6;
    padding:3px 0;
    border-bottom:1px dashed var(--border, #eee);
}}
.branch-point:last-child {{
    border-bottom:none;
}}
.timeline-section {{
    margin-bottom:24px;
}}
.section-title {{
    text-align:center;
    font-size:14px;
    font-weight:bold;
    color:var(--primary, #333);
    letter-spacing:3px;
    margin-bottom:16px;
}}
.timeline-flow {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}}
.tl-item {{
    display:flex;
    align-items:baseline;
    gap:8px;
    padding:6px 10px;
    border-left:2px solid var(--accent, #888);
}}
.tl-date {{
    font-size:12px;
    font-weight:bold;
    color:var(--primary, #222);
    white-space:nowrap;
}}
.tl-event {{
    font-size:12px;
    color:var(--text, #444);
    line-height:1.4;
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
    <div class="branches-grid">
        {branch_cards}
    </div>
    {timeline_html}
    {kp_html}
    {footer}
</div>
</body>
</html>"""
    return html
