"""AI 模块 — 通过 OpenAI 兼容 API 生成知识库 JSON"""

import json
import os
import re
import ssl
import urllib.request
import urllib.error

from config import API_CONFIG_PATH, FORMATS_DIR
from core.format_manager import load_prompt


DEFAULT_CONFIG = {
    "endpoint": "https://api.openai.com/v1/chat/completions",
    "key": "",
    "model": "gpt-4o-mini",
    "temperature": 0.3,
    "max_tokens": 4096,
}


def load_config():
    if os.path.isfile(API_CONFIG_PATH):
        with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(saved)
        return cfg
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    os.makedirs(os.path.dirname(API_CONFIG_PATH), exist_ok=True)
    with open(API_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def test_connection(cfg):
    payload = {
        "model": cfg["model"],
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5,
    }
    _call_api(cfg, payload)
    return True


def generate_json(subject, topic, fmt, cfg, style=None):
    prompt = load_prompt(fmt, subject, topic, style=style)
    prompt += "\n\n只输出合法 JSON，不要任何解释、注释或 markdown 标记。"

    payload = {
        "model": cfg["model"],
        "messages": [
            {"role": "system", "content": "你是一个专业的知识整理助手。用户会给你一个提示词模板，你需要严格按照模板的 JSON 格式输出内容。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": cfg["temperature"],
        "max_tokens": cfg["max_tokens"],
    }

    raw_text = _call_api(cfg, payload)
    return _parse_json(raw_text)


def _call_api(cfg, payload):
    endpoint = cfg["endpoint"].rstrip("/")
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg['key']}",
        },
        method="POST",
    )

    ctx = ssl.create_default_context()

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API 错误 {e.code}: {err_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"连接失败: {e.reason}")

    if "error" in body:
        raise RuntimeError(f"API 返回错误: {body['error']}")

    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"API 返回格式异常: {body}")


def _parse_json(text):
    text = text.strip()

    m = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()

    decoder = json.JSONDecoder()

    try:
        result, _ = decoder.raw_decode(text)
        return result
    except (json.JSONDecodeError, ValueError):
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            result, _ = decoder.raw_decode(text[start:])
            return result
        except (json.JSONDecodeError, ValueError):
            pass

    raise ValueError(f"无法解析 JSON:\n{text[:500]}")
