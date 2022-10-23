import asyncio
from typing import TYPE_CHECKING

import discord
from discord.ext.commands.context import Context

if TYPE_CHECKING:
    from core.bot.bot import ModularBot


async def confirm(
    bot: "ModularBot",
    ctx: Context,
    message: str,
    timeout: int = 20,
    author: str = "Confirm",
) -> bool:
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(255, 255, 0), description=message
    )
    embed.set_author(name=author, icon_url=bot.avatar_url)

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction: discord.Reaction, user: discord.User) -> bool:
        return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=timeout, check=check)
        if reaction.emoji == "❌":
            await msg.delete()
            return False
        elif reaction.emoji == "✅":
            await msg.delete()
            return True
        else:
            return False
    except asyncio.TimeoutError:
        await msg.delete()
        return False
