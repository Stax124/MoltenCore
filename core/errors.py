from datetime import datetime
from discord.ext.commands import Context, Cog
from discord import User, Member, Guild


class Error:
    def __init__(self, command: str, ctx: Context) -> None:
        self.command: str = command
        self.ctx: Context = ctx
        self.time: datetime = datetime.now()
        self.args = ctx.args
        self.called_by: User | Member = ctx.author
        self.cog: Cog | None = ctx.cog
        self.guild: Guild | None = ctx.guild


class Errors:
    def __init__(self) -> None:
        self.errors: list[Error]

    def add(self, name: str, ctx: Context):
        self.errors.append(Error(name, ctx))
