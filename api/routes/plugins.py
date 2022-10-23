from core.shared import bot
from db import generate_engine, get_session
from fastapi import APIRouter, HTTPException
from models.guild import Guild
from sqlmodel import select

router = APIRouter(tags=["plugins"])
engine = generate_engine()
db = get_session(engine)


@router.get("/plugin/{plugin}")
async def plugin(plugin: str):
    if bot.plugins[plugin]:
        return bot.plugins[plugin].to_dict()
    else:
        raise HTTPException(status_code=404, detail="Plugin not found")


@router.get("/")
async def plugins():
    return [i for i in bot.plugins]
