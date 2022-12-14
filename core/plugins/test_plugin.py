import logging

import pytest

from core.bot.bot import ModularBot
from core.plugins.plugin import Plugin
from models.plugins import PluginData


@pytest.fixture()
def plugin():
    bot = ModularBot()
    data = PluginData(id=1, url="https://github.com/Stax124/test-plugin", enabled=True)
    return Plugin(data, bot)


def test_plugin_init(plugin: Plugin):
    assert plugin


def test_id(plugin: Plugin):
    assert plugin.id == 1


def test_empty(plugin: Plugin):
    assert plugin.empty == False


def test_enabled(plugin: Plugin):
    assert plugin.enabled == True


def test_repo_url(plugin: Plugin):
    assert plugin.repo and plugin.repo.remotes.origin.url == plugin.repo_url
