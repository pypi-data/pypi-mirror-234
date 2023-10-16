from typing import Any


class ValuesNotFound(Exception):
    def __init__(self, *args) -> str:
        self.message = args[0] if args else None


    def __str__(self) -> str:
        return f"{self.message}"
    


