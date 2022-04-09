from enum import Enum
from typing import Any

class Type(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'

class Token:
    def __init__(self, type: Type, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'