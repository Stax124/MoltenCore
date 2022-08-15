import logging

from db import generate_engine, get_session
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from watchdog.events import (
    FileModifiedEvent,
    FileSystemEventHandler,
    LoggingEventHandler,
)
from watchdog.observers import Observer

engine = generate_engine()
db = get_session(engine)

logger = logging.getLogger(__name__)


class TaskHandler(FileSystemEventHandler):
    def __init__(self):
        pass

    def on_modified(self, event: FileModifiedEvent):
        with open("test.txt", "a") as f:
            f.write(str(event.src_path) + " " + str(event.event_type))
        logger.debug(f"{event.src_path} modified")


class Tasks(commands.Cog):
    "Tasks"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.handler, path="config")
        logger.debug("Watchdog observer starting")
        self.observer.start()
        logger.debug("Watchdog observer started")

    # TODO - Port all reconnect logic and tasks


def setup(bot):
    bot.add_cog(Tasks(bot))
