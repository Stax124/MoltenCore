# Example Plugin

This is the core structure of a plugin. It is a simple plugin that sends an embed with the text "Hello world from test plugin" when the command `test` is used.

Each plugin is required to be hosted in a **GitHub** repository. Please add the `moltencore` topic to your repository so that it is easier to find.

::: info
GitHub is the only supported source control provider at the moment because it provides a simple API with a lot of features.
:::

## Exaple plugin file

Your plugin needs to be saved in this directory pattern: `plugins/[plugin_name]/[any_name]_plugin.py`

For example: `plugins/test/test_plugin.py`

Bot will only attempt to load plugins that are in the `plugins` folder and contain `_plugin.py` in their name.

::: details Code

```py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import ModularBot

import discord
from discord.ext import commands
from discord.ext.commands import Context

class Test(commands.Cog):
    def __init__(self, bot: "ModularBot") -> None:
        self.bot = bot

    @commands.hybrid_command(name="test")
    async def test(self, ctx: Context):
        embed = discord.Embed(description="Hello world from test plugin")
        embed.set_author(name="Test", icon_url=self.bot.avatar_url)
        await ctx.send(embed=embed)


async def setup(bot: "ModularBot"):
    await bot.add_cog(Test(bot))
```

:::

## Dependencies

If plugin requires any dependencies, they should be listed in a file called `requirements.txt` in the plugin's folder. This file should contain the name of the dependency and the version of the dependency. For example:

```py
supabase>=0.7
```

## Developers

Every developer counts! Feel free to create new interesting plugins and share them with the community.

::: tip
There are lots of useful components aleardy premade for you, please check out the Plugin Developer section for more information.
:::
