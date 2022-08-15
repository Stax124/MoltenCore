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
            embed.set_author(
                name="Plugins", icon_url=self.bot.user.avatar_url.__str__()
            )
            await ctx.send(embed=embed)
        else:
            modular_embed = ModularEmbedList(self.bot, ctx, title="Plugins")
            for plugin_name in self.bot.plugins:
                plugin = self.bot.plugins[plugin_name]
                modular_embed.add_data(
                    f"{'🟩' if plugin.enabled else '🟥'} {plugin.name}"
                )
            await modular_embed.build().run()


def setup(bot):
    bot.add_cog(Plugins(bot))
