from sqlmodel import BigInteger, Column, Field, SQLModel


class Guild(SQLModel, table=True):
    id: int = Field(
        sa_column=Column(BigInteger(), primary_key=True, autoincrement=False)
    )
    prefix: str = Field(default="!")
