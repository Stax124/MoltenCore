from fastapi import APIRouter, WebSocket
from core.shared import bot
import asyncio

router = APIRouter(tags=["websockets"])


@router.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    bot.websocket.add(websocket)

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@router.websocket("/master")
async def main_websocket(websocket: WebSocket):
    await websocket.accept()

    bot.websocket.add(websocket)

    while True:
        text = await websocket.receive_text()
        if text == "ping":
            await websocket.send_text("pong")
