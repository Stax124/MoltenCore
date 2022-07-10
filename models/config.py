from sqlmodel import Field, SQLModel


class Config(SQLModel, table=True):
    main_color: int = Field(default=0xFF0000, primary_key=True)
