from fastapi import APIRouter, HTTPException

from api.queue import run_async
from core.exceptions import URLException
from core.shared import bot

router = APIRouter(tags=["plugins"])


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


@router.post("/reload-plugin/{plugin}")
async def reload_plugin(plugin: str):
    if bot.plugins[plugin]:
        await run_async(bot.plugins[plugin].reload())
        return bot.plugins[plugin].to_dict()
    else:
        raise HTTPException(status_code=404, detail="Plugin not found")


@router.get("/stats")
async def plugin_stats():
    return {
        "enabled": len([i for i in bot.plugins if bot.plugins[i].enabled]),
        "disabled": len([i for i in bot.plugins if not bot.plugins[i].enabled]),
        "total": len(bot.plugins),
    }


@router.post("/reload-all")
async def reload_all():
    await run_async(bot.plugin_manager.reload_all_plugins())
    return {"status": "ok"}


@router.post("/install-plugin")
async def install_plugin(url: str):
    try:
        await run_async(bot.plugin_manager.install_plugin(url))
    except URLException:
        raise HTTPException(status_code=400, detail="Invalid URL")

    return {"status": "ok"}


@router.post("/remove-plugin/{plugin}")
async def remove_plugin(plugin: str):
    try:
        await run_async(bot.plugin_manager.remove_plugin(plugin))
        return {"status": "ok"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Plugin not found")
