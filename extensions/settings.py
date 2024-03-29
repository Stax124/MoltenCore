import logging
from typing import Union

import discord
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.ext.commands.context import Context

from core.bot.bot import ModularBot
from core.functions.confirm import confirm
from models.config import Config
from models.guild import Guild

logger = logging.getLogger(__name__)


class Settings(commands.Cog):
    "Settings"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    @commands.hybrid_command(
        name="prefix", help="Change the prefix for the current guild"
    )
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        if await confirm(self.bot, ctx, message=f"Set prefix to `{prefix}` ?"):

            # Change prefix in database
            if ctx.guild is not None:
                if (
                    self.bot.database.query(Guild).filter_by(id=ctx.guild.id).first()
                    is not None
                ):
                    logger.info(
                        f"Updating prefix for guild {ctx.guild.name} to `{prefix}`"
                    )
                    self.bot.database.query(Guild).filter_by(id=ctx.guild.id).update(
                        {Guild.prefix: prefix}
                    )
                    self.bot.database.commit()

    @commands.hybrid_command(name="pause", help="Pauses all command executions")
    @commands.is_owner()
    async def pause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Pause process ?")
        if not confirmed:
            return

        embed = discord.Embed(colour=0x00FF00, description="✅ Paused...")
        embed.set_author(name="Pause", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

        config: Union[Config, None] = self.bot.database.query(Config).first()

        if config:
            config.paused = True
            self.bot.database.commit()

            logger.info("Paused...")

            await self.bot.change_presence(
                activity=discord.Game(name="Paused"), status=Status.do_not_disturb
            )
        else:
            embed = discord.Embed(
                colour=0xFF0000, description="❌ Error... Config not found in database"
            )
            embed.set_author(name="Pause", icon_url=self.bot.avatar_url)
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="unpause", help="Resumes all command executions")
    @commands.is_owner()
    async def unpause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Unpause process ?")
        if not confirmed:
            return

        embed = discord.Embed(colour=0x00FF00, description="✅ Unpaused...")
        embed.set_author(name="Unpause", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

        config: Union[Config, None] = self.bot.database.query(Config).first()

        if config:
            config.paused = False
            self.bot.database.commit()

            logger.info("Unpaused...")

            await self.bot.change_presence(
                activity=Activity(name="commands", type=ActivityType.listening)
            )
        else:
            embed = discord.Embed(
                colour=0xFF0000, description="❌ Error... Config not found in database"
            )
            embed.set_author(name="Pause", icon_url=self.bot.avatar_url)
            await ctx.send(embed=embed)


async def setup(bot: ModularBot):
    await bot.add_cog(Settings(bot))
