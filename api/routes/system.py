from typing import Optional
import discord
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from core.shared import bot
from db import generate_engine, get_session
from models.config import Config

router = APIRouter(tags=["system"])
engine = generate_engine()
db = get_session(engine)


@router.post("/sync-slash-commands")
async def sync_slash_commands():
    await bot.sync()
    return {"status": "ok"}


@router.post(
    "/pause",
    responses={
        200: {"description": "Returns the bot status"},
        503: {"description": "Config not found in database"},
    },
)
async def pause():
    config: Optional[Config] = bot.database.query(Config).first()

    if config:
        config.paused = True
        bot.database.commit()

        await bot.change_presence(
            activity=discord.Game(name=f"Paused"), status=discord.Status.do_not_disturb
        )
        return {"status": "ok"}
    else:
        return HTTPException(status_code=503, detail="Config not found in database")


@router.post(
    "/unpause",
    responses={
        200: {"description": "Returns the bot status"},
        503: {"description": "Config not found in database"},
    },
)
async def unpause():
    config: Optional[Config] = db.exec(select(Config)).first()

    if config:
        config.paused = False
        bot.database.commit()

        await bot.change_presence(
            activity=discord.Activity(
                name=config.activity, type=discord.ActivityType.listening
            )
        )
        return {"status": "ok"}
    else:
        return HTTPException(status_code=503, detail="Config not found in database")


@router.get(
    "/status",
    responses={
        200: {"description": "Returns the bot status"},
        503: {"description": "Config not found in database"},
    },
)
async def status():
    config: Optional[Config] = db.exec(select(Config)).first()

    if config:
        return {
            "status": "ok",
            "data": {"paused": config.paused, "activity": config.activity},
        }
    else:
        return HTTPException(status_code=503, detail="Config not found in database")


@router.get("/healthy")
async def healthy():
    return {"status": "ok"}
