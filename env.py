from typing import Any

from token import Token

class Env:
    def __init__(self, enclosing: 'Env'):
        pass
    def get(name: Token) -> Any:
        pass
    def assign(name: Token, value: Any) -> None:
        pass
    def define(name: str, value: Any) -> None:
        pass
