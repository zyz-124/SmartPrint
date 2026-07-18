import importlib.util
import os

from config import FORMATS_DIR


def discover_formats():
    """扫描 formats/ 目录，返回所有可用格式名列表"""
    if not os.path.isdir(FORMATS_DIR):
        return []

    result = []
    for name in sorted(os.listdir(FORMATS_DIR)):
        fmt_dir = os.path.join(FORMATS_DIR, name)
        if not os.path.isdir(fmt_dir):
            continue
        prompt_path = os.path.join(fmt_dir, "prompt.md")
        renderer_path = os.path.join(fmt_dir, "renderer.py")
        if os.path.isfile(prompt_path) and os.path.isfile(renderer_path):
            result.append(name)
    return result


def _format_dir(fmt):
    fmt_dir = os.path.join(FORMATS_DIR, fmt)
    if not os.path.isdir(fmt_dir):
        raise FileNotFoundError(f"格式不存在: {fmt} ({fmt_dir})")
    return fmt_dir


def load_prompt(fmt, subject, topic, style=None):
    """读取提示词模板并替换占位符。

    style 为 None 时读取原始 prompt.md（向后兼容）；
    style 为 "简约"/"严谨"/"丰富"/"逻辑" 时使用新模板系统。
    """
    if style is not None:
        from core.prompts import build_prompt
        return build_prompt(subject, topic, fmt, style)

    fmt_dir = _format_dir(fmt)
    prompt_path = os.path.join(fmt_dir, "prompt.md")
    if not os.path.isfile(prompt_path):
        raise FileNotFoundError(f"提示词模板不存在: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{subject}", subject).replace("{topic}", topic)


def load_renderer(fmt):
    """动态加载指定格式的 renderer.py，返回其 render_html 函数"""
    fmt_dir = _format_dir(fmt)
    renderer_path = os.path.join(fmt_dir, "renderer.py")
    if not os.path.isfile(renderer_path):
        raise FileNotFoundError(f"渲染器不存在: {renderer_path}")

    module_name = f"formats_dynamic.{fmt}.renderer"
    spec = importlib.util.spec_from_file_location(module_name, renderer_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "render_html"):
        raise AttributeError(f"格式 '{fmt}' 的 renderer.py 未定义 render_html 函数")

    return module.render_html
