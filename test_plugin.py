from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot import ModularBot

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Test(commands.Cog):
    def __init__(self, bot: "ModularBot") -> None:
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx: Context):
        embed = discord.Embed(description=self.bot.avatar_url)
        embed.set_author(name="Test", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)


async def setup(bot: "ModularBot"):
    await bot.add_cog(Test(bot))
