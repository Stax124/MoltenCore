from fastapi import APIRouter, HTTPException
from core.shared import bot
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["bot"])


class NotReady(Exception):
    pass


@router.get("/icon", response_class=RedirectResponse)
async def get_icon():
    try:
        if not bot.user:
            raise NotReady

        if not bot.user.avatar:
            raise NotReady

        return RedirectResponse(bot.user.avatar.url)

    except NotReady:
        raise HTTPException(status_code=503, detail="Bot is not ready yet")
