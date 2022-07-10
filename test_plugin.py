from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import ModularBot

import discord
from discord.ext import commands
from discord.ext.commands import Context


class Test(commands.Cog):
    def __init__(self, bot: "ModularBot") -> None:
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx: Context):
        embed = discord.Embed(description=self.bot.user.avatar_url.__str__())
        embed.set_author(name="Test", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)


def setup(bot: "ModularBot"):
    bot.add_cog(Test(bot))
