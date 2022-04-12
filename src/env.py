from typing import Any

from tok import Token
from err import *


class Env:
    values = {}

    def __init__(self, enclosing: 'Env' = None):
        self.enclosing = enclosing
    
    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def assign(self, name: Token, value: Any) -> None:
        pass

    def get(self, name: Token) -> Any:
        if name in self.values:
            return self.values[name]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeErr("Undefined Variable \'" + name.lexeme + "\'")
