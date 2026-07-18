from core.theme import theme_css_vars
from core.decorations import (
    divider_html, title_ornament,
    shared_css, decoration_css, student_info_html, footer_html,
    knowledge_panel_html, knowledge_panel_css,
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
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ background:#f5f5f5; font-family:"KaiTi","楷体","STKaiti","Microsoft YaHei","SimSun",serif; color:var(--text, #222); }}
body {{ display:flex; justify-content:center; padding:24px 0; }}
.page {{
    width:794px;
    min-height:auto;
    background:var(--bg, #fff);
    position:relative;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
    padding:40px 60px;
}}
.header {{
    text-align:center;
    margin-bottom:30px;
}}
.header h1 {{
    font-size:28px;
    letter-spacing:4px;
    margin-bottom:8px;
    color:var(--primary, #222);
}}
.header .subtitle {{
    font-size:14px;
    color:var(--muted, #666);
}}
.divider-wrap {{
    margin: 10px auto;
    max-width:500px;
}}
.timeline {{
    position:relative;
    padding:10px 0;
}}
.timeline::before {{
    content:"";
    position:absolute;
    left:50%;
    top:0;
    bottom:0;
    width:2px;
    background:var(--border, #888);
    transform:translateX(-50%);
}}
.item {{
    display:flex;
    align-items:center;
    margin-bottom:20px;
    position:relative;
}}
.item.left {{
    flex-direction:row;
}}
.item.right {{
    flex-direction:row-reverse;
}}
.dot {{
    width:12px;
    height:12px;
    border:2px solid var(--primary, #333);
    border-radius:50%;
    background:var(--bg, #fff);
    position:absolute;
    left:50%;
    transform:translateX(-50%);
    z-index:2;
}}
.date {{
    width:42%;
    font-size:14px;
    font-weight:bold;
    letter-spacing:1px;
    color:var(--primary, #222);
}}
.item.left .date {{
    text-align:right;
    padding-right:24px;
}}
.item.right .date {{
    text-align:left;
    padding-left:24px;
}}
.event {{
    width:42%;
    font-size:13px;
    color:var(--text, #333);
    line-height:1.5;
}}
.item.left .event {{
    text-align:left;
    padding-left:24px;
}}
.item.right .event {{
    text-align:right;
    padding-right:24px;
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
