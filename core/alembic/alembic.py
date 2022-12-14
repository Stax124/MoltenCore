from alembic import command
from alembic.config import Config


# Migrate the database to the latest version
def upgrade(config: str = "alembic.ini"):
    alembic_cfg = Config(config)
    command.upgrade(alembic_cfg, "head")


def check_if_up_to_date(config: str = "alembic.ini"):
    alembic_cfg = Config(config)
    command.current(alembic_cfg)
