from typing import Any, List

from err import ScanErr
from tok import Token, Type

# Class to tokenize the file/input strings
class Scanner:
    # Create dict of possible keywords
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
        'log': Type.PRINT,
        'return': Type.RETURN,
        'true': Type.TRUE,
        'while': Type.WHILE
    }
    tokens = []
    start = 0
    current = 0
    line = 1

    # Constructor given source
    def __init__(self, source: str):
        self.source = source

    def scanTokens(self) -> List[Token]:
        # Scan each token until EOF
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        # Create new token at end and add it to the list
        self.tokens.append(Token(Type.EOF, '', None, self.line))
        return self.tokens

    # Helper function to check if scanner is at EOF
    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def scanToken(self) -> None:
        c = self.advance()
        # For each char add corresponding token to list
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
            # This is "//" case - indicates comment
            if self.match('/'):
                # Keep reading until end of line - comment
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
        # Base case - alphanumeric, not symbol
        else:
            # Number case
            if c.isdigit():
                self.readNumber()
            # Alpha case
            elif c.isalpha() or c == '_':
                self.readIdentifier()
            # Raise error for chars not included
            else:
                raise ScanErr(self.line, "Unexpected Character")

    def readIdentifier(self) -> None:
        # While in same word, advance
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        # Create corresponding word that was scanned
        text = self.source[self.start:self.current]
        type = Type.IDENTIFIER
        # Check if scanned word is keyword and update type
        if text in self.keywords:
            type = self.keywords[text]
        self.addToken(type)

    def readNumber(self) -> None:
        # Read entire number
        while self.peek().isdigit():
            self.advance()
        # Check for decimals
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()
        # Read in number after decimal
        while self.peek().isdigit():
            self.advance()
        # Add correct token from substring as number
        self.addToken(Type.NUMBER, float(self.source[self.start:self.current]))

    def readString(self) -> None:
        # Read string within quote
        while self.peek() != '\"' and not self.isAtEnd():
            if self.peek() == '\n':
                line += 1
            self.advance()
        # Scanner gets to end with no end quote
        if self.isAtEnd():
            pass
        self.advance()
        # Get substring from within quote to end quote and add corresponding token
        value = self.source[self.start+1:self.current-1]
        self.addToken(Type.STRING, value)

    def match(self, expected):
        # Return false if at end or diff character
        if self.isAtEnd() or self.source[self.current] != expected:
            return False
        # Otherwise move forward and return true
        self.current += 1
        return True
    
    def peekNext(self):
        # If next is end of string return null terminator
        if self.current + 1 >= len(self.source):
            return '\0'
        # Otherwise peek the next value
        return self.source[self.current + 1]

    def peek(self):
        # If at end return null terminator
        if self.isAtEnd():
            return '\0'
        # Else return current char
        return self.source[self.current]

    def advance(self) -> str:
        # Move forward and read in next char
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type: Type, literal: Any = None) -> None:
        # Get substring of scanned string
        text = self.source[self.start:self.current]
        # Adds new token with correct type and string value
        self.tokens.append(Token(type, text, literal, self.line))

    
