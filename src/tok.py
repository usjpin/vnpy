from enum import Enum
from logging.config import IDENTIFIER
from typing import Any

class Type(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    SEMICOLON = ';'
    EOF = ''

    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'

    CONFIG = 'config'
    WIDTH = 'width'
    HEIGHT = 'height'
    MODE = 'mode'
    SCENE = 'scene'
    DISPLAY = 'display'
    AUDIO = 'audio'
    START = 'start'
    STOP = 'stop'
    MESSAGE = 'message'
    OPTION = 'option'
    CASE = 'case'
    DO = 'do'
    WAIT = 'wait'
    JUMP = 'jump'
    EXIT = 'exit'
    CHOICE = 'choice'
    CLICK = 'click'
    KEY = 'key'


class Token:
    def __init__(self, type: Type, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'