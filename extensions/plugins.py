import re

import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from core.bot import ModularBot
from core.embed import ModularEmbed, ModularEmbedList


class Plugins(commands.Cog):
    "Handle bot plugins"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    @commands.command(name="plugins")
    @commands.is_owner()
    async def plugins(self, ctx: Context):

        if not self.bot.plugins:
            embed = ModularEmbed(self.bot, title="No plugins found")
            embed.set_author(name="Plugins", icon_url=self.bot.avatar_url)
            await ctx.send(embed=embed)
        else:
            modular_embed = ModularEmbedList(self.bot, ctx, title="Plugins")
            for plugin_name in self.bot.plugins:
                plugin = self.bot.plugins[plugin_name]
                modular_embed.add_data(
                    f"{'🟩' if plugin.enabled else '🟥'} {plugin.name}"
                )
            await modular_embed.build().run()

    @commands.command(name="plugin")
    @commands.is_owner()
    async def plugin(self, ctx: Context, *, plugin_name: str):
        plugin = self.bot.plugins[plugin_name]
        if not plugin:
            await ctx.send(
                embed=discord.Embed(title="Plugin not found", color=0xFF0000)
            )
        else:

            embed = discord.Embed(title=plugin.name, color=0x0000FF)
            embed.add_field(name="Id", value=plugin.id)
            embed.add_field(name="Author", value=plugin.author)
            embed.add_field(name="Enabled", value=plugin.enabled)
            embed.add_field(
                name="Hash",
                value=plugin.repo.head.object.hexsha if plugin.repo else "Unknown",
            )
            embed.add_field(
                name="Traceback",
                value=plugin.short_traceback if plugin.short_traceback else "None",
            )
            embed.add_field(name="Stars", value=plugin.stars)
            embed.add_field(name="Forks", value=plugin.forks)
            embed.add_field(name="Issues", value=plugin.issues)
            embed.add_field(name="License", value=plugin.license)

            await ctx.send(embed=embed)

    @commands.command(name="enable-plugin")
    @commands.is_owner()
    async def enable_plugin(self, ctx: Context, *, plugin_name: str):
        plugin = self.bot.plugins[plugin_name]
        if not plugin:
            await ctx.send(
                embed=discord.Embed(title="Plugin not found", color=0xFF0000)
            )
        elif plugin.enabled:
            await ctx.send(
                embed=discord.Embed(title="Plugin already enabled", color=0xFF0000)
            )
        else:
            await plugin.enable(load=True)
            await ctx.send(
                embed=discord.Embed(
                    title=f"Plugin {plugin.name} enabled",
                    color=0x00FF00,
                    description="Plugin has been enabled and loaded",
                )
            )

    @commands.command(name="disable-plugin")
    @commands.is_owner()
    async def disable_plugin(self, ctx: Context, *, plugin_name: str):
        plugin = self.bot.plugins[plugin_name]
        if not plugin:
            await ctx.send(
                embed=discord.Embed(title="Plugin not found", color=0xFF0000)
            )
        elif not plugin.enabled:
            await ctx.send(
                embed=discord.Embed(title="Plugin already disabled", color=0xFF0000)
            )
        else:
            await plugin.disable(unload=True)
            await ctx.send(
                embed=discord.Embed(
                    title=f"Plugin {plugin.name} disabled",
                    color=0x00FF00,
                    description="Plugin has been disabled and unloaded",
                )
            )


async def setup(bot: ModularBot):
    await bot.add_cog(Plugins(bot))
