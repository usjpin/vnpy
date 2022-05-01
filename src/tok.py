from enum import Enum
from typing import Any

# Declare enum of token types
class Type(Enum):
    # List of special characters
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

    # List of comparison operators
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # List of data types
    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'

    # List of reserved keywords
    AND = 'and'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'log'
    RETURN = 'return'
    SET = 'let'
    TRUE = 'true'
    WHILE = 'while'

    # End of file
    EOF = ''

    # VNPy exclusive tokens

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

    # Other
    SHOW = 'show'
    HIDE = 'hide'
    START = 'start'
    STOP = 'stop'
    CASE = 'case'
    DO = 'do'
    DELAY = 'delay'

# Token class
class Token:
    # Constructor to create general token
    def __init__(self, type: Type, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    # toString operator
    def __str__(self) -> str:
        return f'{self.type} {self.lexeme} {self.literal}'