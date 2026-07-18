import argparse
import json
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.runner import run_mode_a, run_mode_b
from config import DEFAULT_FORMAT, DEFAULT_THEME, DEFAULT_STYLE, OUTPUT_DIR
from core.theme import list_themes
from core.decorations import list_styles
from core.prompts import PROMPT_STYLES


def build_parser():
    parser = argparse.ArgumentParser(
        prog="SmartPrint",
        description="知识卡片排版工具",
    )
    parser.add_argument("--subject", help="学科名称，如 历史 / 地理")
    parser.add_argument("--topic", help="主题名称，如 辛亥革命")
    parser.add_argument("--json", dest="json_path", help="知识库 JSON 路径")
    parser.add_argument("--format", dest="fmt", default=DEFAULT_FORMAT,
                        help="输出格式（对应 formats/ 下的文件夹名），默认思维导图")
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
    parser.add_argument("--prompt-style", dest="prompt_style", default=None,
                        choices=PROMPT_STYLES,
                        help="提示词风格（简约/严谨/丰富/逻辑）")
    parser.add_argument("--ai", action="store_true",
                        help="使用 AI 生成 JSON（需要先配置 API）")
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

    if args.ai:
        if not args.subject or not args.topic:
            print("错误: --ai 模式需要 --subject 和 --topic")
            return 1

        from core.ai import load_config, generate_json

        cfg = load_config()
        if not cfg.get("key"):
            print("错误: 请先配置 API Key（编辑 api_config.json 或用 GUI 的 AI 设置）")
            return 1

        print(f"AI 生成中: {args.subject} / {args.topic} ...")
        try:
            data = generate_json(args.subject, args.topic, args.fmt, cfg,
                                 style=args.prompt_style)
        except Exception as e:
            print(f"错误: {e}")
            return 1

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"{args.subject}_{args.topic}.html"
        out_json = os.path.join(OUTPUT_DIR, f"{args.subject}_{args.topic}.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"JSON 已保存: {out_json}")

        run_mode_b(out_json, fmt=args.fmt, **fmt_opts)
        return 0

    if args.subject and args.topic:
        run_mode_a(args.subject, args.topic, fmt=args.fmt,
                   style=args.prompt_style)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
