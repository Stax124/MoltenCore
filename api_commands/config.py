from typing import TYPE_CHECKING

from .commands import commands

if TYPE_CHECKING:
    from ..main import ModularBot


def test(bot: "ModularBot", *args, **kwargs):
    pass
