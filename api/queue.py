import asyncio
import logging
from typing import Coroutine

from fastapi import HTTPException

from core.queue import Status as QueueStatus
from core.shared import bot


async def run_async(
    coroutine: Coroutine,
    ok: dict = {"status": "ok"},
    error: HTTPException = HTTPException(
        status_code=503, detail="Error running async command"
    ),
) -> HTTPException | dict[str, str]:
    _id = bot.queue.add(coroutine)
    while not bot.queue.ready(_id):
        await asyncio.sleep(0.1)

    logging.info("Sync finished, retrieving status")
    if bot.queue.get(_id).status == QueueStatus.error:
        return error

    bot.queue.remove(_id)

    return ok
