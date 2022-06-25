from sqlmodel import Field, SQLModel


class Config(SQLModel, table=True):
    main_color: int = Field(default=0xff0000, primary_key=True)
