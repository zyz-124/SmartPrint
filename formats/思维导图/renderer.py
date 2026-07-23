import random
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

    layout = random.randint(0, 7)
    is_split = layout in (2, 7)

    if is_split and len(branches) >= 2:
        mid = (len(branches) + 1) // 2
        left_branches = branches[:mid]
        right_branches = branches[mid:]
    else:
        left_branches = branches
        right_branches = []

    def build_branch(bi, b, side_cls=""):
        title = b.get("title", "")
        points = b.get("points", [])
        pts = ""
        for pi, p in enumerate(points):
            pts += f'<div class="point-card" data-branch="{bi}" data-idx="{pi}"><span class="bullet">{bullet_svg(style)}</span><span class="card-text">{p}</span></div>'
        return f'<div class="branch-group{side_cls}" data-branch="{bi}"><div class="branch-title-card" data-branch="{bi}"><span class="card-text">{title}</span></div><div class="branch-points">{pts}</div></div>'

    if is_split:
        left_html = ""
        for bi, b in enumerate(left_branches):
            left_html += build_branch(bi, b, " side-left")
        right_html = ""
        for bi, b in enumerate(right_branches):
            right_html += build_branch(mid + bi, b, " side-right")
        mm_inner = (
            f'<div class="mm-side left" id="leftSide">{left_html}</div>'
            f'<div class="mm-center"><div class="mm-center-card" id="centerCard">{center}</div></div>'
            f'<div class="mm-side right" id="rightSide">{right_html}</div>'
        )
    else:
        all_branches = ""
        for bi, b in enumerate(branches):
            all_branches += build_branch(bi, b)
        mm_inner = (
            f'<div class="mm-center"><div class="mm-center-card" id="centerCard">{center}</div></div>'
            f'<div class="mm-branches" id="branchesWrap">{all_branches}</div>'
        )

    timeline_html = ""
    if timeline:
        tl_items = ""
        for t in timeline:
            tl_items += f'<div class="tl-item"><div class="tl-date">{t.get("date", "")}</div><div class="tl-event">{t.get("event", "")}</div></div>'
        timeline_html = f'<div class="timeline-section"><div class="section-title">{title_dec} 时间线 {title_dec}</div><div class="timeline-flow">{tl_items}</div></div>'

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
* {{ box-sizing: border-box; }}
.divider-wrap {{ margin:12px auto; max-width:400px; }}

