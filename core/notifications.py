from discord.ext.commands import CommandError
import enum


class NotificationSeverity(enum.Enum):
    MESSAGE = enum.auto()
    ERROR = enum.auto()
    WARNING = enum.auto()


class Notification:
    def __init__(self, title: str, text: str, severity: NotificationSeverity) -> None:
        self.title = title
        self.text = text
        self.severity = severity

    def __str__(self) -> str:
        return f"{self.title}: {self.text}"


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
