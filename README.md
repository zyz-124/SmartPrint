# SmartPrint

AI 驱动的知识卡片排版工具 — 交作业神器

## 功能

- **4 种输出格式**：知识卡片（原思维导图）、表格、时间轴、大纲
- **4 套色彩主题**：素雅灰、沉稳蓝、清新绿、暖橙
- **4 套装饰风格**：简约几何、中式古典、自然花藤、学术边框
- **知识面板**：核心概念 + 关键人物 + 知识拓展
- **学生信息栏**：姓名 / 班级 / 学号 / 日期
- **零依赖**：纯 Python 标准库，无需安装任何第三方包
- **GUI 图形界面**：选学科→选主题→一键生成
- **插件架构**：`formats/` 目录下每个子文件夹 = 一种新格式

## 快速开始

```bash
# CLI 模式
python app.py --json subjects/历史/辛亥革命.json --format 思维导图

# GUI 模式
python gui.py

# 指定主题和风格
python app.py --json subjects/历史/辛亥革命.json --format 表格 --theme 暖橙 --style 中式古典

# 带学生信息
python app.py --json subjects/历史/辛亥革命.json --name 张三 --class "七年级1班" --sid "001" --date "2024-06-15"
```

## 输出格式

| 格式 | 说明 |
|------|------|
| 思维导图 | 两列卡片式知识布局 |
| 表格 | 行式知识对照表 |
| 时间轴 | 交替时间线 |
| 大纲 | 层级编号大纲 |

## 插件开发

在 `formats/` 下新建文件夹，包含两个文件即可：

```
formats/你的格式/
├── prompt.md      # 提示词模板（{subject} / {topic} 占位符）
└── renderer.py    # 渲染器，必须导出 render_html(data, **fmt_opts)
```

## 项目结构

```
SmartPrint/
├── app.py                  # CLI 入口
├── gui.py                  # GUI 入口
├── config.py               # 全局配置
├── core/
│   ├── theme.py            # 色彩主题
│   ├── decorations.py      # 装饰风格 + 知识面板
│   ├── renderer.py         # 渲染代理
│   ├── runner.py           # 运行模式
│   ├── knowledge.py        # JSON 加载
│   └── format_manager.py   # 插件发现/加载
├── formats/
│   ├── 思维导图/
│   ├── 表格/
│   ├── 时间轴/
│   └── 大纲/
└── subjects/               # 知识库 JSON 数据
```

## 许可证

MIT License
