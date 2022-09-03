import asyncio
import logging
from typing import Optional

import discord
from db import generate_engine, get_session
from discord import utils
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
        return commands.when_mentioned_or("!")(bot, msg)  # type: ignore
    else:
        if msg.guild == None:
            return commands.when_mentioned_or("!")(bot, msg)  # type: ignore

        statement = select(Guild).where(Guild.id == msg.guild.id)
        server = bot.database.exec(statement).first()
        prefix = server.prefix if server else "!"

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

        # Database stuff
        self.engine = generate_engine()
        self.database: Session = get_session(self.engine)

        # Set up config for the bot
        self.setup_config()

        # Plugins
        self.disable_plugins: bool = disable_plugins
        self.plugins: dict[str, Plugin] = {}
        self.plugin_handler: PluginHandler = PluginHandler(self)
        if self.disable_plugins:
            logging.warning("Plugins are disabled")

        # RCE
        self.enable_rce: bool = enable_rce

    def run(
        self,
        token: str,
        *,
        reconnect: bool = True,
        log_handler: Optional[logging.Handler] = utils.MISSING,
        log_formatter: logging.Formatter = utils.MISSING,
        log_level: int = utils.MISSING,
        root_logger: bool = False,
    ) -> None:
        """A blocking call that abstracts away the event loop
        initialisation from you.

        If you want more control over the event loop then this
        function should not be used. Use :meth:`start` coroutine
        or :meth:`connect` + :meth:`login`.

        This function also sets up the logging library to make it easier
        for beginners to know what is going on with the library. For more
        advanced users, this can be disabled by passing ``None`` to
        the ``log_handler`` parameter.

        .. warning::

            This function must be the last function to call due to the fact that it
            is blocking. That means that registration of events or anything being
            called after this function call will not execute until it returns.

        Parameters
        -----------
        token: :class:`str`
            The authentication token. Do not prefix this token with
            anything as the library will do it for you.
        reconnect: :class:`bool`
            If we should attempt reconnecting, either due to internet
            failure or a specific failure on Discord's part. Certain
            disconnects that lead to bad state will not be handled (such as
            invalid sharding payloads or bad tokens).
        log_handler: Optional[:class:`logging.Handler`]
            The log handler to use for the library's logger. If this is ``None``
            then the library will not set up anything logging related. Logging
            will still work if ``None`` is passed, though it is your responsibility
            to set it up.

            The default log handler if not provided is :class:`logging.StreamHandler`.

            .. versionadded:: 2.0
        log_formatter: :class:`logging.Formatter`
            The formatter to use with the given log handler. If not provided then it
            defaults to a colour based logging formatter (if available).

            .. versionadded:: 2.0
        log_level: :class:`int`
            The default log level for the library's logger. This is only applied if the
            ``log_handler`` parameter is not ``None``. Defaults to ``logging.INFO``.

            .. versionadded:: 2.0
        root_logger: :class:`bool`
            Whether to set up the root logger rather than the library logger.
            By default, only the library logger (``'discord'``) is set up. If this
            is set to ``True`` then the root logger is set up as well.

            Defaults to ``False``.

            .. versionadded:: 2.0
        """

        async def runner():
            async with self:
                await self.async_init()
                await self.start(token, reconnect=reconnect)

        if log_handler is not None:
            utils.setup_logging(
                handler=log_handler,
                formatter=log_formatter,
                level=log_level,
                root=root_logger,
            )

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            # nothing to do here
            # `asyncio.run` handles the loop cleanup
            # and `self.start` closes all sockets and the HTTPClient instance.
            return

    def setup_config(self) -> None:
        config = self.database.exec(select(Config)).first()

        if not config:
            logging.warning("No config found, creating one")
            self.database.add(Config())
            self.database.commit()
            logging.info("Config created")

    async def async_init(self):
        # Load core extension
        await self.load_extension("extensions.core")

        # Load plugins if enabled
        if not self.disable_plugins:
            self.plugin_handler.populate_plugins()
            logging.info(f"Plugins: {self.plugins}")
            self.plugin_handler.install_requirements()
            await self.plugin_handler.load_all_plugins()
        else:
            logging.warning("Plugins are disabled")

    @property
    def avatar_url(self):
        if self.user and self.user.avatar:
            return self.user.avatar.url
        else:
            logging.debug("No avatar found")
            return ""
