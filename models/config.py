from discord import ActivityType
from sqlalchemy import Boolean, Column, Integer
from sqlmodel import Field, SQLModel
from sqlmodel.sql.sqltypes import AutoString


class Config(SQLModel, table=True):
    main_color: int = Field(default=0xFF0000, primary_key=True, nullable=False)
    activity: str = Field(
        sa_column=Column(
            AutoString(), default="", server_default="commands", nullable=False
        ),
        default="",
    )
    activity_type: int = Field(
        sa_column=Column(
            Integer, nullable=False, server_default=str(ActivityType.listening.value)
        ),
        default=ActivityType.listening,
    )
    paused: bool = Field(
        sa_column=Column(Boolean(), default=False, server_default="0", nullable=False),
        default=False,
    )
