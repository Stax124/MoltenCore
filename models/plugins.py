from sqlalchemy import String
from sqlmodel import BigInteger, Column, Field, SQLModel


class PluginData(SQLModel, table=True):
    id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False)
    )
    url: str = Field(sa_column=Column(String(255), nullable=False, server_default=""))
    enabled: bool = Field(default=False)
