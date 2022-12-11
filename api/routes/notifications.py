from core.shared import bot
from fastapi import APIRouter

router = APIRouter(tags=["notifications"])


@router.get("/")
async def notifications():
    return [i.to_json() for i in bot.notification_queue.notifications]


@router.get("/clear")
async def clear_notifications():
    bot.notification_queue.clear()
    return {"status": "ok"}
