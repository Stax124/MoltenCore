class Errors:
    def __init__(self) -> None:
        self.errors: dict[str, int]

    def __repr__(self) -> list[str]:
        return list(self.errors.keys())

    def add(self, name: str):
        if name in self.errors:
            self.errors[name] += 1
        else:
            self.errors[name] = 1
