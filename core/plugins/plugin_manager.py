import importlib
import logging
import re
import subprocess
import sys
from typing import TYPE_CHECKING

from sqlmodel import select

from core.exceptions import URLException
from core.plugins.plugin import Plugin
from models.plugins import PluginData

if TYPE_CHECKING:
    from core.bot.bot import ModularBot

logger = logging.getLogger("plugin-handler")


class PluginManager:
    "Takes care of managing all the installed plugins"

    def __init__(self, bot: "ModularBot") -> None:
        self.bot = bot

    def _find_plugin_data(self) -> list[PluginData]:
        return self.bot.database.exec(select(PluginData)).all()

    def populate_plugins(self) -> None:
        logger.debug("Populating plugin list")

        for data in self._find_plugin_data():
            plugin = Plugin(data, self.bot)
            self.bot.plugins[plugin.name] = plugin

    async def remove_plugin(self, name: str) -> None:
        logger.debug(f"Removing plugin {name}")
        plugin = self.bot.plugins[name]
        await plugin.remove()
        del self.bot.plugins[name]

    async def install_plugin(self, url: str) -> None:
        "Installs a plugin from a remote git repository"

        # mitigation of CVE-2022-24439 - https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858
        pattern = re.compile(
            r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        )
        if not pattern.match(url):
            raise URLException("Invalid URL")

        logger.debug(f"Installing plugin from {url}")

        try:
            new_id = (
                max(i.id for i in self.bot.database.exec(select(PluginData)).all()) + 1
            )
        except ValueError:
            new_id = 1
        logger.debug(f"Created plugin id: {new_id}")
        new_data = PluginData(id=new_id, url=url)
        self.bot.database.add(new_data)

        plugin = Plugin(new_data, self.bot)

        logger.info("Installing requirements")
        self.install_requirements()

        await plugin.load()
        self.bot.plugins[plugin.name] = plugin

        self.bot.database.commit()

    async def reload_all_plugins(self) -> None:
        logger.debug("Reloading plugin data of all plugins")

        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            if plugin.enabled:
                await plugin.reload()
                logger.debug(f"{plugin_name} successfully reloaded")

    async def load_all_plugins(self) -> None:
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            await plugin.load()
            logger.debug(f"{plugin_name} successfully loaded")

    async def unload_all_plugins(self) -> None:
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            await plugin.unload()
            logger.debug(f"{plugin_name} successfully unloaded")

    @property
    def requirements(self) -> list[str]:
        # Get all requirements for pip packages from all plugins

        req: list[str] = []
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            recieved = plugin.get_requirements()
            for requirement in recieved:
                if requirement not in req:
                    req.append(requirement)

        return req

    def install_requirements(self) -> None:
        "Installs all requirements that plugins require"

        try:
            for i in self.requirements:
                importlib.import_module(i)
        except ImportError:
            logger.warning("Some requirements not found, installing them")
            extended = (
                "\\Scripts\\python.exe" if sys.platform == "win32" else "\\bin\\python"
            )
            command = subprocess.Popen(
                f"{sys.prefix+extended} -m pip install {' '.join(self.requirements)}",
                shell=True,
            )
            command.wait()
