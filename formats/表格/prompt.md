在项目目录 subjects/{subject}/ 下创建 {topic}.json，格式如下：

{
  "subject": "{subject}",
  "center": "{topic}",
  "subtitle": "（课本版本信息，如 人教版必修一 第3章）",
  "branches": [
    {"title": "知识模块标题", "points": [
      "该模块第一个要点，包含完整知识点描述",
      "第二个要点，补充说明或举例",
      "第三个要点，与其他知识点的联系",
      "第四个要点，应用或延伸"
    ]}
  ],
  "timeline": [],
  "key_concepts": [
    {"term": "核心术语", "explain": "准确定义，完整表述"}
  ],
  "key_figures": [
    {"name": "人物姓名", "title": "身份头衔", "contribution": "主要贡献或成就"}
  ],
  "marginalia": [
    "课本补充说明、知识拓展、易混辨析等"
  ],
  "reference_images": [
    {"url": "https://example.com/image.jpg", "caption": "图片说明"}
  ]
}

规则：
- 8～10个分支（知识模块），每分支4～6个要点
- 每个要点20～35个字，完整表达一个知识片段
- 按课本内容逻辑组织，覆盖该章节所有核心知识
- key_concepts：课本重点术语和定义，6～8个
- key_figures：涉及的重要人物（科学家/历史人物等），3～5个
- marginalia：课本边栏、知识卡片、小字内容，4～6条
- reference_images：搜索网上与主题相关的参考图片，2～6张
- 时间线按需填写（理科可省略）
- 内容准确，严格依照课本表述
- 只输出 JSON，不要解释