.mm-wrap {{ display:flex; gap:0; margin-top:20px; width:100%; }}
.mm-center {{ flex:0 0 auto; display:flex; align-items:center; justify-content:center; position:relative; }}
.mm-center-card {{
    width:180px; height:180px; display:flex; align-items:center; justify-content:center;
    background:var(--primary, #222); color:var(--bg, #fff); font-size:22px; font-weight:bold;
    letter-spacing:3px; border-radius:50%; text-align:center; cursor:grab; user-select:none;
    touch-action:none; position:relative; z-index:5;
    box-shadow:0 8px 32px rgba(0,0,0,0.18);
    animation: centerPulse 3s ease-in-out infinite;
}}
@keyframes centerPulse {{
    0%,100% {{ box-shadow:0 8px 32px rgba(0,0,0,0.18); transform:scale(1); }}
    50% {{ box-shadow:0 8px 48px rgba(0,0,0,0.28); transform:scale(1.03); }}
}}
.mm-branches {{ flex:1 1 auto; display:grid; gap:14px; align-content:start; }}
.mm-side {{ display:flex; flex-direction:column; gap:14px; }}
.mm-side.left {{ align-items:flex-end; }}
.mm-side.right {{ align-items:flex-start; }}

.branch-group {{ display:flex; flex-direction:column; gap:5px; position:relative; }}
.side-left {{ align-items:flex-end; }}
.side-left .branch-points {{ display:flex; flex-direction:column; align-items:flex-end; }}
.side-right {{ align-items:flex-start; }}
.side-right .branch-points {{ display:flex; flex-direction:column; align-items:flex-start; }}

.branch-title-card {{
    font-size:14px; font-weight:bold; color:var(--primary, #222); letter-spacing:1.5px;
    padding:7px 14px; border:2px solid var(--primary, #222); border-radius:10px;
    background:var(--light-bg, #f5f5f5); cursor:grab; user-select:none; touch-action:none;
    position:relative; z-index:5; white-space:nowrap;
}}
.point-card {{
    font-size:12px; color:var(--text, #333); line-height:1.5; padding:5px 10px;
    border:1.5px dashed var(--border, #888); border-radius:8px; background:var(--bg, #fff);
    cursor:grab; user-select:none; touch-action:none; position:relative; z-index:5; white-space:nowrap;
}}
.dragging {{
    cursor:grabbing !important; box-shadow:0 16px 48px rgba(0,0,0,0.25);
    border-color:var(--accent, #4a90d9) !important; border-style:solid !important; z-index:100 !important;
}}

/* === LAYOUTS === */
.layout-0 {{ flex-direction:row; align-items:center; }}
.layout-0 .mm-branches {{ grid-template-columns:1fr 1fr; }}

.layout-1 {{ flex-direction:row-reverse; align-items:center; }}
.layout-1 .mm-branches {{ grid-template-columns:1fr 1fr; }}

.layout-2 {{ flex-direction:row; align-items:center; }}

.layout-3 {{ flex-direction:column; align-items:center; }}
.layout-3 .mm-branches {{ grid-template-columns:1fr 1fr 1fr; }}

.layout-4 {{ flex-direction:column-reverse; align-items:center; }}
.layout-4 .mm-branches {{ grid-template-columns:1fr 1fr 1fr; }}

.layout-5 {{ flex-direction:row; align-items:center; }}
.layout-5 .mm-center-card {{ width:140px; height:140px; font-size:18px; }}
.layout-5 .mm-branches {{ grid-template-columns:1fr 1fr; }}

.layout-6 {{ flex-direction:row-reverse; align-items:center; }}
.layout-6 .mm-center-card {{ width:140px; height:140px; font-size:18px; }}
.layout-6 .mm-branches {{ grid-template-columns:1fr 1fr; }}

.layout-7 {{ flex-direction:row; align-items:center; justify-content:center; }}

.timeline-section {{ margin:16px 0 24px; }}
.section-title {{ text-align:center; font-size:14px; font-weight:bold; color:var(--primary, #333); letter-spacing:3px; margin-bottom:16px; }}
.timeline-flow {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }}
.tl-item {{ display:flex; align-items:baseline; gap:8px; padding:6px 10px; border-left:2px solid var(--accent, #888); }}
.tl-date {{ font-size:12px; font-weight:bold; color:var(--primary, #222); white-space:nowrap; }}
.tl-event {{ font-size:12px; color:var(--text, #444); line-height:1.4; }}

.conn-svg {{ position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:3; overflow:visible; }}
.conn-path {{ fill:none; stroke-linecap:round; }}
.conn-main {{ stroke:var(--primary, #333); stroke-width:2.5; stroke-dasharray:8 5; opacity:0.45; }}
.conn-branch {{ stroke:var(--border, #aaa); stroke-width:2; stroke-dasharray:6 4; opacity:0.55; }}
.conn-path {{ animation:flowDash 2s linear infinite; }}
@keyframes flowDash {{ to {{ stroke-dashoffset:-28; }} }}
</style>
</head>
<body>
<div class="page" id="canvas">
    <svg class="conn-svg" id="connSvg"></svg>
    <div class="top-bar">
        <div class="subject-label">{subject}</div>
        {student_html}
    </div>
    <div class="header">
        <h1>{title_dec} {center} {title_dec}</h1>
        <div class="subtitle">{subtitle}</div>
        <div class="divider-wrap">{divider}</div>
    </div>
    <div class="mm-wrap layout-{layout}" id="mmWrap">
        {mm_inner}
    </div>
    {timeline_html}
    {kp_html}
    {footer}
</div>
<script>
(function() {{
'use strict';

var canvas = document.getElementById('canvas');
var svg = document.getElementById('connSvg');
var centerCard = document.getElementById('centerCard');
var layout = {layout};
var isSplit = { 'true' if is_split else 'false' };
var cards = Array.prototype.slice.call(document.querySelectorAll('.branch-title-card, .point-card, .mm-center-card'));
var mainConns = [];
var subConns = [];
var NS = 'http://www.w3.org/2000/svg';

cards.forEach(function(c, i) {{
    c.style.opacity = '0';
    c.style.transform = 'translateY(18px) scale(0.95)';
    setTimeout(function() {{
        c.style.transition = 'opacity 0.5s cubic-bezier(.4,0,.2,1), transform 0.5s cubic-bezier(.4,0,.2,1)';
        c.style.opacity = '1';
        c.style.transform = 'translateY(0) scale(1)';
        setTimeout(function() {{ c.style.transition = ''; }}, 520);
    }}, 40 + i * 45);
}});

document.querySelectorAll('.branch-title-card').forEach(function(bt) {{
    var side = 'none';
    if (isSplit) {{
        var p = bt.closest('.mm-side');
        if (p) side = p.classList.contains('left') ? 'left' : 'right';
    }}
    mainConns.push({{ from: centerCard, to: bt, side: side }});
}});

document.querySelectorAll('.branch-group').forEach(function(g) {{
    var title = g.querySelector('.branch-title-card');
    var side = 'none';
    if (isSplit) {{
        var p = g.closest('.mm-side');
        if (p) side = p.classList.contains('left') ? 'left' : 'right';
    }}
    g.querySelectorAll('.point-card').forEach(function(pt) {{
        subConns.push({{ from: title, to: pt, side: side }});
    }});
}});

function makePath(cls) {{
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('class', 'conn-path ' + cls);
    svg.appendChild(p);
    return p;
}}
var mainPaths = mainConns.map(function() {{ return makePath('conn-main'); }});
var subPaths = subConns.map(function() {{ return makePath('conn-branch'); }});

function relPos(el) {{
    var er = el.getBoundingClientRect();
    var cr = canvas.getBoundingClientRect();
    return {{
        cx: er.left - cr.left + er.width / 2,
        top: er.top - cr.top,
        bottom: er.bottom - cr.top,
        cy: er.top - cr.top + er.height / 2,
        left: er.left - cr.left,
        right: er.right - cr.left,
        w: er.width,
        h: er.height
    }};
}}

function curve(x1, y1, x2, y2) {{
    var dx = x2 - x1, dy = y2 - y1;
    var dist = Math.sqrt(dx * dx + dy * dy);
    var t = Math.min(dist * 0.35, 70);
    return 'M' + x1 + ',' + y1 + ' C' + x1 + ',' + (y1 + t) + ' ' + x2 + ',' + (y2 - t) + ' ' + x2 + ',' + y2;
}}

function autoEdge(f, t) {{
    var dx = t.cx - f.cx, dy = t.cy - f.cy;
    var x1, y1, x2, y2;
    if (Math.abs(dy) > Math.abs(dx) * 0.3) {{
        y1 = dy > 0 ? f.bottom : f.top;
        x1 = f.cx;
        y2 = dy > 0 ? t.top : t.bottom;
        x2 = t.cx;
    }} else {{
        x1 = dx > 0 ? f.right : f.left;
        y1 = f.cy;
        x2 = dx > 0 ? t.left : t.right;
        y2 = t.cy;
    }}
    return [x1, y1, x2, y2];
}}

function drawAll() {{
    var i, c, f, t, e;
    for (i = 0; i < mainConns.length; i++) {{
        c = mainConns[i];
        f = relPos(c.from);
        t = relPos(c.to);
        if (isSplit) {{
            if (c.side === 'left') {{
                mainPaths[i].setAttribute('d', curve(f.left, f.cy, t.right, t.cy));
            }} else {{
                mainPaths[i].setAttribute('d', curve(f.right, f.cy, t.left, t.cy));
            }}
        }} else {{
            e = autoEdge(f, t);
            mainPaths[i].setAttribute('d', curve(e[0], e[1], e[2], e[3]));
        }}
    }}
    for (i = 0; i < subConns.length; i++) {{
        c = subConns[i];
        f = relPos(c.from);
        t = relPos(c.to);
        if (isSplit) {{
            if (c.side === 'left') {{
                subPaths[i].setAttribute('d', curve(f.left, f.cy, t.right, t.cy));
            }} else {{
                subPaths[i].setAttribute('d', curve(f.right, f.cy, t.left, t.cy));
            }}
        }} else {{
            e = autoEdge(f, t);
            subPaths[i].setAttribute('d', curve(e[0], e[1], e[2], e[3]));
        }}
    }}
}}

setTimeout(drawAll, 700);
window.addEventListener('resize', drawAll);

var dragEl = null, dsx = 0, dsy = 0, dox = 0, doy = 0, raf = null;
function pt(el) {{
    var t = el.style.transform;
    if (!t) return {{ x:0, y:0 }};
    var m = t.match(/translate\(\s*([-\d.]+)px[,\s]+([-\d.]+)px\s*\)/);
    return m ? {{ x:parseFloat(m[1]), y:parseFloat(m[2]) }} : {{ x:0, y:0 }};
}}
function onDown(e) {{
    var card = e.target.closest('.branch-title-card, .point-card, .mm-center-card');
    if (!card) return;
    e.preventDefault();
    var p = pt(card);
    dragEl = card; dsx = e.clientX; dsy = e.clientY; dox = p.x; doy = p.y;
    card.classList.add('dragging');
    card.style.transition = 'box-shadow 0.15s, border-color 0.15s';
}}
function onMove(e) {{
    if (!dragEl) return;
    dragEl.style.transform = 'translate(' + (e.clientX - dsx + dox) + 'px, ' + (e.clientY - dsy + doy) + 'px)';
    if (!raf) {{ raf = requestAnimationFrame(function() {{ drawAll(); raf = null; }}); }}
}}
function onUp() {{
    if (!dragEl) return;
    dragEl.classList.remove('dragging');
    dragEl.style.transition = '';
    dragEl = null;
    drawAll();
}}
canvas.addEventListener('mousedown', onDown);
window.addEventListener('mousemove', onMove);
window.addEventListener('mouseup', onUp);
canvas.addEventListener('touchstart', function(e) {{
    if (e.touches.length === 1) {{
        var t = e.touches[0], el = document.elementFromPoint(t.clientX, t.clientY);
        if (el) onDown({{ target:el, clientX:t.clientX, clientY:t.clientY, preventDefault:function(){{}} }});
    }}
}}, {{ passive:false }});
window.addEventListener('touchmove', function(e) {{
    if (dragEl && e.touches.length === 1) {{
        e.preventDefault();
        var t = e.touches[0];
        onMove({{ clientX:t.clientX, clientY:t.clientY }});
    }}
}}, {{ passive:false }});
window.addEventListener('touchend', onUp);

}})();
</script>
</body>
</html>"""
    return html
