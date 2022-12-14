import logging
from typing import Optional

from coloredlogs import install as install_coloredlogs

from core.structures.const import loglevels


def install_logger(file: Optional[str], logging_arg: str):
    if file:
        logging.basicConfig(
            level=loglevels[logging_arg],
            handlers=[logging.FileHandler(file, "w", "utf-8")],
            format="%(levelname)s | %(asctime)s | %(name)s |->| %(message)s",
            datefmt=r"%H:%M:%S",
        )

    # Coloring the logs
    install_coloredlogs(
        level=loglevels[logging_arg],
        fmt="%(levelname)s | %(asctime)s | %(name)s |->| %(message)s",
        datefmt=r"%H:%M:%S",
        reconfigure=False,
    )
