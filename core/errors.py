import logging
from datetime import datetime
from typing import Callable

from discord import Guild, Member, User
from discord.ext.commands import Cog, Context

logger = logging.getLogger(__name__)


class Error:
    "Runtime error caused by the bot or any of his interactions."

    def __init__(self, command: str, ctx: Context) -> None:
        self.command: str = command
        self.ctx: Context = ctx
        self.time: datetime = datetime.now()
        self.args = ctx.args
        self.called_by: User | Member = ctx.author
        self.cog: Cog | None = ctx.cog
        self.guild: Guild | None = ctx.guild
        self.id: int = hash(self)


class Errors:
    def __init__(self) -> None:
        self.errors: list[Error] = []
        self.add_callbacks: list[Callable] = []

    def add(self, name: str, ctx: Context) -> None:
        "Adds an error to the errors list."
        error = Error(name, ctx)

        self.errors.append(error)
        for callback in self.add_callbacks:
            callback(error)

    def remove(self, id: int) -> None:
        "Removes an error from the errors list."
        for error in self.errors:
            if error.id == id:
                self.errors.remove(error)

    def clear(self) -> None:
        "Clears the errors list."
        self.errors.clear()
