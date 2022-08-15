import logging
from typing import Union

import discord
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.ext.commands.context import Context
from models.config import Config
from models.guild import Guild

from core.bot import ModularBot
from core.confirm import confirm


class Settings(commands.Cog):
    "Settings"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    @commands.command(name="version")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        await ctx.send(self.bot.__version__)

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        if await confirm(self.bot, ctx, message=f"Set prefix to `{prefix}` ?"):

            # Change prefix in database
            if ctx.guild is not None:
                if (
                    self.bot.database.query(Guild).filter_by(id=ctx.guild.id).first()
                    is not None
                ):
                    logging.info(
                        f"Updating prefix for guild {ctx.guild.name} to `{prefix}`"
                    )
                    self.bot.database.query(Guild).filter_by(id=ctx.guild.id).update(
                        {Guild.prefix: prefix}
                    )
                    self.bot.database.commit()

    @commands.command(name="pause", help="Show the bot, whos da boss: shutdown")
    @commands.is_owner()
    async def pause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Pause process ?")
        if not confirmed:
            return

        embed = discord.Embed(colour=0x00FF00, description="✅ Paused...")
        embed.set_author(name="Pause", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)

        config: Union[Config, None] = self.bot.database.query(Config).first()

        if config:
            config.paused = True
            self.bot.database.commit()

            logging.info("Paused...")

            await self.bot.change_presence(
                activity=discord.Game(name=f"Paused"), status=Status.do_not_disturb
            )
        else:
            embed = discord.Embed(
                colour=0xFF0000, description="❌ Error... Config not found in database"
            )
            embed.set_author(name="Pause", icon_url=self.bot.user.avatar_url.__str__())
            await ctx.send(embed=embed)

    @commands.command(name="unpause", help="Show the bot, whos da boss: shutdown")
    @commands.is_owner()
    async def unpause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Unpause process ?")
        if not confirmed:
            return

        embed = discord.Embed(colour=0x00FF00, description="✅ Unpaused...")
        embed.set_author(name="Unpause", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)

        config: Union[Config, None] = self.bot.database.query(Config).first()

        if config:
            config.paused = False
            self.bot.database.commit()

            logging.info("Unpaused...")

            await self.bot.change_presence(
                activity=Activity(name=f"commands", type=ActivityType.listening)
            )
        else:
            embed = discord.Embed(
                colour=0xFF0000, description="❌ Error... Config not found in database"
            )
            embed.set_author(name="Pause", icon_url=self.bot.user.avatar_url.__str__())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Settings(bot))
