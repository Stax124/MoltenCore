from sqlmodel import BigInteger, Column, Field, SQLModel


class ScheduledTask(SQLModel, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True), default=None)
    guild_id: int = Field(sa_column=Column(BigInteger(), nullable=False))
    owner: int = Field(sa_column=Column(BigInteger(), nullable=False))
    type: str
    data: str
    execute_on: float


class RepeatedTask(SQLModel, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True), default=None)
    guild_id: int = Field(sa_column=Column(BigInteger(), nullable=False))
    owner: int = Field(sa_column=Column(BigInteger(), nullable=False))
    type: str
    data: str
    execute_on: float
    repeat_time: float
    active: bool = Field(default=True, nullable=False)
