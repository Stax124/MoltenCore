import pytest
from sqlmodel.sql.expression import Select, SelectOfScalar

from core.bot.bot import ModularBot

# Fix sqlalchemy caching with sqlmodel
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


@pytest.fixture()
def bot():
    return ModularBot()


def test_bot_init(bot: ModularBot):
    "If the bot is even initializable"
    assert bot


def test_bot(bot: ModularBot):
    "No plugins loaded at start for security reasons"
    assert bot.plugins == {}
