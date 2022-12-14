from fastapi import APIRouter
from sqlmodel import select

from core.shared import bot
from models.config import Config

router = APIRouter(tags=["config"])


@router.get("/config")
async def config():
    return bot.database.exec(select(Config)).all().__str__()


@router.get("/commands")
async def commands():
    return list(bot.all_commands).__str__()
