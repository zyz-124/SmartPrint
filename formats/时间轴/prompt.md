在项目目录 subjects/{subject}/ 下创建 {topic}.json，格式如下：

{
  "subject": "{subject}",
  "center": "{topic}",
  "subtitle": "（课本版本信息，如 人教版七年级下册 第5课）",
  "branches": [
    {"title": "阶段标题", "points": [
      "该阶段背景或原因的详细描述",
      "关键事件的过程说明"
    ]}
  ],
  "timeline": [
    {"date": "具体时间（年/月/日）", "event": "事件的完整描述，包含人物、地点、意义"}
  ],
  "key_concepts": [
    {"term": "核心概念", "explain": "准确定义或解释"}
  ],
  "key_figures": [
    {"name": "人物姓名", "title": "身份", "contribution": "主要事迹或贡献"}
  ],
  "marginalia": [
    "课本旁注、背景补充、比较辨析等"
  ]
}

规则：
- 10～15个时间节点，按时间顺序排列
- 每个事件描述25～40个字，包含完整的"谁+在哪+做了什么+结果"
- 时间节点尽量精确到年，重要的精确到月或日
- branches按时间阶段划分（如"起义背景""斗争过程""最终结局"），3～5个
- key_concepts：时间轴涉及的核心概念，4～6个
- key_figures：时间轴中的关键人物，4～6个
- marginalia：课本对这段历史的补充说明，3～5条
- 内容准确，严格依照课本表述
- 只输出 JSON，不要解释
