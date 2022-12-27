"""
MODIFIED FILE - original author toxicrecker
MODIFIED BY - Stax124 (2022)

LICENSE:
	MIT License
 
	Copyright (c) 2018 toxicrecker
 
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.
 
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
"""

import asyncio
import logging

import discord
from discord.ext.commands import Context


class Paginator:
    """Utility for fast pagination of discord embeds

    Attributes:
        ctx (Context): The context of the command
        embeds (Embed | ModularEmbed): A list of `discord.Embed` objects
        auto_footer (bool): Whether to add a footer with page number to the embeds
        remove_reactions (bool): Whether to remove reaction when clicking on the control emojis
        timeout (int): The amount of time to wait for a reaction before closing the paginator
        control_emojis (tuple): The emojis to use for the control emojis

    Example:
        >>> embeds = [discord.Embed(title="Page 1"), discord.Embed(title="Page 2")]
        >>> paginator = Paginator(ctx, embeds, auto_footer=False)
        >>> await paginator.run()
    """

    def __init__(
        self,
        ctx: Context,
        embeds: list[discord.Embed],
        auto_footer: bool = True,
        remove_reactions: bool = True,
        timeout: int = 0,
        control_emojis: tuple = ("⏮️", "⏪", "🔐", "⏩", "⏭️"),
    ) -> None:
        self.ctx = ctx
        self.bot = ctx.bot
        self.current_page = 0
        self.auto_footer = auto_footer
        self.remove_reactions = remove_reactions
        self.control_emojis = control_emojis
        self.timeout = int(timeout)
        self.embeds = embeds

    async def run(self) -> None:
        """Run the paginator, exit after timeout

        Example:
            >>> embeds = [discord.Embed(title="Page 1"), discord.Embed(title="Page 2")]
            >>> paginator = Paginator(ctx, embeds, auto_footer=False)
            >>> await paginator.run()
        """

        if self.auto_footer:
            self.embeds[0].set_footer(
                text=f"({self.current_page+1}/{len(self.embeds)})"
            )

        msg = await self.ctx.send(embed=self.embeds[0])

        for emoji in self.control_emojis:
            try:
                await msg.add_reaction(emoji)
            except Exception:
                pass

        msg = await msg.channel.fetch_message(msg.id)

        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            return (
                user == self.ctx.author
                and reaction.message.id == msg.id
                and str(reaction.emoji) in self.control_emojis
            )

        while True:
            if self.timeout > 0:
                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", check=check, timeout=self.timeout
                    )
                except asyncio.TimeoutError:
                    self.current_page = 0
                    for reaction in msg.reactions:
                        if reaction.message.author.id == self.bot.user.id:
                            try:
                                await msg.remove_reaction(
                                    str(reaction.emoji), reaction.message.author
                                )
                            except Exception:
                                pass
                    break
            else:
                reaction: discord.Reaction
                user: discord.User
                reaction, user = await self.bot.wait_for("reaction_add", check=check)

            if str(reaction.emoji) == self.control_emojis[0]:
                self.current_page = 0

                await self._remove_reaction(msg, reaction, user)

                if self.auto_footer:
                    self.embeds[0].set_footer(
                        text=f"({self.current_page+1}/{len(self.embeds)})"
                    )
                await msg.edit(embed=self.embeds[0])

            elif str(reaction.emoji) == self.control_emojis[1]:
                self.current_page = self.current_page - 1
                self.current_page = 0 if self.current_page < 0 else self.current_page

                await self._remove_reaction(msg, reaction, user)

                if self.auto_footer:
                    self.embeds[self.current_page].set_footer(
                        text=f"({self.current_page+1}/{len(self.embeds)})"
                    )
                await msg.edit(embed=self.embeds[self.current_page])

            elif str(reaction.emoji) == self.control_emojis[2]:
                self.current_page = 0
                for reaction in msg.reactions:
                    try:
                        if reaction.message.author.id == self.bot.user.id:
                            await msg.remove_reaction(
                                str(reaction.emoji), reaction.message.author
                            )
                    except Exception:
                        pass
                break

            elif str(reaction.emoji) == self.control_emojis[3]:
                self.current_page = self.current_page + 1
                self.current_page = (
                    len(self.embeds) - 1
                    if self.current_page > len(self.embeds) - 1
                    else self.current_page
                )

                await self._remove_reaction(msg, reaction, user)

                if self.auto_footer:
                    self.embeds[self.current_page].set_footer(
                        text=f"({self.current_page+1}/{len(self.embeds)})"
                    )
                await msg.edit(embed=self.embeds[self.current_page])

            elif str(reaction.emoji) == self.control_emojis[4]:
                self.current_page = len(self.embeds) - 1

                await self._remove_reaction(msg, reaction, user)

                if self.auto_footer:
                    self.embeds[len(self.embeds) - 1].set_footer(
                        text=f"({self.current_page+1}/{len(self.embeds)})"
                    )
                await msg.edit(embed=self.embeds[len(self.embeds) - 1])

    async def _remove_reaction(
        self, msg: discord.Message, reaction: discord.Reaction, user: discord.User
    ):
        if self.remove_reactions:
            try:
                await msg.remove_reaction(str(reaction.emoji), user)
            except discord.errors.Forbidden:
                pass
            except Exception as e:
                logging.warning(f"{type(e).__name__: {e}}")
