from typing import Any, List
from err import ScanErr
from tok import Token, Type

class Scanner:
    keywords = {
        'config': Type.CONFIG,
        'width': Type.WIDTH,
        'height': Type.HEIGHT,
        'mode': Type.MODE,
        'volume': Type.VOLUME,
        'scene': Type.SCENE,
        'image': Type.IMAGE,
        'display': Type.DISPLAY,
        'options': Type.OPTIONS,
        'audio': Type.AUDIO,
        'wait': Type.WAIT,
        'jump': Type.JUMP,
        'exit': Type.EXIT,
        'let': Type.SET,
        'show': Type.SHOW,
        'hide': Type.HIDE,
        'start': Type.START,
        'stop': Type.STOP,
        'case': Type.CASE,
        'do': Type.DO,
        'delay': Type.DELAY,
        'and': Type.AND,
        'else': Type.ELSE,
        'false': Type.FALSE,
        'fun': Type.FUN,
        'if': Type.IF,
        'nil': Type.NIL,
        'or': Type.OR,
        'print': Type.PRINT,
        'return': Type.RETURN,
        'true': Type.TRUE,
        'while': Type.WHILE
    }
    tokens = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source: str):
        self.source = source

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(Type.EOF, '', None, self.line))
        return self.tokens

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def scanToken(self) -> None:
        c = self.advance()
        if c == '(':
            self.addToken(Type.LEFT_PAREN)
        elif c == ')':
            self.addToken(Type.RIGHT_PAREN)
        elif c == '{':
            self.addToken(Type.LEFT_BRACE)
        elif c == '}':
            self.addToken(Type.RIGHT_BRACE)
        elif c == ',':
            self.addToken(Type.COMMA)
        elif c == '.':
            self.addToken(Type.DOT)
        elif c == '-':
            self.addToken(Type.MINUS)
        elif c == '+':
            self.addToken(Type.PLUS)
        elif c == ';':
            self.addToken(Type.SEMICOLON)
        elif c == '*':
            self.addToken(Type.STAR)
        elif c == '!':
            self.addToken(Type.BANG_EQUAL if self.match('=') else Type.BANG)
        elif c == '=':
            self.addToken(Type.EQUAL_EQUAL if self.match('=') else Type.EQUAL)
        elif c == '<':
            self.addToken(Type.LESS_EQUAL if self.match('=') else Type.LESS)
        elif c == '>':
            self.addToken(Type.GREATER_EQUAL if self.match('=') else Type.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(Type.SLASH)
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c == '\n':
            self.line += 1
        elif c == '\"':
            self.readString()
        else:
            if c.isdigit():
                self.readNumber()
            elif c.isalpha() or c == '_':
                self.readIdentifier()
            else:
                raise ScanErr(self.line, "Unexpected Character")

    def readIdentifier(self) -> None:
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        type = Type.IDENTIFIER
        if text in self.keywords:
            type = self.keywords[text]
        self.addToken(type)

    def readNumber(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()
        while self.peek().isdigit():
            self.advance()
        self.addToken(Type.NUMBER, float(self.source[self.start:self.current]))

    def readString(self) -> None:
        while self.peek() != '\"' and not self.isAtEnd():
            if self.peek() == '\n':
                line += 1
            self.advance()
        if self.isAtEnd():
            pass
        self.advance()
        value = self.source[self.start+1:self.current-1]
        self.addToken(Type.STRING, value)

    def match(self, expected):
        if self.isAtEnd() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type: Type, literal: Any = None) -> None:
        text = self.source[self.start:self.current]
        #print(Token(type, text, literal, self.line))
        self.tokens.append(Token(type, text, literal, self.line))

    
