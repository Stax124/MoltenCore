import os
from typing import TYPE_CHECKING

from models.config import Config
from models.plugins import PluginData
from sqlmodel import select

if TYPE_CHECKING:
    from main import ModularBot

class PluginHandler():
    def __init__(self, bot: "ModularBot") -> None:
        self.bot = bot
        self.plugins = self.find_plugins()

    def find_plugins(self) -> list[PluginData]:
        return self.bot.database.exec(select(PluginData)).all()
    
    def load_plugins(self) -> None:
        pass
