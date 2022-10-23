import importlib
import logging
import inspect
import os
from pathlib import Path

logger = logging.getLogger(__name__)

permissions = {"database": ["sqlmodel", "db", "alembic"]}

forbidden = tuple([permissions[i] for i in [j for j in permissions.keys()]])


def secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    "Check if the module is allowed to be imported by plugin (or other module)"

    frame = inspect.currentframe()
    previous_frame = frame.f_back if frame else None
    file = Path(previous_frame.f_code.co_filename).resolve() if previous_frame else ""

    bot_path = (
        Path(os.path.abspath(__file__)).parents[2].resolve()
        if Path(os.path.abspath(__file__)).parents.__len__() > 2
        else None
    )

    if file and bot_path:
        try:
            rel_path = file.relative_to(bot_path)
            logger.debug(f"Importing {name} from {rel_path}")
        except ValueError:
            pass

    # TODO: Finish verification layer
    frommodule = globals["__name__"] if globals else None
    if name == "B" and frommodule != "C":
        raise ImportError("module '%s' is restricted." % name)

    return importlib.__import__(name, globals, locals, fromlist, level)


__builtins__["__import__"] = secure_importer
