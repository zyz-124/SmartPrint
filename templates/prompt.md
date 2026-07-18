在项目目录 subjects/{subject}/ 下创建 {topic}.json，格式如下：

{
  "subject": "{subject}",
  "center": "{topic}",
  "subtitle": "（简短副标题，如年代、别称）",
  "branches": [
    {"title": "分支1标题", "points": ["要点1", "要点2"]}
  ],
  "timeline": [
    {"date": "年份", "event": "事件"}
  ]
}

规则：
- 6个分支，每分支2～3个要点，每个要点不超过10个字
- 有明确时间线则填，没有可省略
- 内容准确，适合手绘到A4纸上
- 只输出 JSON，不要解释
