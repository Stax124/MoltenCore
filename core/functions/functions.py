import os
import sys
from datetime import timedelta


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


def convert_timedelta(duration: timedelta):
    "Converts a timedelta into a human-readable string"

    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if days > 0:
        return f"{days} day{'s' if days != 1 else ''} {hours} hour{'s' if days != 1 else ''}"
    elif hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
    else:
        return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"
