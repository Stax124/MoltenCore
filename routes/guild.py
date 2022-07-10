from db import generate_engine, get_session
from fastapi import APIRouter
from models.guild import Guild
from sqlmodel import select

router = APIRouter(tags=["guild"])
engine = generate_engine()
db = get_session(engine)

@router.get('/guild/{guild_id}')
async def guild(guild_id: int):
    return db.exec(select(Guild).where(Guild.id == guild_id)).all().__str__()

@router.get('/guilds')
async def guilds():
    return db.exec(select(Guild)).all().__str__()
