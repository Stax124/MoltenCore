from core.shared import bot
from fastapi import APIRouter

router = APIRouter(tags=["errors"])


@router.get("/")
async def errors():
    errors = bot.errors.errors
    errors.sort(key=lambda x: x.time, reverse=True)
    data = []

    for error in errors:
        data.append(
            {
                "id": error.id,
                "command": error.command,
                "guild": {
                    "name": error.guild.name if error.guild else None,
                    "id": error.guild.id if error.guild else None,
                },
                "called_by": {
                    "name": error.called_by.name,
                    "id": error.called_by.id,
                },
                "args": error.args.__str__(),
                "time": error.time.strftime("%d/%m/%Y %H:%M:%S"),
                "cog": error.cog.qualified_name if error.cog else None,
            }
        )

    return data


@router.get("/clear")
async def clear_errors():
    bot.errors.clear()
    return {"status": "ok"}
