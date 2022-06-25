import argparse
import logging
import os

import discord
from coloredlogs import install as install_coloredlogs
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (ExtensionAlreadyLoaded,
                                         ExtensionNotFound, ExtensionNotLoaded)
from pretty_help import PrettyHelp
from rich.traceback import install as install_traceback
from sqlmodel import Session, select

from db import generate_engine, get_session
from models.guild import Guild

install_traceback() # Installs better error logging

# Command line interface handling
parser = argparse.ArgumentParser(
    prog="Trinity", description="Economy discord bot made in python")
parser.add_argument("-l", "--logging",  default="INFO",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Choose level of logging")
parser.add_argument("-f", "--file", type=str, help="Filename for logging")
parser.add_argument("--token", default=os.environ.get("TRINITY"), type=str,
                    help="Discord API token: Get yours at https://discord.com/developers/applications")
args = parser.parse_args()


loglevels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL:": logging.CRITICAL
}

if args.file:
    logging.basicConfig(
        level=loglevels[args.logging], handlers=[logging.FileHandler(args.file, "w", 'utf-8')], format='%(levelname)s | %(asctime)s | %(name)s |->| %(message)s', datefmt=r"%H:%M:%S"
    )

# Coloring the logs
install_coloredlogs(level=loglevels[args.logging],
                    fmt='%(levelname)s | %(asctime)s | %(name)s |->| %(message)s', datefmt=r"%H:%M:%S")

# Searching for all primary modules
default_extensions = ["extensions."+i.replace(".py", "")
                      for i in os.listdir("extensions") if i.endswith(".py")]

if not os.path.exists("plugins"):
    os.makedirs("plugins")
        
if not os.path.exists("plugins/plugins.json"):
    with open("plugins/plugins.json", "w") as f:
        f.write("{}")
            
    


def get_prefix(bot: "ModularBot", msg: discord.Message):
    if msg.channel.type == discord.ChannelType.private:
        logging.debug("Private message, using default prefix")
        return commands.when_mentioned_or("!")(bot, msg)  # type: ignore
    else:
        if msg.guild == None:
            return commands.when_mentioned_or("!")(bot, msg)  # type: ignore

        statement = select(Guild).where(
            Guild.id == msg.guild.id)
        server = bot.database.exec(statement).first()
        prefix = server.prefix if server else "!"

        logging.debug(f"Using prefix {prefix} for this server")
        return commands.when_mentioned_or(prefix)(bot, msg)  # type: ignore


class ModularBot(AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,  # type: ignore
            help_command=PrettyHelp(
                color=0xffff00, show_index=True, sort_commands=True),
            intents=discord.Intents.all()
        )

        # Variables
        self.paused: bool = False
        self.__version__: str = "0.0.1alpha"
        self.avatar_url: str = ""  # Will get set when the bot is ready

        # Database stuff
        self.engine = generate_engine()
        self.database: Session = get_session(self.engine)

    def run(self, token: str, *, bot: bool = True, reconnect: bool = True):
        super().run(token, bot=bot, reconnect=reconnect)
        self.avatar_url = str(self.user.avatar_url)


bot = ModularBot()


@bot.command(name="reload")
@commands.is_owner()
async def command_reload_extension(ctx: Context, extension: str):
    try:
        bot.reload_extension("extensions."+extension)
        logging.info(f"{extension} reloaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} reloaded")
        embed.set_author(name="Reload", icon_url=bot.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Reload", icon_url=bot.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="load")
@commands.is_owner()
async def command_load_extension(ctx: Context, extension: str):
    try:
        bot.load_extension("extensions."+extension)
        logging.info(f"{extension} loaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} loaded")
        embed.set_author(name="Load", icon_url=bot.avatar_url)
    except ExtensionAlreadyLoaded:
        logging.warn(f"{extension} already loaded")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} already loaded")
        embed.set_author(name="Load", icon_url=bot.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Load", icon_url=bot.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="unload")
@commands.is_owner()
async def command_unload_extension(ctx: Context, extension: str):
    try:
        bot.unload_extension("extensions."+extension)
        logging.info(f"{extension} unloaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} unloaded")
        embed.set_author(name="Unload", icon_url=bot.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Unload", icon_url=bot.avatar_url)
    except ExtensionNotLoaded:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} exists, but is not loaded")
        embed.set_author(name="Unload", icon_url=bot.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="reload-all")
@commands.is_owner()
async def command_reload_all_extensions(ctx: Context):
    all_extensions = ["extensions."+i.replace(".py", "")
                      for i in os.listdir("extensions") if i.endswith(".py")]

    ok = True

    for extension in all_extensions:
        try:
            bot.reload_extension(extension)
            logging.info(f"{extension} reloaded")
        except ExtensionNotFound:
            ok = False
            logging.error(f"{extension} not found")
            embed = discord.Embed(
                color=0xff0000, description=f"{extension} not found")
            embed.set_author(name="Reload All", icon_url=bot.avatar_url)

    if ok:
        embed = discord.Embed(
            color=0x00ff00, description=f"All extensions reloaded")
        embed.set_author(name="Reload All", icon_url=bot.avatar_url)

    await ctx.send(embed=embed)

if __name__ == "__main__":
    for extension in default_extensions:
        bot.load_extension(extension)
        logging.info(f"{extension} loaded")

    bot.run(args.token, reconnect=True)
