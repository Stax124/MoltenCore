from typing import Literal
from datetime import datetime

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

    def __init__(self) -> None:
        self.notifications: list[Notification] = []

    def add(self, nortification: Notification) -> None:
        "Adds an error to the error queue."

        self.notifications.append(nortification)

    def clear(self) -> None:
        "Clears the error queue."

        self.notifications.clear()
