from typing import Optional

from sqlalchemy import String
from sqlmodel import BigInteger, Column, Field, SQLModel, Integer


class PluginPermission:
    NOT_REQUIRED = 0
    REQUESTED = 1
    APPROVED = 2
    DENIED = 3


class PluginPermissions(SQLModel, table=True):
    plugin_id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    database: int = Field(
        sa_column=Column(
            Integer(),
            default=PluginPermission.NOT_REQUIRED,
            server_default=PluginPermission.NOT_REQUIRED.__str__(),
        ),
        default=PluginPermission.NOT_REQUIRED,
    )


class PluginData(SQLModel, table=True):
    id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False)
    )
    url: str = Field(sa_column=Column(String(255), nullable=False, server_default=""))
    enabled: bool = Field(default=False)
