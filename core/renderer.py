from config import DEFAULT_FORMAT
from core.format_manager import load_renderer


def render_html(data, fmt=DEFAULT_FORMAT, **fmt_opts):
    """按格式名代理渲染，动态加载对应 formats/<fmt>/renderer.py 中的 render_html"""
    renderer_fn = load_renderer(fmt)
    return renderer_fn(data, **fmt_opts)
