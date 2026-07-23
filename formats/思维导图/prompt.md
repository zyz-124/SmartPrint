在项目目录 subjects/{subject}/ 下创建 {topic}.json，格式如下：

{
  "subject": "{subject}",
  "center": "{topic}",
  "subtitle": "（课本版本信息，如 人教版八年级上册 第8课）",
  "branches": [
    {"title": "小节标题", "points": [
      "该小节第一个要点，详细描述事件背景或原因",
      "第二个要点，包含时间地点人物等关键信息",
      "第三个要点，说明过程或变化",
      "第四个要点，补充细节或扩展知识"
    ]}
  ],
  "timeline": [
    {"date": "年份/日期", "event": "事件的详细描述，包含人物和地点"}
  ],
  "key_concepts": [
    {"term": "核心概念名称", "explain": "概念的准确定义，20字左右"}
  ],
  "key_figures": [
    {"name": "人物姓名", "title": "人物身份/头衔", "contribution": "该人物的主要贡献或事迹"}
  ],
  "marginalia": [
    "课本注释或拓展知识，如背景补充、易混辨析等"
  ],
  "reference_images": [
    {"url": "https://example.com/image.jpg", "caption": "图片说明"}
  ]
}

规则：
- 8～10个分支（小节），每分支3～5个要点
- 每个要点15～30个字，要完整表述一个知识点
- 按课本章节结构组织，覆盖该课所有重点内容
- key_concepts：提取课本加粗或框住的术语概念，4～6个
- key_figures：课本提到的重要人物，3～5个
- marginalia：课本旁注/小字/资料卡内容，3～5条
- 时间线节点8～12个，每个事件描述完整
- reference_images：搜索网上与主题相关的参考图片，2～6张，URL 必须是可直接访问的图片链接，优先百科类网站
- 内容准确，严格依照课本原文表述
- 只输出 JSON，不要解释
