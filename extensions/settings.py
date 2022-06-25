import logging

import discord
from core.functions import confirm
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
from main import ModularBot
from models.guild import Guild


class Settings(commands.Cog):
    "Settings"

    def __init__(self, bot: ModularBot):
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
                if self.bot.database.query(Guild).filter_by(id=ctx.guild.id).first() is not None:
                    logging.info(
                        f"Updating prefix for guild {ctx.guild.name} to `{prefix}`")
                    self.bot.database.query(Guild).filter_by(
                        id=ctx.guild.id).update({Guild.prefix: prefix})
                    self.bot.database.commit()

    
    @commands.command(name="pause", help="Show the bot, whos da boss: shutdown", pass_context=True) # type: ignore
    @commands.is_owner()
    async def pause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Pause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Paused..."
        )
        embed.set_author(name="Pause", icon_url=self.bot.avatar_url)  # type: ignore
        await ctx.send(embed=embed)
        self.bot.paused = True
        logging.info("Paused...")

        await self.bot.change_presence(activity=discord.Game(name=f"Paused"), status=Status.do_not_disturb)

    
    @commands.command(name="unpause", help="Show the bot, whos da boss: shutdown", pass_context=True) # type: ignore
    @commands.is_owner()
    async def unpause(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Unpause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Unpaused..."
        )
        embed.set_author(name="Unpause", icon_url=self.bot.avatar_url)  # type: ignore
        await ctx.send(embed=embed)
        self.bot.paused = False
        logging.info("Unpaused...")

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))


def setup(bot):
    bot.add_cog(Settings(bot))
