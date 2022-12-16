import logging

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from core.shared import bot

router = APIRouter(tags=["websockets"])

logger = logging.getLogger(__name__)


@router.websocket("/master")
async def main_websocket(websocket: WebSocket):
    await websocket.accept()

    bot.websocket.add(websocket)
    logger.debug(
        f"Added websocket to list ({websocket.client.host if websocket.client else 'Unknown'}:{websocket.client.port if websocket.client else 'Unknown'})"
    )

    while True:
        try:
            text = await websocket.receive_text()
            if text == "ping":
                await websocket.send_text("pong")
        except RuntimeError or WebSocketDisconnect:
            try:
                await websocket.close()
            except WebSocketDisconnect:
                pass

            bot.websocket.remove(websocket)
