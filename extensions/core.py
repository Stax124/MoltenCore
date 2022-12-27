import logging
import os

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionNotFound,
    ExtensionNotLoaded,
)

from core.bot.bot import ModularBot
from core.functions.functions import get_extensions

default_extensions = get_extensions()

logger = logging.getLogger(__name__)


class Core(commands.Cog):
    def __init__(self, bot: ModularBot) -> None:
        self.bot = bot

    async def load_default_extensions(self):
        if self.bot.cogs.__len__() == 0:
            for extension in default_extensions:
                await self.bot.load_extension(extension)
                logger.info(f"{extension} loaded")
        else:
            logger.info("Default extensions already loaded, skipping initial load")

    @commands.hybrid_command(name="reload", help="Reloads an extension")
    @commands.is_owner()
    async def command_reload_extension(self, ctx: Context, extension: str) -> None:
        try:
            await self.bot.reload_extension(extension)
            logger.info(f"{extension} reloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} reloaded")
            embed.set_author(name="Reload", icon_url=self.bot.avatar_url)
        except ExtensionNotFound:
            logger.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Reload", icon_url=self.bot.avatar_url)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="load", help="Loads an extension")
    @commands.is_owner()
    async def command_load_extension(self, ctx: Context, extension: str) -> None:
        try:
            await self.bot.load_extension(extension)
            logger.info(f"{extension} loaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} loaded")
            embed.set_author(name="Load", icon_url=self.bot.avatar_url)
        except ExtensionAlreadyLoaded:
            logger.warn(f"{extension} already loaded")
            embed = discord.Embed(
                color=0xFF0000, description=f"{extension} already loaded"
            )
            embed.set_author(name="Load", icon_url=self.bot.avatar_url)
        except ExtensionNotFound:
            logger.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Load", icon_url=self.bot.avatar_url)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unload", help="Unloads an extension")
    @commands.is_owner()
    async def command_unload_extension(self, ctx: Context, extension: str) -> None:
        try:
            await self.bot.unload_extension(extension)
            logger.info(f"{extension} unloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{extension} unloaded")
            embed.set_author(name="Unload", icon_url=self.bot.avatar_url)
        except ExtensionNotFound:
            logger.error(f"{extension} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{extension} not found")
            embed.set_author(name="Unload", icon_url=self.bot.avatar_url)
        except ExtensionNotLoaded:
            logger.error(f"{extension} exists, but is not loaded")
            embed = discord.Embed(
                color=0xFF0000, description=f"{extension} exists, but is not loaded"
            )
            embed.set_author(name="Unload", icon_url=self.bot.avatar_url)

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="reload-all", help="Reloads all extensions and plugins"
    )
    @commands.is_owner()
    async def command_reload_all_extensions(self, ctx: Context) -> None:
        all_extensions = [
            i.replace(".py", "") for i in os.listdir("extensions") if i.endswith(".py")
        ]

        ok = True

        logger.info("----------Beggining of reload----------")

        for extension in all_extensions:
            try:
                await self.bot.reload_extension("extensions." + extension)
                logger.info(f"{extension} reloaded")
            except ExtensionNotFound:
                ok = False
                logger.error(f"{extension} not found")
                embed = discord.Embed(
                    color=0xFF0000, description=f"{extension} not found"
                )
                break

        if ok:
            embed = discord.Embed(color=0x00FF00, description="All extensions reloaded")
        else:
            embed = discord.Embed(color=0xFF0000, description="Some failiures occured")

        embed.set_author(name="Reload All", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

        ok = True

        self.bot.plugin_manager.populate_plugins()

        for plugin_name in self.bot.plugins:
            try:
                plugin = self.bot.plugins[plugin_name]
                await plugin.reload()
                logger.info(f"Plugin {plugin_name} reloaded")
            except Exception as e:
                ok = False
                logger.error(f"Plugin {plugin_name} failed to reload: {e}")
                embed = discord.Embed(
                    color=0xFF0000,
                    description=f"Plugin {plugin_name} failed to reload: [{type(e).__name__}]{e}",
                )
                break

        if ok:
            embed = discord.Embed(color=0x00FF00, description="All plugins reloaded")
        else:
            embed = discord.Embed(color=0xFF0000, description="Some failiures occured")

        logger.info("----------End of reload----------")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="plugin-reload", help="Reloads a plugin")
    @commands.is_owner()
    async def command_reload_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            self.bot.plugin_manager.populate_plugins()
            await self.bot.plugins[plugin].reload()
            logger.info(f"{plugin} reloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} reloaded")
        except KeyError:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Reload", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="plugin-load", help="Loads a plugin")
    @commands.is_owner()
    async def command_load_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            self.bot.plugin_manager.populate_plugins()
            await self.bot.plugins[plugin].load()
            logger.info(f"{plugin} loaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} loaded")
        except KeyError:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Load", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="plugin-unload", help="Unloads a plugin")
    @commands.is_owner()
    async def command_unload_plugin(self, ctx: Context, plugin: str) -> None:
        try:
            await self.bot.plugins[plugin].unload()
            logger.info(f"{plugin} unloaded")
            embed = discord.Embed(color=0x00FF00, description=f"{plugin} unloaded")
        except KeyError:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")
        except ExtensionNotFound:
            logger.error(f"{plugin} not found")
            embed = discord.Embed(color=0xFF0000, description=f"{plugin} not found")

        embed.set_author(name="Unload", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="sync", help="Sync all registered slash commands to discord"
    )
    @commands.is_owner()
    async def sync(self, ctx: Context) -> None:
        await self.bot.sync()
        await ctx.send(
            embed=discord.Embed(color=0x00FF00, description="Commands synced")
        )


async def setup(bot: ModularBot):
    cog = Core(bot)
    await cog.load_default_extensions()
    await bot.add_cog(cog)
