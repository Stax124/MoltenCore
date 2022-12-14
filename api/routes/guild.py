from fastapi import APIRouter, HTTPException
from sqlmodel import select

from core.shared import bot
from models.guild import Guild

router = APIRouter(tags=["guild"])


@router.get("/{guild_id}")
async def guild(guild_id: int):
    return bot.database.exec(select(Guild).where(Guild.id == guild_id)).all().__str__()


@router.get("/list")
async def guilds():
    return {"status": "ok", "guilds": bot.database.exec(select(Guild)).all()}


@router.post("/{guild_id}/prefix")
async def prefix(guild_id: int, prefix: str):
    guild = bot.database.exec(select(Guild).where(Guild.id == guild_id)).first()

    if guild:
        guild.prefix = prefix
        bot.database.commit()
        return {"status": "ok"}
    else:
        return HTTPException(status_code=503, detail="Guild not found in database")
