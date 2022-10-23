import importlib
import logging
import subprocess
import sys
from typing import TYPE_CHECKING

from sqlmodel import select

from core.plugins.plugin import Plugin
from models.plugins import PluginData

if TYPE_CHECKING:
    from core.bot.bot import ModularBot


class PluginHandler:
    "Takes care of managing all the installed plugins"

    def __init__(self, bot: "ModularBot") -> None:
        self.logger = logging.getLogger("plugin-handler")
        self.bot = bot

    def _find_plugin_data(self) -> list[PluginData]:
        return self.bot.database.exec(select(PluginData)).all()

    def populate_plugins(self) -> None:
        self.logger.debug("Populating plugin list")

        for data in self._find_plugin_data():
            plugin = Plugin(data, self.bot)
            self.bot.plugins[plugin.name] = plugin

    async def reload_all_plugins(self) -> None:
        self.logger.debug("Reloading plugin data of all plugins")

        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            if plugin.enabled:
                await plugin.reload()
                logging.debug(f"{plugin_name} successfully reloaded")

    async def load_all_plugins(self) -> None:
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            await plugin.load()
            logging.debug(f"{plugin_name} successfully loaded")

    async def unload_all_plugins(self) -> None:
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            await plugin.unload()
            logging.debug(f"{plugin_name} successfully unloaded")

    @property
    def requirements(self) -> list[str]:
        # Get all requirements for pip packages from all plugins

        req: list[str] = []
        for plugin_name in self.bot.plugins:
            plugin = self.bot.plugins[plugin_name]
            recieved = plugin.get_requirements()
            for requirement in recieved:
                if not requirement in req:
                    req.append(requirement)

        return req

    def install_requirements(self) -> None:
        "Installs all requirements that plugins require"

        try:
            for i in self.requirements:
                importlib.import_module(i)
        except ImportError:
            logging.warning("Some requirements not found, installing them")
            extended = (
                "\\Scripts\\python.exe" if sys.platform == "win32" else "\\bin\\python"
            )
            command = subprocess.Popen(
                f"{sys.prefix+extended} -m pip install {' '.join(self.requirements)}",
                shell=True,
            )
            command.wait()
