from core.shared import bot
from db import generate_engine, get_session
from fastapi import APIRouter, HTTPException
from api.queue import run_async

router = APIRouter(tags=["plugins"])
engine = generate_engine()
db = get_session(engine)


@router.get("/status/{plugin}")
async def plugin(plugin: str):
    if bot.plugins[plugin]:
        return bot.plugins[plugin].to_dict()
    else:
        raise HTTPException(status_code=404, detail="Plugin not found")


@router.get("/")
async def plugins():
    return [i for i in bot.plugins]


@router.post("/enable-plugin/{plugin}")
async def enable_plugin(plugin: str):
    if bot.plugins[plugin]:
        await run_async(bot.plugins[plugin].enable(load=True))
        return bot.plugins[plugin].to_dict()
    else:
        raise HTTPException(status_code=404, detail="Plugin not found")


@router.post("/disable-plugin/{plugin}")
async def disable_plugin(plugin: str):
    if bot.plugins[plugin]:
        await run_async(bot.plugins[plugin].disable(unload=True))
        return bot.plugins[plugin].to_dict()
    else:
        raise HTTPException(status_code=404, detail="Plugin not found")