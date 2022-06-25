from typing import TYPE_CHECKING

from models.plugins import PluginData, PluginFiles
from sqlmodel import select

if TYPE_CHECKING:
    from main import ModularBot

class Plugin():
    def __init__(self, plugin_data: PluginData, bot: ModularBot) -> None:
        self.version = plugin_data.version
        self.name = plugin_data.name
        self.description = plugin_data.description
        self.author = plugin_data.author
        self.folder_name = plugin_data.folder_name
        self.enabled = plugin_data.enabled
        self.files: dict[str, str] = {}
        self.id = plugin_data.id

        self.bot = bot
    
    def download(self):
        pass
    
    def get_files(self):
        self.bot.database.exec(select(PluginFiles).where(PluginFiles.plugin_id == self.id))
