import logging
from typing import TYPE_CHECKING

from models.plugins import PluginData
from sqlmodel import select

from core.plugin import Plugin

if TYPE_CHECKING:
    from main import ModularBot

class PluginHandler():
    "Takes care of managing all the installed plugins"
    
    def __init__(self, bot: "ModularBot") -> None:
        self.logger = logging.getLogger("plugin-handler")
        self.bot = bot
        self.plugin_data = self._find_plugin_data()

    def _find_plugin_data(self) -> list[PluginData]:
        return self.bot.database.exec(select(PluginData)).all()
    
    def populate_plugins(self) -> None:
        self.logger.debug("Populating plugin list")
        
        for data in self.plugin_data:
            self.bot.plugins.append(Plugin(data, self.bot))
    
    def reload_all_plugins(self):
        self.logger.debug("Reloading plugin data of all plugins")
        
        for plugin in self.bot.plugins:
            plugin.reload()

    def load_all_plugins(self):
        for plugin in self.bot.plugins:
            plugin.load()
    
    def unload_all_plugins(self):
        for plugin in self.bot.plugins:
            plugin.unload()
