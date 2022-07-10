import sys
from fastapi import FastAPI
from sqlmodel.sql.expression import Select, SelectOfScalar

from db import generate_engine, get_session
from routes import config, guild

app = FastAPI()
engine = generate_engine()
db = get_session(engine)

# sqlmodel stuff
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

app.include_router(config.router)
app.include_router(guild.router)
