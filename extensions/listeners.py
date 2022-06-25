from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord.activity import Activity
from discord.enums import ActivityType
from discord.ext import commands
from models.guild import Guild

if TYPE_CHECKING:
    from main import ModularBot


class Listeners(commands.Cog):
    "Listeners for bot, feel free to add your own"

    def __init__(self, bot: "ModularBot"):
        self.bot = bot

    # region Default

    @commands.Cog.listener()
    async def on_connect(self):
        logging.info("Bot sucessfully connected to Discord servers")

    @commands.Cog.listener()
    async def on_connected(self):
        logging.info("Connected to Discord servers")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Guilds joined: {len(self.bot.guilds)}")

        for guild in self.bot.guilds:
            if self.bot.database.query(Guild).filter_by(id=guild.id).first() is None:
                logging.info(f"Adding guild {guild.name} to database")
                self.bot.database.add(Guild(id=guild.id))
                self.bot.database.commit()

        await self.bot.change_presence(
            activity=Activity(type=ActivityType.listening, name="for commands"))

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.info("Bot lost connection to Discord servers")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if self.bot.database.query(Guild).filter_by(id=guild.id).first() is None:
            logging.info(f"Adding guild {guild.name} to database")
            self.bot.database.add(Guild(id=guild.id))
            self.bot.database.commit()

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        if self.bot.database.query(Guild).filter_by(id=guild.id).first() is not None:
            logging.info(f"Removing guild {guild.name} from database")
            self.bot.database.query(Guild).filter_by(id=guild.id).delete()
            self.bot.database.commit()

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))


def setup(bot):
    bot.add_cog(Listeners(bot))
