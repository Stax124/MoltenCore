import importlib
import logging
import subprocess
import sys
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
    
    @property
    def requirements(self) -> list[str]:
        # Get all requirements for pip packages from all plugins
        
        req: list[str] = []
        for plugin in self.bot.plugins:
            recieved = plugin.get_requirements()
            for requirement in recieved:
                if not requirement in req:
                    req.append(requirement)
        
        return req
    
    def install_requirements(self):
        "Installs all requirements that plugins require"
        
        try:
            for i in self.requirements:
                importlib.import_module(i)
        except ImportError:
            logging.warning("Some requirements not found, installing them")
            extended = "\\Scripts\\python.exe" if sys.platform == "win32" else "\\bin\\python"
            command = subprocess.Popen(f"{sys.prefix+extended} -m pip install {' '.join(self.requirements)}", shell=True)
            command.wait()
