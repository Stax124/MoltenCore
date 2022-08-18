import logging

from db import generate_engine, get_session
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot

engine = generate_engine()
db = get_session(engine)

logger = logging.getLogger(__name__)


class Tasks(commands.Cog):
    "Tasks"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    # TODO - Port all reconnect logic and tasks


async def setup(bot):
    await bot.add_cog(Tasks(bot))
