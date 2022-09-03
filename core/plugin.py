import logging
import os
import traceback
from typing import TYPE_CHECKING, Optional

import termcolor
from discord.ext.commands.errors import (
    ExtensionFailed,
    ExtensionNotFound,
    ExtensionNotLoaded,
    NoEntryPointError,
)
from git.repo import Repo
from models.plugins import PluginData

from core.github_parser import Repository

if TYPE_CHECKING:
    from core.bot import ModularBot


class Plugin:
    "Plugin for Discord bot, manages the state and files"

    def __init__(self, plugin_data: PluginData, bot: "ModularBot") -> None:

        self.id = plugin_data.id
        self.enabled = plugin_data.enabled
        self.repo_url = plugin_data.url
        self.repo: Optional[Repo] = None

        # Plugin data
        self.repo_data = Repository(self.repo_url)
        self.name = self.repo_data.name
        self.author = self.repo_data.owner
        self.stars = self.repo_data.stars
        self.forks = self.repo_data.forks
        self.issues = self.repo_data.issues
        self.license = self.repo_data.license
        self.last_updated = self.repo_data.last_updated

        # Traceback
        self.traceback: str = ""
        self.short_traceback: str = ""

        # Logger
        self.logger = logging.getLogger("plugin." + self.name)

        # Bot needs to be here to access the database
        self.bot: "ModularBot" = bot

        self.exists = self.does_exist()
        self.empty = self.executable_files() == []

        # If files are missing and can be downloaded, download them
        if not self.exists:
            self.git_download()
        else:
            self.get_git_repo()

        # If no files are found, disable the plugin
        if self.empty:
            self.logger.warning(f"{self.name} has no files, it will not be loaded")
            self.enabled = False

    def __repr__(self) -> str:
        return f"Plugin(name={self.name}, hash={self.repo.head.object.hexsha if self.repo else 'Unknown'}, enabled={self.enabled})"

    def __str__(self) -> str:
        return f"Plugin(name={self.name}, hash={self.repo.head.object.hexsha if self.repo else 'Unknown'}, enabled={self.enabled})"

    def does_exist(self):
        if os.path.exists(f"plugins/{self.name}") and os.path.exists(
            f"plugins/{self.name}/.git"
        ):
            return True
        else:
            return False

    def generate_safe_path(self, path: str) -> str:
        "Generates a safe path for module loading"

        return f'plugins.{self.name}.{path.replace(".py", "").replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", ".")}'

    def database_models(self):
        return [i for i in os.listdir(f"plugins/{self.name}/models")]

    def executable_files(self):
        if os.path.exists(f"plugins/{self.name}"):
            return [
                i
                for i in os.listdir(f"plugins/{self.name}")
                if i.endswith("_plugin.py")
            ]
        else:
            return []

    async def load(self) -> bool:
        "Loads the plugin files"

        if self.enabled:
            local_files = self.executable_files()
            self.logger.info(f"Loading plugin {self.name}")
            self.logger.debug(f"Files: {local_files}")

            for pythonpath in [self.generate_safe_path(i) for i in local_files]:
                self.logger.debug(f"Loading file {pythonpath}")
                try:
                    await self.bot.load_extension(pythonpath)
                except (
                    ExtensionFailed,
                    ExtensionNotFound,
                    ExtensionNotLoaded,
                    NoEntryPointError,
                ) as e:
                    self.enabled = False
                    self.logger.error(
                        f"{type(e).__name__}: Could not load {pythonpath}"
                    )
                    self.short_traceback = type(e).__name__
                    self.traceback = traceback.format_exc()
                    return False

            self.logger.info(termcolor.colored(f"Loaded plugin {self.name}", "green"))
            return True

        else:
            self.logger.info(f"Plugin {self.name} is disabled")
            return False

    async def unload(self) -> bool:
        "Unloads the plugin files"

        try:
            local_files = self.executable_files()
            self.logger.info(f"Unloading plugin {self.name}")
            self.logger.debug(f"Files: {local_files}")

            for pythonpath in [self.generate_safe_path(i) for i in local_files]:
                self.logger.debug(f"Unloading file {pythonpath}")
                await self.bot.unload_extension(pythonpath)

            return True

        except (ExtensionNotFound, ExtensionNotLoaded) as e:
            self.enabled = False
            self.logger.error(
                f"{type(e).__name__}: Could not unload plugin {self.name}"
            )
            self.traceback = traceback.format_exc(2000)
            return False

    async def reload(self) -> bool:
        "Reloads the plugin files"

        try:
            local_files = self.executable_files()
            self.logger.info(f"Reloading plugin {self.name}")
            self.logger.debug(f"Files: {local_files}")

            for pythonpath in [self.generate_safe_path(i) for i in local_files]:
                self.logger.debug(f"Reloading file {pythonpath}")
                await self.bot.reload_extension(pythonpath)

            return True

        except (
            ExtensionFailed,
            ExtensionNotFound,
            ExtensionNotLoaded,
            NoEntryPointError,
        ) as e:
            self.enabled = False
            self.logger.error(
                f"{type(e).__name__}: Could not reload plugin {self.name}"
            )
            self.traceback = traceback.format_exc(2000)
            return False

    async def enable(self, load: bool) -> None:
        "Marks this plugin as enabled, it will take a reload to apply changes"

        self.enabled = True
        self.bot.database.query(PluginData).filter_by(id=self.id).update(
            {PluginData.enabled: True}
        )

        if load:
            await self.load()

    async def disable(self, unload: bool) -> None:
        "Marks this plugin as disabled, it will take a reload to apply changes"

        self.enabled = False
        self.bot.database.query(PluginData).filter_by(id=self.id).update(
            {PluginData.enabled: False}
        )

        if unload:
            await self.unload()

    def update(self):
        # TODO: Update the plugin

        raise NotImplementedError

    def get_requirements(self) -> list[str]:
        if os.path.exists(f"plugins/{self.name}/requirements.txt"):
            with open(f"plugins/{self.name}/requirements.txt", "r") as f:
                return f.read().splitlines()
        else:
            return []

    def git_download(self):
        self.repo = Repo.clone_from(self.repo_url, f"plugins/{self.name}")

    def get_git_repo(self):
        self.repo = Repo(f"plugins/{self.name}")
