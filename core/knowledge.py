import json


def load_knowledge(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
