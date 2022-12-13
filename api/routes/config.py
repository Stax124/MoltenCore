from core.shared import bot
from fastapi import APIRouter
from models.config import Config
from sqlmodel import select

router = APIRouter(tags=["config"])


@router.get("/config")
async def config():
    return bot.database.exec(select(Config)).all().__str__()


@router.get("/commands")
async def commands():
    return list(bot.all_commands).__str__()
