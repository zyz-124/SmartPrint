"""4种提示词风格 × 4种格式 = 16套提示词模板."""

PROMPT_STYLES = ["简约", "严谨", "丰富", "逻辑", "要点清单"]

# ═══════════════════════════════════════════════════════
#   通用结构约束（每种格式都会附加）
# ═══════════════════════════════════════════════════════
STRUCTURE_RULES = """\
【输出规则】
- 只输出合法JSON，不要任何解释、标题或markdown代码块
- 所有字段必须齐全，缺少数据时填空列表 []，不允许省略字段
- 中文内容，学科专业术语保持准确
- 每个 point 是完整的一句话（15-50字）
- 不要出现"考试重点""必考"等与考试相关的词语

【参考图片 reference_images】
- 从网上搜索与主题相关的参考图片，URL 必须是可直接访问的图片链接
- 优先使用维基百科、百度百科、百科知识类网站的图片
- 每张图片附带 caption 说明，中文
- 图片数量 2-6 张，覆盖不同知识点
- 找不到合适的图片时填空列表 []"""

# ═══════════════════════════════════════════════════════
#   四种风格的写作指令
# ═══════════════════════════════════════════════════════
STYLE_INSTRUCTIONS = {
    "简约": (
        "【风格：简约】\n"
        "用最精炼的语言提炼核心知识。每个分支只保留最本质的要点，"
        "避免冗余信息。一般生成3个分支，每分支2-3个要点。\n"
        "要点力求一句话说清一个知识点，不展开解释。"
    ),
    "严谨": (
        "【风格：严谨】\n"
        "以教材和学术规范为准绳，使用学科专业术语，表述准确、"
        "逻辑严密。一般生成4个分支，每分支3-4个要点。\n"
        "每个要点需有明确的定义、条件或因果关系，不使用口语化表达。"
    ),
    "丰富": (
        "【风格：丰富】\n"
        "尽可能全面覆盖知识点，包括背景、过程、影响、评价等维度。"
        "一般生成5个分支，每分支3-5个要点。\n"
        "在核心知识之外补充关联知识、延伸解读和实际应用案例。"
    ),
    "逻辑": (
        "【风格：逻辑】\n"
        "以因果链、对比关系或推理过程为主线组织知识。分支之间有"
        "递进或因果关系，每个分支内部也是层层推导。\n"
        "一般生成4个分支，每分支3-4个要点。"
        "要点之间应体现「因为…所以…」「前提→结论」「对比A与B」等逻辑结构。"
    ),
    "要点清单": (
        "【风格：要点清单】\n"
        "将知识点拆解为尽量多的独立条目，每个分支只放一个最精炼的要点。\n"
        "一般生成8-12个分支，每分支仅1个要点（一句话，10-25字）。\n"
        "追求覆盖面广、一目了然，适合快速浏览和查漏补缺。"
    ),
}

# ═══════════════════════════════════════════════════════
#   四种格式的完整 JSON schema（与 renderer 期望字段对齐）
# ═══════════════════════════════════════════════════════
#
#   所有格式共享的顶层字段：
#     subject    — 学科名称（字符串）
#     center     — 主题名称（字符串）
#     subtitle   — 课本版本信息（字符串）
#     key_concepts  — 核心概念列表（可空）
#     key_figures   — 关键人物列表（可空）
#     marginalia    — 知识拓展列表（可空）
#
#   各格式特有字段见下方 schema。
# ═══════════════════════════════════════════════════════

