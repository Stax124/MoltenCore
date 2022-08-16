import core.shared as shared
from db import generate_engine, get_session
from fastapi import APIRouter
from models.config import Config
from sqlmodel import select

router = APIRouter(tags=["config"])
engine = generate_engine()
db = get_session(engine)


@router.get("/config")
async def config():
    return db.exec(select(Config)).all().__str__()


@router.get("/commands")
async def bot():
    return shared.bot.all_commands.__str__()
