from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands.errors import (CommandNotFound,
                                         MissingRequiredArgument)

if TYPE_CHECKING:
    from main import ModularBot


class Events(commands.Cog):

    def __init__(self, bot: "ModularBot"):
        @bot.event
        async def on_message(message):
            if not message.author == bot.user:
                if await bot.is_owner(message.author):
                    await bot.process_commands(message)

        @bot.event
        async def on_command_error(ctx, error):
            logging.debug(f"Error occured: {error}")
            if isinstance(error, CommandNotFound):
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f'❌ Command not found'
                )
                embed.set_author(name="Status", icon_url=bot.user.avatar_url.__str__())
                await ctx.send(embed=embed)
            elif isinstance(error, NotFound):
                logging.warning("Error 404, passing")
                pass
            elif isinstance(error, MissingRequiredArgument):
                logging.debug(error)
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f'❌ Missing required argument(s)'
                )
                embed.set_author(name="Status", icon_url=bot.user.avatar_url.__str__())
                await ctx.send(embed=embed)
                pass
            else:
                logging.debug("Error not catched, raising")
                raise error


def setup(bot: "ModularBot"):
    bot.add_cog(Events(bot))
