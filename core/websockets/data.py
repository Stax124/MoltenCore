from typing import Any, Literal


class Data:
    def __init__(self, data: dict, type: str):
        self.data = data
        self.type = type

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "data": self.data}


def notification(
    severity: Literal["info", "success", "warning", "error"],
    message: str,
    timeout: int = 0,
) -> Data:
    return Data(
        {"severity": severity, "message": message, "timeout": timeout},
        "notification",
    )
