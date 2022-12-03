import os
import sys
from pathlib import Path


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
