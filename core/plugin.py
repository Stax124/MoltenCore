import logging
import os
from typing import TYPE_CHECKING

import requests
import termcolor
from models.plugins import PluginData, PluginFiles
from sqlmodel import select

if TYPE_CHECKING:
    from main import ModularBot

class Plugin():
    def __init__(self, plugin_data: PluginData, bot: ModularBot) -> None:
        # Plugin data
        self.version = plugin_data.version
        self.name = plugin_data.name
        self.description = plugin_data.description
        self.author = plugin_data.author
        self.folder_name = plugin_data.folder_name
        self.enabled = plugin_data.enabled
        self.id = plugin_data.id

        # Bot needs to be here to access the database
        self.bot = bot
        
        # Check if plugin folder exists, if not, create it
        if not os.path.exists(f'plugins/{self.folder_name}'):
            os.mkdir(f'plugins/{self.folder_name}')
        
        # Get all files required for this plugin
        self.files: dict[str, str] = self._get_files()
        self.local, self.non_local_files = self._exists_localy()
        
        if not self.local:
            self.download()
    
    def download(self):
        logging.info(termcolor.colored(f'Downloading {self.name}', 'orange'))
        for file in self.non_local_files:
            file, link = file[0], file[1]
            logging.info(f"Downloading {file}")
            
            r = requests.get(link)
            
            os.makedirs(f'plugins/{self.folder_name}/{file}', exist_ok=True) # Make all necessary folders
            
            with open(f'plugins/{self.folder_name}/{file}', 'wb') as f: # Download the file
                f.write(r.content)
                
            logging.info(termcolor.colored(f'Downloaded {self.name}', 'green'))
    
    def load(self):
        pass

    def unload(self):
        pass
        
    def reload(self):
        pass
    
    def _get_files(self):
        "Populates all files required for this plugin"
        
        plugin_files = self.bot.database.exec(select(PluginFiles).where(PluginFiles.plugin_id == self.id)).all()
        return {file.file: file.file_url for file in plugin_files}

    def _exists_localy(self) -> tuple[bool, list[tuple[str, str]]]:
        "Checks if the plugin is installed locally, if not, returns a list of tuples (file: str, url: str) that are missing"
        
        local = True
        non_local: list[tuple[str, str]] = []
        
        for i in self.files:
            file, link = i[0], i[1]
            
            if not os.path.exists(f'plugins/{file}'):
                non_local.append((file, link))
                local = False
                
        return local, non_local
