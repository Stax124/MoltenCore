import enum
from datetime import datetime


class NotificationSeverity(enum.Enum):
    MESSAGE = "message"
    ERROR = "error"
    WARNING = "warning"


class Notification:
    def __init__(self, title: str, text: str, severity: NotificationSeverity) -> None:
        self.title: str = title
        self.text: str = text
        self.severity: NotificationSeverity = severity
        self.timestamp: datetime = datetime.now()

    def __str__(self) -> str:
        return f"{self.title}: {self.text}"

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "text": self.text,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
        }


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
