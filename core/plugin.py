import logging
import os
from typing import TYPE_CHECKING

import requests
import termcolor
from discord.ext.commands.errors import (ExtensionFailed, ExtensionNotFound,
                                         ExtensionNotLoaded, NoEntryPointError)
from models.plugins import PluginData, PluginFiles
from sqlmodel import select

if TYPE_CHECKING:
    from main import ModularBot

class Plugin():
    "Plugin for Discord bot, manages the state and files"
    
    def __init__(self, plugin_data: PluginData, bot: "ModularBot") -> None:

        # Plugin data
        self.version = plugin_data.version
        self.name = plugin_data.name
        self.description = plugin_data.description
        self.author = plugin_data.author
        self.folder_name = plugin_data.folder_name
        self.enabled = plugin_data.enabled
        self.id = plugin_data.id

        # Logger
        self.logger = logging.getLogger("plugin."+self.name)

        # Bot needs to be here to access the database
        self.bot = bot
        
        # Check if plugin folder exists, if not, create it
        if not os.path.exists(f'plugins/{self.folder_name}'):
            os.mkdir(f'plugins/{self.folder_name}')
        
        # Get all files required for this plugin
        self.files: dict[str, str] = self._get_files()
        self.empty: bool = len(self.files) == 0
        self.local, self.non_local_files, self.local_files = self._exists_localy()
        
        # If no files are found and can't be downloaded, disable the plugin
        if self.empty:
            self.logger.warning(f"{self.name} has no files, it will not be loaded")
            self.enabled = False
        
        # If files are missing and can be downloaded, download them
        if not self.local and not self.empty:
            self._download()
    
    def generate_safe_path(self, path: str) -> str:
        "Generates a safe path for module loading"
        
        return f'plugins.{self.folder_name}.{path.replace(".plugin.py", "").replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", ".")}'
    
    def _download(self):
        "Downloads the necessary files for this plugin"
        
        try:
            self.logger.info(termcolor.colored(f'Downloading files for plugin `{self.name}`', 'yellow'))
            
            for file in self.non_local_files:
                file, link = file[0], file[1]
                self.logger.info(f"Downloading {file}")
                
                r = requests.get(link)
                
                os.makedirs(os.path.dirname(f'plugins/{self.folder_name}/{file}'), exist_ok=True) # Make all necessary folders
                
                with open(f'plugins/{self.folder_name}/{file}', 'wb') as f: # Download the file
                    f.write(r.content)
                    
                self.logger.info(termcolor.colored(f'Downloaded {file}', 'green'))
                self.local_files.append(file)
                
        except ConnectionError as e:
            self.logger.error(termcolor.colored(f'Could not download {self.name}: {e}', 'red'))
    
    def load(self):
        "Loads the plugin files"
        
        try:
            self.logger.info(f"Loading plugin {self.name}")
            self.logger.debug(f"Files: {self.local_files}")
            
            for pythonpath in [self.generate_safe_path(i) for i in self.local_files]:
                self.logger.debug(f"Loading file {pythonpath}")
                self.bot.load_extension(pythonpath)
                
        except (ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError) as e:
            self.enabled = False
            self.logger.error(f"{type(e).__name__}: Could not load plugin {self.name}")

    def unload(self):
        "Unloads the plugin files"
        
        try:
            self.logger.info(f"Unloading plugin {self.name}")
            self.logger.debug(f"Files: {self.local_files}")
            
            for pythonpath in [self.generate_safe_path(i) for i in self.local_files]:
                self.logger.debug(f"Unloading file {pythonpath}")
                self.bot.unload_extension(pythonpath)
                
        except (ExtensionNotFound, ExtensionNotLoaded) as e:
            self.enabled = False
            self.logger.error(f"{type(e).__name__}: Could not unload plugin {self.name}")

    def reload(self):
        "Reloads the plugin files"
        
        try:
            self.logger.info(f"Reloading plugin {self.name}")
            self.logger.debug(f"Files: {self.local_files}")
            
            for pythonpath in [self.generate_safe_path(i) for i in self.local_files]:
                self.logger.debug(f"Reloading file {pythonpath}")
                self.bot.reload_extension(pythonpath)
                
        except (ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError) as e:
            self.enabled = False
            self.logger.error(f"{type(e).__name__}: Could not reload plugin {self.name}")
    
    def enable(self):
        self.enabled = True
        self.bot.database.query(PluginData).filter_by(id=self.id).update({PluginData.enabled: True})
    
    def disable(self):
        self.enabled = False
        self.bot.database.query(PluginData).filter_by(id=self.id).update({PluginData.enabled: False})
        
    def _get_files(self):
        "Populates all files required for this plugin"
        
        plugin_files = self.bot.database.exec(select(PluginFiles).where(PluginFiles.plugin_id == self.id)).all()
        return {file.file: file.file_url for file in plugin_files}

    def _exists_localy(self) -> tuple[bool, list[tuple[str, str]], list[str]]:
        "Checks if the plugin is installed locally, if not, returns a list of tuples (file: str, url: str) that are missing"
        
        local = True
        non_local_files: list[tuple[str, str]] = []
        local_files: list[str] = []
        
        for file in self.files:
            link = self.files[file]
            
            if not os.path.exists(f'plugins/{self.folder_name}/{file}'):
                non_local_files.append((file, link))
                local = False
            else:
                local_files.append(file)
        
        return local, non_local_files, local_files
