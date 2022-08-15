import logging

import discord
from db import generate_engine, get_session
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from models.config import Config
from models.guild import Guild
from pretty_help import PrettyHelp
from sqlmodel import Session, select

from core.plugin import Plugin
from core.plugin_handler import PluginHandler


def get_prefix(bot: "ModularBot", msg: discord.Message) -> list[str]:
    if msg.channel.type == discord.ChannelType.private:
        logging.debug("Private message, using default prefix")
        return commands.when_mentioned_or("!")(bot, msg)  # type: ignore
    else:
        if msg.guild == None:
            return commands.when_mentioned_or("!")(bot, msg)  # type: ignore

        statement = select(Guild).where(Guild.id == msg.guild.id)
        server = bot.database.exec(statement).first()
        prefix = server.prefix if server else "!"

        logging.debug(f"Using prefix {prefix} for this server")
        return commands.when_mentioned_or(prefix)(bot, msg)  # type: ignore


class ModularBot(AutoShardedBot):
    def __init__(self, enable_rce: bool = False, disable_plugins: bool = False) -> None:
        super().__init__(
            command_prefix=get_prefix,  # type: ignore
            help_command=PrettyHelp(
                color=0xFFFF00, show_index=True, sort_commands=True
            ),
            intents=discord.Intents.all(),
        )

        # State of the bot
        self.__version__: str = "0.0.1alpha"

        # Database stuff
        self.engine = generate_engine()
        self.database: Session = get_session(self.engine)

        # Set up config for the bot
        self.setup_config()

        # Load core extension
        self.load_extension("extensions.core")

        # Plugins
        self.disable_plugins: bool = disable_plugins
        self.plugins: dict[str, Plugin] = {}
        self.plugin_handler: PluginHandler = PluginHandler(self)
        if self.disable_plugins:
            logging.warning("Plugins are disabled")

        if not disable_plugins:
            self.plugin_handler.populate_plugins()
            logging.info(f"Plugins: {self.plugins}")
            self.plugin_handler.install_requirements()
            self.plugin_handler.load_all_plugins()

        # RCE
        self.enable_rce: bool = enable_rce

    def run(self, token: str, *, bot: bool = True, reconnect: bool = True) -> None:
        super().run(token, bot=bot, reconnect=reconnect)

    def setup_config(self) -> None:
        config = self.database.exec(select(Config)).first()

        if not config:
            logging.warning("No config found, creating one")
            self.database.add(Config())
            self.database.commit()
            logging.info("Config created")
