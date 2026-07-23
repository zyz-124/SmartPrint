from core.theme import theme_css_vars
from core.decorations import (
    divider_html, title_ornament,
    shared_css, decoration_css, student_info_html, footer_html,
    knowledge_panel_html, knowledge_panel_css, base_page_css,
)


def render_html(data, **fmt_opts):
    theme = fmt_opts.get("theme", "素雅灰")
    style = fmt_opts.get("style", "简约几何")

    center = data.get("center", "")
    subtitle = data.get("subtitle", "")
    subject = data.get("subject", "")
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

    items_html = ""
    for i, t in enumerate(timeline):
        date_str = t.get("date", "")
        event_str = t.get("event", "")
        side = "left" if i % 2 == 0 else "right"
        items_html += f"""
        <div class="item {side}">
            <div class="date">{date_str}</div>
            <div class="dot"></div>
            <div class="event">{event_str}</div>
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
.timeline {{
    position:relative;
    padding:10px 0;
}}
.timeline::before {{
    content:"";
    position:absolute;
    left:0;
    right:0;
    top:50%;
    height:2px;
    background:var(--border, #888);
    transform:translateY(-50%);
}}
.item {{
    display:flex;
    align-items:center;
    position:relative;
    width:50%;
    padding:12px 20px;
}}
.item.left {{
    left:0;
    flex-direction:row;
}}
.item.right {{
    left:50%;
    flex-direction:row-reverse;
}}
.dot {{
    width:12px;
    height:12px;
    border:2px solid var(--primary, #333);
    border-radius:50%;
    background:var(--bg, #fff);
    position:absolute;
    z-index:2;
}}
.item.left .dot {{
    right:0;
}}
.item.right .dot {{
    left:0;
}}
.date {{
    width:45%;
    font-size:14px;
    font-weight:bold;
    letter-spacing:1px;
    color:var(--primary, #222);
}}
.item.left .date {{
    text-align:right;
    padding-right:16px;
}}
.item.right .date {{
    text-align:left;
    padding-left:16px;
}}
.event {{
    width:45%;
    font-size:13px;
    color:var(--text, #333);
    line-height:1.5;
}}
.item.left .event {{
    text-align:left;
    padding-left:16px;
}}
.item.right .event {{
    text-align:right;
    padding-right:16px;
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
    <div class="timeline">
        {items_html}
    </div>
    {kp_html}
    {footer}
</div>
</body>
</html>"""
    return html
