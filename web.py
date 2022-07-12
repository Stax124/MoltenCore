from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel.sql.expression import Select, SelectOfScalar
from starlette.responses import FileResponse

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
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/")
async def index():
    return FileResponse("index.html")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("favicon.ico")
