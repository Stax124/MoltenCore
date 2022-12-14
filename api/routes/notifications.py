from fastapi import APIRouter

from core.shared import bot

router = APIRouter(tags=["notifications"])


@router.get("/")
async def notifications():
    return [i.to_json() for i in bot.notification_queue.notifications]


@router.post("/clear")
async def clear_notifications():
    bot.notification_queue.clear()
    return {"status": "ok"}


@router.post("/clear/{id}")
async def clear_notification(id: int):
    bot.notification_queue.remove(id)
    return {"status": "ok"}
