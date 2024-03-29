from __future__ import annotations

import logging

import discord
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands import CommandError, Context
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

from core.bot.bot import ModularBot

logger = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot: "ModularBot"):
        @bot.event
        async def on_message(message):
            if not message.author == bot.user:
                if await bot.is_owner(message.author):
                    await bot.process_commands(message)

        @bot.event
        async def on_command_error(ctx: Context, error: CommandError):
            logger.debug(f"Error occured: {error}")

            if isinstance(error, CommandNotFound):
                embed = discord.Embed(
                    colour=0xFF0000, description="❌ Command not found"
                )
                embed.set_author(name="Status", icon_url=bot.avatar_url)
                await ctx.send(embed=embed)
            elif isinstance(error, NotFound):
                logger.warning("Error 404, passing")
                pass
            elif isinstance(error, MissingRequiredArgument):
                logger.debug(error)
                embed = discord.Embed(
                    colour=0xFF0000, description="❌ Missing required argument(s)"
                )
                embed.set_author(name="Status", icon_url=bot.avatar_url)
                await ctx.send(embed=embed)
                pass
            else:
                if ctx.command:
                    command_name = ctx.command.name
                    # If the error has already been encountered, increment the error count
                    bot.errors.add(name=command_name, ctx=ctx)

                logger.debug("Error not catched, raising")
                raise error


async def setup(bot: "ModularBot"):
    await bot.add_cog(Events(bot))
