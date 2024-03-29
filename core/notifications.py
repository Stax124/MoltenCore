from datetime import datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from core.bot import ModularBot

from core.websockets.data import Data


class Notification:
    def __init__(
        self,
        title: str,
        text: str,
        severity: Literal["error", "info", "success", "warning"],
        timeout: int = 3000,
    ) -> None:
        self.title: str = title
        self.text: str = text
        self.severity: Literal["error", "info", "success", "warning"] = severity
        self.timestamp: datetime = datetime.now()
        self.id: int = hash(self)
        self.timeout = timeout

    def __str__(self) -> str:
        return f"{self.title}: {self.text}"

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "message": self.text,
            "severity": self.severity,
            "timeout": self.timeout,
            "timestamp": self.timestamp.isoformat(),
            "id": self.id,
        }

    def to_data(self):
        return Data(type="notification", data=self.to_json())


class NotificationQueue:
    "A queue for storing errors. Primarily for webui"

    def __init__(self, bot: "ModularBot") -> None:
        self.notifications: list[Notification] = []
        self.bot = bot

    async def send(self, nortification: Notification) -> None:
        "Adds an error to the error queue."

        self.notifications.append(nortification)
        await self.bot.websocket.send_data(nortification.to_data())

    def clear(self) -> None:
        "Clears the error queue."

        self.notifications.clear()

    def remove(self, id: int) -> None:
        "Removes an error from the error queue."

        self.notifications = [i for i in self.notifications if i.id != id]
