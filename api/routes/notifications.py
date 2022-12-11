from core.notifications import Notification
from core.shared import bot
from fastapi import APIRouter

router = APIRouter(tags=["errors"])


@router.get("/")
async def notifications() -> list[Notification]:
    return bot.notification_queue.notifications


@router.get("/clear")
async def clear_notifications():
    bot.notification_queue.clear()
    return {"status": "ok"}
