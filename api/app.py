import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes import config, guild, plugins

logger = logging.getLogger(__name__)
origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(guild.router, prefix="/guilds", tags=["guild"])
app.include_router(plugins.router, prefix="/plugins", tags=["plugins"])
app.mount("/assets", StaticFiles(directory="./frontend/dist/assets"), name="assets")


@app.get("/")
async def index():
    logger.info("index")
    return FileResponse("../frontend/dist/index.html")
