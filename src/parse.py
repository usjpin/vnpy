from typing import List

from tok import Token, Type
from expr import *
from stmt import *

class ParseErr(Exception): pass

class Parser:
    current = 0

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self) -> List[Stmt]:
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
            #print(statements[len(statements)-1])
        return statements

    def declaration(self) -> Stmt:
        try:
            return self.statement()
        except ParseErr:
            print("Parse Error")
            self.synchronize()
            return None

    def statement(self) -> Stmt:
        if self.match(Type.SHOW):
            return self.showStatement()
        if self.match(Type.WAIT):
            return self.waitStatement()
        return self.expressionStatement()

    def showStatement(self) -> Stmt:
        if self.match(Type.STRING):
            path = Literal(self.previous().literal)
            return Show(path)
        raise self.error(self.peek(), "Expect String Value")

    def waitStatement(self) -> Stmt:
        if self.match(Type.NUMBER):
            number = Literal(self.previous().literal)
            return Wait(number)
        raise self.error(self.peek(), "Expect Number Value")

    def expressionStatement(self) -> Stmt:
        pass
    
    def match(self, *types: List[Type]):
        for type in types:
            if (self.check(type)):
                self.advance()
                return True
        return False

    def check(self, type: Type) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self) -> bool:
        return self.peek().type == Type.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def consume(self, type: Type, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseErr:
        pass
        return ParseErr()

    def synchronize(self) -> None:
        pass