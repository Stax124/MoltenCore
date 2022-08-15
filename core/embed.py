import datetime
from typing import TYPE_CHECKING, Literal, Union

import discord
from discord.colour import Colour
from discord.embeds import _EmptyEmbed
from discord.ext.commands import Context
from models.config import Config
from sqlmodel import select

from core.paginator import Paginator

if TYPE_CHECKING:
    from core.bot import ModularBot


class NoDataProvided(Exception):
    pass


class ModularEmbed(discord.Embed):
    """Extended discord.Embed class that automatically respects the main color of the bot

    Args:
        bot (ModularBot): The bot instance
        color (Union[int, Colour, _EmptyEmbed]): The color of the embed
        colour (Union[int, Colour, _EmptyEmbed]): The color of the embed (alternative name)
        title (Union[object, _EmptyEmbed]): The title of the embed
        type (str): The type of the embed
    """

    def __init__(
        self,
        bot: "ModularBot",
        *,
        color: Union[int, Colour, _EmptyEmbed] = _EmptyEmbed(),
        colour: Union[int, Colour, _EmptyEmbed] = _EmptyEmbed(),
        title: Union[object, _EmptyEmbed] = _EmptyEmbed(),
        type: str = "",
        url: Union[object, _EmptyEmbed] = "",
        description: Union[object, _EmptyEmbed] = _EmptyEmbed(),
        timestamp: Union[Literal[True], datetime.datetime, _EmptyEmbed] = _EmptyEmbed()
    ) -> None:
        config = bot.database.exec(select(Config)).first()
        if config:
            color = config.main_color

        if timestamp == True:
            timestamp = datetime.datetime.now()

        super().__init__(
            color=color,
            colour=colour,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp,
        )


class ModularEmbedList:
    """Utility class that handles pagination of large amounts of data automatically

    Attributes:
        bot (ModularBot): The bot instance
        ctx (Context): The context of the command
        title (str): The title of the embed

    Example:
        >>> embed = ModularEmbedList(bot, ctx, title="Title")
        >>> embed.add_data("Hello World")
        >>> embed.add_data("Hello World 2")
        >>> paginator = embed.build()
        >>> paginator.run()

    """

    def __init__(
        self,
        bot: "ModularBot",
        ctx: Context,
        title: Union[str, _EmptyEmbed],
        raw: bool = False,
    ) -> None:
        self.ctx = ctx
        self.bot = bot
        self.title = title

        self.data: list[str] = []
        self.limit = 1990 if raw else 2000
        self.raw = raw

    def add_data(self, data: str) -> None:
        """Append data to the embed

        Example:
            >>> embed = ModularEmbedList(bot, ctx, title="Title")
            >>> embed.add_data("Hello World")
        """

        self.data.append(data)

    def build(self) -> Paginator:
        """Build the paginator from the data that was provided

        Example:
            >>> embed = ModularEmbedList(bot, ctx, title="Title")
            >>> embed.add_data("Hello World")
            >>> paginator = embed.build()
        """

        if not self.data:
            raise NoDataProvided("No data to build")

        embeds: list[discord.Embed] = []
        page: str = ""

        if self.raw:
            page += "```"

        for data in self.data:
            if len(data) > self.limit:
                i: list[str] = []
                current = ""

                for char in data:
                    if len(current) < self.limit - 1:
                        current += char
                    else:
                        i.append(current)
                        current = ""

            else:
                i = [data]

            for item in data:
                if len(page) + len(item) > self.limit:
                    if self.raw:
                        page += "```"

                    embeds.append(
                        ModularEmbed(self.bot, title=self.title, description=page)
                    )
                    page = "```" if self.raw else ""
                else:
                    page += item

            # Add the last page
            if self.raw:
                page += "```"
            embeds.append(ModularEmbed(self.bot, title=self.title, description=page))

        return Paginator(ctx=self.ctx, embeds=embeds)
