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
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeErr(name, "Undefined Variable \'" + name.lexeme + "\' During Assignment.")

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeErr(name, "Undefined Variable \'" + name.lexeme + "\'")
