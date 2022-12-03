import logging
from db import generate_engine, get_session
from fastapi import APIRouter, HTTPException
from models.guild import Guild
from sqlmodel import select

router = APIRouter(tags=["guild"])
engine = generate_engine()
db = get_session(engine)


@router.get("/{guild_id}")
async def guild(guild_id: int):
    return db.exec(select(Guild).where(Guild.id == guild_id)).all().__str__()


@router.get("/list")
async def guilds():
    return {"status": "ok", "guilds": db.exec(select(Guild)).all()}


@router.post("/{guild_id}/prefix")
async def prefix(guild_id: int, prefix: str):
    guild = db.exec(select(Guild).where(Guild.id == guild_id)).first()

    if guild:
        guild.prefix = prefix
        db.commit()
        return {"status": "ok"}
    else:
        return HTTPException(status_code=503, detail="Guild not found in database")
