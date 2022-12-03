import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes import config, guild, plugins, extensions, system, bot

logger = logging.getLogger(__name__)
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router, prefix="/config")
app.include_router(guild.router, prefix="/guilds")
app.include_router(plugins.router, prefix="/plugins")
app.include_router(extensions.router, prefix="/extensions")
app.include_router(system.router, prefix="/system")
app.include_router(bot.router, prefix="/bot")
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")


@app.get("/")
async def index():
    return FileResponse("frontend/dist/index.html")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("frontend/dist/favicon.ico")
