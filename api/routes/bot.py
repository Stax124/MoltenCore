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


@router.get("/status")
async def status():
    return {
        "ready": bot.is_ready(),
        "banner": bot.user.banner.url if bot.user and bot.user.banner else None,
        "created_at": bot.user.created_at if bot.user else None,
        "display_name": bot.user.display_name if bot.user else None,
        "id": str(bot.user.id) if bot.user else None,
        "name": bot.user.name if bot.user else None,
        "guilds": len(bot.guilds),
        "members": len(bot.users),
    }
