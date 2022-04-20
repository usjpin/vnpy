from enum import Enum
from lib2to3.pgen2.token import GREATER
from logging.config import IDENTIFIER
from typing import Any

class Type(Enum):
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'

    AND = 'and'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SET = 'let'
    TRUE = 'true'
    WHILE = 'while'

    EOF = ''

    # Config
    CONFIG = 'config'
    WIDTH = 'width'
    HEIGHT = 'height'
    MODE = 'mode'
    VOLUME = 'volume'
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
    LOG = 'log' # add
    # Other
    SHOW = 'show'
    HIDE = 'hide'
    START = 'start'
    STOP = 'stop'
    CASE = 'case'
    DO = 'do'
    DELAY = 'delay'


class Token:
    def __init__(self, type: Type, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'