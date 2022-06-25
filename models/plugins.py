from sqlmodel import BigInteger, Column, Field, SQLModel


class PluginData(SQLModel, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    name: str = Field(default="")
    description: str = Field(default="")
    author: str = Field(default="")
    version: str
    folder_name: str
    enabled: bool = Field(default=False)

class PluginFiles(SQLModel, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    plugin_id: int = Field(sa_column=Column(BigInteger(), autoincrement=False))
    file: str
    file_url: str
