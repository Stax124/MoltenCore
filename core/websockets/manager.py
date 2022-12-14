import logging

from fastapi import WebSocket

from .data import Data

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.sockets: list[WebSocket] = []

    def add(self, socket: WebSocket):
        self.sockets.append(socket)

    def remove(self, socket: WebSocket):
        try:
            self.sockets.remove(socket)
        except ValueError:
            pass

    def check_connected(self):
        for socket in self.sockets:
            if not socket.client_state.CONNECTED:
                logger.debug("Removing disconnected socket")
                self.sockets.remove(socket)

    def connected_clients(self):
        "Returns the addresses of connected clients"

        clients: list[str] = []

        for socket in self.sockets:
            if socket.client:
                clients.append(socket.client.host)

        return clients

    async def send_data(self, data: Data):
        self.check_connected()

        for socket in self.sockets:
            try:
                await socket.send_json(data.to_dict())
            except Exception as e:
                logger.error(e)
                self.sockets.remove(socket)
                logger.info(
                    f"Removed socket from list: {socket.client.host if socket.client else 'Unknown'}:{socket.client.port if socket.client else 'Unknown'}"
                )

    def clear(self):
        self.sockets.clear()
