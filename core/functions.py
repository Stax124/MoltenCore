import json
import os
import sys


def is_in_virtualenv() -> bool:
    return sys.prefix != sys.base_prefix


def get_extensions() -> list[str]:
    "Search for all primary modules"

    extensions = [
        "extensions." + i.replace(".py", "")
        for i in os.listdir("extensions")
        if i.endswith(".py") and i != "core.py"
    ]

    return extensions


def generate_necessarry_files():
    if not os.path.exists("plugins"):
        os.makedirs("plugins")
    if not os.path.exists("config/tasks.json"):
        os.makedirs("config", exist_ok=True)
        with open("config/tasks.json", "w") as f:
            json.dump({}, f)
