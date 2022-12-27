import json
import logging
import os
import pathlib
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
from sqlmodel import select

from core.functions.delete import delete_folder
from core.parser.github_parser import Repository
from core.plugins.plugin_encoder import PluginEncoder
from models.plugins import PluginData, PluginPermission, PluginPermissions

if TYPE_CHECKING:
    from core.bot.bot import ModularBot


class Plugin:
    "Plugin for Discord bot, manages the state and files"

    def __init__(self, plugin_data: PluginData, bot: "ModularBot") -> None:

        self.id: int = plugin_data.id
        self.enabled: bool = plugin_data.enabled
        self.repo_url: str = plugin_data.url
        self.repo: Optional[Repo] = None
        self.plugin_data: PluginData = plugin_data

        # Plugin data
        self.repo_data: Repository = Repository(self.repo_url)
        self.name = self.repo_data.name
        self.author = self.repo_data.owner
        self.stars = self.repo_data.stars
        self.forks = self.repo_data.forks
        self.issues = self.repo_data.issues
        self.license = self.repo_data.license
        self.last_updated = self.repo_data.last_updated

        # Logger
        self.logger: logging.Logger = logging.getLogger("plugin." + self.name)

        # Bot needs to be here to access the database
        self.bot: "ModularBot" = bot

        # Traceback
        self.traceback: str = ""
        self.short_traceback: str = ""

        self.initialize()

    def __repr__(self) -> str:
        return f"Plugin(name={self.name}, hash={self.repo.head.object.hexsha if self.repo else 'Unknown'}, enabled={self.enabled})"

    def __str__(self) -> str:
        return f"Plugin(name={self.name}, hash={self.repo.head.object.hexsha if self.repo else 'Unknown'}, enabled={self.enabled})"

    def to_dict(self) -> dict:
        encoder: PluginEncoder = PluginEncoder()
        return encoder.default(self)

    def initialize(self) -> None:
        self.exists = self.does_exist()
        self.empty = self.executable_files() == []

        # If files are missing and can be downloaded, download them
        if not self.exists:
            self.git_clone()
        else:
            self.get_git_repo()

        # If no files are found, disable the plugin
        if self.empty:
            self.logger.warning(f"{self.name} has no files, it will not be loaded")
            self.enabled = False

        # Permissions
        self.permissions: PluginPermissions = self.get_permissions()

    def does_exist(self) -> bool:
        if os.path.exists(f"plugins/{self.name}") and os.path.exists(
            f"plugins/{self.name}/.git"
        ):
            return True
        else:
            return False

    def get_permissions(self) -> PluginPermissions:
        db_perms: list[PluginPermissions] = self.bot.database.exec(
            select(PluginPermissions).where(PluginPermissions.plugin_id == self.id)
        ).all()

        if db_perms:
            return db_perms[0]
        else:
            return self.generate_permissions()

    def generate_permissions(self) -> PluginPermissions:
        "Check if plugin requires any permissions, if so, make changes in the database"

        permissions: PluginPermissions = PluginPermissions(plugin_id=self.id)

        self.logger.debug(
            f"Plugin {self.name} has no permissions in the database, generating"
        )

        config_file: str = f"plugins/{self.name}/plugin.json"
        if os.path.exists(config_file):
            try:
                config: dict = json.load(open(config_file, "r"))
            except json.JSONDecodeError:
                config: dict = {}
        else:
            config: dict = {}

        if config.get("permissions", []):
            self.logger.debug(
                f"Permissions for plugin {self.name}: {config.get('permissions', [])}"
            )
            for permission in config.get("permissions", []):
                if permissions.__dict__[permission] and (
                    permissions.__dict__[permission] != PluginPermission.APPROVED
                    or permissions.__dict__[permission] != PluginPermission.DENIED
                ):
                    permissions.__dict__[permission] = PluginPermission.REQUESTED
        else:
            self.logger.debug(f"No permissions required for plugin {self.name}")

        self.bot.database.add(permissions)
        self.bot.database.commit()
        return permissions

    def generate_safe_path(self, path: str) -> str:
        "Generates a safe path for module loading"

        return f'plugins.{self.name}.{path.replace(".py", "").replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", ".")}'

    def database_models(self):
        "Returns a list of all the database models in the plugin repository"

        return [i for i in os.listdir(f"plugins/{self.name}/models")]

    def executable_files(self):
        "Returns a list of files that can be executed by the bot"

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
        self.bot.database.commit()

        if load:
            await self.load()

    async def disable(self, unload: bool) -> None:
        "Marks this plugin as disabled, it will take a reload to apply changes"

        self.enabled = False
        self.bot.database.query(PluginData).filter_by(id=self.id).update(
            {PluginData.enabled: False}
        )
        self.bot.database.commit()

        if unload:
            await self.unload()

    def update(self):
        "Resets current repository and updates the plugin files"

        if self.repo:
            self.logger.info(f"Updating plugin {self.name}")
            self.repo.head.reset(index=True, working_tree=True)
            self.repo.remotes.origin.pull()
        else:
            self.logger.error(f"Could not update plugin {self.name}: Repo not loaded")

    def check_update(self) -> bool:
        "Checks if the plugin has an update on remote"

        if self.repo:
            return (
                self.repo.head.object.hexsha
                == self.repo.remote().refs.main.object.hexsha
            )
        else:
            self.logger.error(f"Could not update plugin {self.name}: Repo not loaded")
            return False

    async def remove(self):
        "Removes the plugin files, database entries and the plugin folder"

        self.logger.info(f"Removing plugin {self.name}")
        await self.unload()

        # Remove the database entries
        self.bot.database.delete(self.plugin_data)
        self.bot.database.delete(self.permissions)

        # Commit the changes
        self.bot.database.commit()

        if self.repo:
            self.repo.close()
            del self.repo

        # Remove the folder
        path = pathlib.Path(f"plugins/{self.name}")
        delete_folder(path)

    def get_requirements(self) -> list[str]:
        "Reads the requirements.txt file and returns a list of requirements"

        if os.path.exists(f"plugins/{self.name}/requirements.txt"):
            with open(f"plugins/{self.name}/requirements.txt", "r") as f:
                return f.read().splitlines()
        else:
            return []

    def git_clone(self):
        "Clones the plugin repository"
        self.repo = Repo.clone_from(
            self.repo_url, f"plugins/{self.name}", single_branch=True
        )

        # Recheck if there are files to be loaded
        self.exists = self.does_exist()
        self.empty = self.executable_files() == []

    def get_git_repo(self):
        "Gets all the git information from the plugin repository"
        self.repo = Repo(f"plugins/{self.name}")
