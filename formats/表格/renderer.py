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

    table_html = ""
    for branch in branches:
        title = branch.get("title", "")
        points = branch.get("points", [])
        points_text = "、".join(points)
        table_html += f"""
            <tr>
                <td class="branch-title">{title}</td>
                <td class="branch-points">{points_text}</td>
            </tr>"""

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
    padding:40px 55px;
}}
.header {{
    text-align:center;
    margin-bottom:24px;
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
table {{
    width:100%;
    border-collapse:collapse;
}}
th, td {{
    border:1.5px dashed var(--border, #888);
    padding:10px 14px;
    text-align:left;
    font-size:13px;
    word-break:break-word;
}}
th {{
    background:var(--light-bg, #f0f0f0);
    font-weight:bold;
    letter-spacing:2px;
    color:var(--primary, #333);
    font-size:14px;
}}
.branch-title {{
    font-weight:bold;
    font-size:14px;
    letter-spacing:1px;
    color:var(--primary, #333);
    white-space:nowrap;
}}
.branch-points {{
    color:var(--text, #333);
    line-height:1.7;
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
    <table>
        <thead>
            <tr>
                <th>分支</th>
                <th>要点</th>
            </tr>
        </thead>
        <tbody>
            {table_html}
        </tbody>
    </table>
    {kp_html}
    {footer}
</div>
</body>
</html>"""
    return html
