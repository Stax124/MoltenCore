from __future__ import annotations

import logging
import sys

import discord
import models  # For eval
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands.context import Context
from sqlmodel import select  # For eval

from core.bot.bot import ModularBot
from core.functions.confirm import confirm
from core.structures.embed import ModularEmbedList

logger = logging.getLogger(__name__)


class Owner(commands.Cog):
    "Owner commands"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    @commands.hybrid_command(name="shutdown", help="Terminate the process")  # type: ignore
    @commands.is_owner()
    async def shutdown(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Terminate process ?")
        if not confirmed:
            return

        logger.warning("Shutting down bot")
        embed = discord.Embed(colour=0x00FF00, description="✅ Shutting down...")
        embed.set_author(name="Shutdown", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)
        logger.info("Shutting down...")

        await self.bot.change_presence(
            activity=discord.Game(name=f"Shutting down..."), status=Status.offline
        )
        sys.exit()

    @commands.is_owner()
    @commands.hybrid_command(name="eval", help="Evaluate string")  # type: ignore
    async def eval(self, ctx: Context, *, message: str):
        if self.bot.enable_rce:
            try:
                embed = ModularEmbedList(self.bot, ctx, title="Eval", raw=True)
                embed.add_data(str(eval(message)))
                await embed.build().run()
                # await ctx.send(str(eval(message))[:2000])
            except Exception as e:
                await ctx.send(e.__str__())
        else:
            await ctx.send("RCE disabled by default")

    @commands.is_owner()
    @commands.hybrid_command(name="exec", help="Execute string")  # type: ignore
    async def exec(self, ctx: Context, *, message: str):
        if self.bot.enable_rce:
            try:
                exec(message)
                await ctx.send("Success")
            except Exception as e:
                await ctx.send(e.__str__())
        else:
            await ctx.send("RCE disabled by default")


async def setup(bot: "ModularBot"):
    await bot.add_cog(Owner(bot))