FORMAT_SCHEMAS = {
    "思维导图": """\
JSON结构（严格按此格式输出，所有字段必须存在）：
{
  "subject": "学科名",
  "center": "主题名",
  "subtitle": "课本版本信息，如 人教版八年级上册 第8课",
  "centerPosition": "center",
  "branches": [
    {
      "title": "分支标题",
      "points": ["要点1（完整一句话）", "要点2"]
    }
  ],
  "timeline": [
    { "date": "年份或时期", "event": "事件描述" }
  ],
  "key_concepts": [
    { "term": "核心概念", "explain": "准确定义，20字左右" }
  ],
  "key_figures": [
    { "name": "人物姓名", "title": "身份头衔", "contribution": "主要贡献" }
  ],
  "marginalia": ["补充说明或知识拓展"],
  "reference_images": [
    { "url": "https://example.com/image.jpg", "caption": "图片说明" }
  ]
}
说明：branches 3-5个，每个2-4个要点；timeline 按时间顺序（理科可用 []）；key_concepts 3-6个；key_figures 2-4个；marginalia 2-4条；reference_images 2-6张，搜索网上相关图片 URL。""",

    "表格": """\
JSON结构（严格按此格式输出，所有字段必须存在）：
{
  "subject": "学科名",
  "center": "主题名",
  "subtitle": "课本版本信息，如 人教版必修一 第3章",
  "branches": [
    {
      "title": "类别/维度",
      "points": ["条目1：说明", "条目2：说明"]
    }
  ],
  "timeline": [],
  "key_concepts": [
    { "term": "核心术语", "explain": "准确定义" }
  ],
  "key_figures": [
    { "name": "人物姓名", "title": "身份头衔", "contribution": "主要贡献" }
  ],
  "marginalia": ["补充说明或知识拓展"],
  "reference_images": [
    { "url": "https://example.com/image.jpg", "caption": "图片说明" }
  ]
}
说明：branches 4-8个，每个3-5个要点；key_concepts 3-6个；key_figures 若无相关人物填 []；marginalia 2-4条；reference_images 2-6张。""",

    "时间轴": """\
JSON结构（严格按此格式输出，所有字段必须存在）：
{
  "subject": "学科名",
  "center": "主题名",
  "subtitle": "课本版本信息，如 人教版七年级下册 第5课",
  "branches": [
    {
      "title": "阶段标题（如：起义背景、斗争过程）",
      "points": ["该阶段概述1", "该阶段概述2"]
    }
  ],
  "timeline": [
    { "date": "具体时间（年/月/日）", "event": "事件完整描述，含人物地点意义" }
  ],
  "key_concepts": [
    { "term": "核心概念", "explain": "准确定义" }
  ],
  "key_figures": [
    { "name": "人物姓名", "title": "身份", "contribution": "主要事迹" }
  ],
  "marginalia": ["补充说明或背景知识"],
  "reference_images": [
    { "url": "https://example.com/image.jpg", "caption": "图片说明" }
  ]
}
说明：timeline 至少8个节点，按时间先后排列；branches 3-5个阶段；key_concepts 3-5个；key_figures 3-5个；marginalia 2-4条；reference_images 2-6张。""",

    "大纲": """\
JSON结构（严格按此格式输出，所有字段必须存在）：
{
  "subject": "学科名",
  "center": "主题名",
  "subtitle": "课本版本信息，如 人教版必修二 第4单元",
  "branches": [
    {
      "title": "一级标题（课本小节名）",
      "points": [
        "二级要点：该节第一个重要知识点的完整描述",
        "二级要点：第二个知识点"
      ]
    }
  ],
  "timeline": [],
  "key_concepts": [
    { "term": "核心术语", "explain": "课本定义或标准解释" }
  ],
  "key_figures": [
    { "name": "人物姓名", "title": "身份头衔", "contribution": "主要贡献" }
  ],
  "marginalia": ["课本旁注、知识拓展、易混辨析等补充内容"],
  "reference_images": [
    { "url": "https://example.com/image.jpg", "caption": "图片说明" }
  ]
}
说明：branches 4-8个，每个3-5个要点；key_concepts 4-8个；key_figures 若无相关人物填 []；marginalia 3-5条；reference_images 2-6张。""",
}


# ═══════════════════════════════════════════════════════
#   对外接口
# ═══════════════════════════════════════════════════════
def build_prompt(subject: str, topic: str, fmt: str, style: str = "简约") -> str:
    """拼装完整提示词：学科背景 + 风格指令 + 格式JSON结构 + 规则."""
    parts = [
        f"为「{subject}」学科整理「{topic}」的知识，生成可直接渲染的知识卡片数据。",
        "",
        STYLE_INSTRUCTIONS.get(style, STYLE_INSTRUCTIONS["简约"]),
        "",
        FORMAT_SCHEMAS.get(fmt, FORMAT_SCHEMAS["思维导图"]),
        "",
        STRUCTURE_RULES,
    ]
    return "\n".join(parts)
