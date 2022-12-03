from fastapi import APIRouter
from core.shared import bot

router = APIRouter(tags=["extensions"])


@router.post("/load/{extension}")
async def load(extension: str):
    await bot.load_extension(extension)
    return {"status": "ok"}


@router.post("/unload/{extension}")
async def unload(extension: str):
    await bot.unload_extension(extension)
    return {"status": "ok"}


@router.post("/reload/{extension}")
async def reload(extension: str):
    await bot.reload_extension(extension)
    return {"status": "ok"}
