from configparser import ConfigParser

from sqlmodel import Session
from sqlmodel import create_engine as _create_engine

config = ConfigParser()
config.read("alembic.ini")


def generate_engine(verbose=False):
    return _create_engine(config["alembic"]["sqlalchemy.url"], echo=verbose)


def get_session(engine):
    with Session(engine) as session:
        return session
