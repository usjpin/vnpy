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

    # Config
    CONFIG = 'config'
    WIDTH = 'width'
    HEIGHT = 'height'
    MODE = 'mode'
    # Declaration
    SCENE = 'scene'
    # Statement
    IMAGE = 'image'
    DISPLAY = 'display'
    OPTIONS = 'options'
    AUDIO = 'audio'
    WAIT = 'wait'
    JUMP = 'jump'
    EXIT = 'exit'
    # Other
    SHOW = 'show'
    HIDE = 'hide'
    START = 'start'
    STOP = 'stop'
    CASE = 'case'
    DO = 'do'
    DELAY = 'delay'
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