from typing import Optional
import discord
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from core.functions.functions import convert_timedelta
from core.shared import bot
from models.config import Config
from api.queue import run_async

router = APIRouter(tags=["system"])


@router.post("/sync-slash-commands")
async def sync_slash_commands():
    return await run_async(bot.sync())


@router.post(
    "/pause",
    responses={
        200: {
            "description": "Pauses the bot from responding to commands from non-owner users"
        },
        503: {"description": "Config not found in database"},
    },
)
async def pause():
    config: Optional[Config] = bot.database.exec(select(Config)).first()

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
        200: {"description": "Resumes the normal operation of the bot"},
        503: {"description": "Config not found in database"},
    },
)
async def unpause():
    config: Optional[Config] = bot.database.exec(select(Config)).first()

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
    config: Optional[Config] = bot.database.exec(select(Config)).first()

    if config:
        return {
            "status": "ok",
            "data": {"paused": config.paused, "activity": config.activity},
        }
    else:
        return HTTPException(status_code=503, detail="Config not found in database")


@router.get("/uptime")
async def uptime() -> str:
    return convert_timedelta(bot.uptime)


@router.get("/healthy")
async def healthy() -> dict[str, str]:
    return {"status": "ok"}
