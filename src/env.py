from typing import Any

from tok import Token

class Env:
    values = {}

    def __init__(self, enclosing: 'Env' = None):
        self.enclosing = enclosing

    def get(name: Token) -> Any:
        pass

    def assign(name: Token, value: Any) -> None:
        pass
    
    def define(name: str, value: Any) -> None:
        pass
