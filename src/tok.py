from enum import Enum
from logging.config import IDENTIFIER
from typing import Any

class Type(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    EOF = ''

    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'

    # Special
    SHOW = 'show'
    WAIT = 'wait'
    SCENE = 'scene'
    OPTION = 'option'
    DO = 'do'
    JUMP = 'jump'
    EXIT = 'exit'

class Token:
    def __init__(self, type: Type, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'