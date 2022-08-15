import logging
import os

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionNotFound,
    ExtensionNotLoaded,
)

from core.bot import ModularBot
from core.functions import get_extensions

default_extensions = get_extensions()

logger = logging.getLogger(__name__)


class Core(commands.Cog):
    def __init__(self, bot: ModularBot) -> None:
        self.bot = bot

        if self.bot.cogs.__len__() == 0:
            self.load_default_extensions()

    def load_default_extensions(self):
        for extension in default_extensions:
            self.bot.load_extension(extension)
            logger.info(f"{extension} loaded")

    @commands.command(name="reload")
    @commands.is_owner()
    async def command_reload_extension(self, ctx: Context, extension: str) -> None:
        try:
            self.bot.reload_extension(extension)
            logger.info(f"{extension} reloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} reloaded")
            embed.set_author(name="Reload", icon_url=self.bot.user.avatar_url.__str__())
        except ExtensionNotFound:
            logging.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Reload", icon_url=self.bot.user.avatar_url.__str__())

        await ctx.send(embed=embed)

    @commands.command(name="load")
    @commands.is_owner()
    async def command_load_extension(self, ctx: Context, extension: str) -> None:
        try:
            self.bot.load_extension(extension)
            logger.info(f"{extension} loaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} loaded")
            embed.set_author(name="Load", icon_url=self.bot.user.avatar_url.__str__())
        except ExtensionAlreadyLoaded:
            logging.warn(f"{extension} already loaded")
            embed = discord.Embed(
                color=0xFF0000, description=f"{extension} already loaded"
            )
            embed.set_author(name="Load", icon_url=self.bot.user.avatar_url.__str__())
        except ExtensionNotFound:
            logging.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Load", icon_url=self.bot.user.avatar_url.__str__())

        await ctx.send(embed=embed)

    @commands.command(name="unload")
    @commands.is_owner()
    async def command_unload_extension(self, ctx: Context, extension: str) -> None:
        try:
            self.bot.unload_extension(extension)
            logger.info(f"{extension} unloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} unloaded")
            embed.set_author(name="Unload", icon_url=self.bot.user.avatar_url.__str__())
        except ExtensionNotFound:
            logging.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Unload", icon_url=self.bot.user.avatar_url.__str__())
        except ExtensionNotLoaded:
            logging.error(f"{extension} exists, but is not loaded")
            embed = discord.Embed(
                color=0xFF0000, description=f"{extension} exists, but is not loaded"
            )
            embed.set_author(name="Unload", icon_url=self.bot.user.avatar_url.__str__())

        await ctx.send(embed=embed)

    @commands.command(name="reload-all")
    @commands.is_owner()
    async def command_reload_all_extensions(self, ctx: Context) -> None:
        all_extensions = [
            i.replace(".py", "") for i in os.listdir("extensions") if i.endswith(".py")
        ]

        ok = True

        for extension in all_extensions:
            try:
                self.bot.reload_extension("extensions." + extension)
                logger.info(f"{extension} reloaded")
            except ExtensionNotFound:
                ok = False
                logging.error(f"{extension} not found")
                embed = discord.Embed(
                    color=0xFF0000, description=f"{extension} not found"
                )
                break

        if ok:
            embed = discord.Embed(
                color=0x00FF00, description=f"All extensions reloaded"
            )

        embed.set_author(name="Reload All", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)

        ok = True

        self.bot.plugin_handler.populate_plugins()

        for plugin_name in self.bot.plugins:
            try:
                plugin = self.bot.plugins[plugin_name]
                plugin.reload()
                logger.info(f"Plugin {plugin_name} reloaded")
            except Exception as e:
                ok = False
                logging.error(f"Plugin {plugin_name} failed to reload: {e}")
                embed = discord.Embed(
                    color=0xFF0000,
                    description=f"Plugin {plugin_name} failed to reload: [{type(e).__name__}]{e}",
                )
                break

        if ok:
            embed = discord.Embed(color=0x00FF00, description=f"All plugins reloaded")

        await ctx.send(embed=embed)

    @commands.command(name="plugin-reload")
    @commands.is_owner()
    async def command_reload_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            self.bot.plugin_handler.populate_plugins()
            self.bot.plugins[plugin].reload()
            logger.info(f"{plugin} reloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} reloaded")
        except KeyError:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Reload", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)

    @commands.command(name="plugin-load")
    @commands.is_owner()
    async def command_load_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            self.bot.plugin_handler.populate_plugins()
            self.bot.plugins[plugin].load()
            logger.info(f"{plugin} loaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} loaded")
        except KeyError:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Load", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)

    @commands.command(name="plugin-unload")
    @commands.is_owner()
    async def command_unload_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            self.bot.plugins[plugin].unload()
            logger.info(f"{plugin} unloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} unloaded")
        except KeyError:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logging.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Unload", icon_url=self.bot.user.avatar_url.__str__())
        await ctx.send(embed=embed)


def setup(bot: ModularBot):
    bot.add_cog(Core(bot))
