import os
import webbrowser
from core.knowledge import load_knowledge
from core.renderer import render_html
from core.format_manager import load_prompt
from config import OUTPUT_DIR, DEFAULT_FORMAT


def run_mode_a(subject, topic, fmt=DEFAULT_FORMAT):
    text = load_prompt(fmt, subject, topic)
    print(text)


def run_mode_b(json_path, fmt=DEFAULT_FORMAT, **fmt_opts):
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"JSON 文件不存在: {json_path}")
    data = load_knowledge(json_path)
    html = render_html(data, fmt=fmt, **fmt_opts)

    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    center = data.get("center", "output")
    subject = data.get("subject", "")
    filename = f"{subject}_{center}.html" if subject else f"{center}.html"
    out_path = os.path.join(OUTPUT_DIR, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已生成: {out_path}")
    webbrowser.open("file:///" + os.path.abspath(out_path).replace("\\", "/"))
