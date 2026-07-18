import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.runner import run_mode_a, run_mode_b
from config import DEFAULT_FORMAT, DEFAULT_THEME, DEFAULT_STYLE
from core.theme import list_themes
from core.decorations import list_styles


def build_parser():
    parser = argparse.ArgumentParser(
        prog="SubjectDraw",
        description="A4 手绘知识图谱生成工具",
    )
    parser.add_argument("--subject", help="学科名称，如 历史 / 地理")
    parser.add_argument("--topic", help="主题名称，如 辛亥革命")
    parser.add_argument("--json", dest="json_path", help="知识库 JSON 路径")
    parser.add_argument("--format", dest="fmt", default=DEFAULT_FORMAT,
                        help="图谱格式名称（对应 formats/ 下的文件夹名），默认思维导图")
    parser.add_argument("--theme", default=DEFAULT_THEME,
                        choices=list_themes(),
                        help="色彩主题，默认素雅灰")
    parser.add_argument("--style", default=DEFAULT_STYLE,
                        choices=list_styles(),
                        help="装饰风格，默认简约几何")
    parser.add_argument("--name", default="", help="学生姓名")
    parser.add_argument("--class", dest="cls", default="", help="班级")
    parser.add_argument("--sid", default="", help="学号")
    parser.add_argument("--date", default="", help="日期")
    parser.add_argument("--watermark", default="", help="水印文字")
    parser.add_argument("--gui", action="store_true", help="启动图形界面")
    return parser


def _build_fmt_opts(args):
    return dict(
        theme=args.theme,
        style=args.style,
        student_name=args.name,
        cls=args.cls,
        student_id=args.sid,
        date=args.date,
        watermark=args.watermark,
    )


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.gui:
        import gui
        gui.run()
        return 0

    fmt_opts = _build_fmt_opts(args)

    if args.json_path:
        run_mode_b(args.json_path, fmt=args.fmt, **fmt_opts)
        return 0

    if args.subject and args.topic:
        run_mode_a(args.subject, args.topic, fmt=args.fmt)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
