from typing import Any

from tok import Token, Type

class Scanner:
    keywords = {
        'show': Type.SHOW,
        'wait': Type.WAIT
    }
    tokens = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source: str):
        self.source = source

    def scanTokens(self) -> None:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(Type.EOF, '', None, self.line))
        return self.tokens

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def scanToken(self) -> None:
        c = self.advance()
        if c == ' ' or c == '\r' or c == '\t':
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
                pass

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

    
