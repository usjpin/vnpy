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
            if (self.match(Type.SCENE)):
                return self.sceneDeclaration()
            return self.statement()
        except ParseErr:
            print("Parse Error")
            print(self.tokens[self.current])
            self.synchronize()
            return None
        
    def sceneDeclaration(self) -> Stmt:
        name = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        self.consume(Type.LEFT_BRACE, "Expect \'{\' Before Scene Body")
        body = self.block()
        return Scene(name, body)
    
    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(Type.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(Type.RIGHT_BRACE, "Expect \'}\' After Block")
        return statements

    def statement(self) -> Stmt:
        if self.match(Type.SHOW):
            return self.showStatement()
        if self.match(Type.WAIT):
            return self.waitStatement()
        if self.match(Type.OPTION):
            return self.optionStatement()
        if self.match(Type.JUMP):
            return self.jumpStatement()
        if self.match(Type.EXIT):
            return self.exitStatement()
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

    def optionStatement(self) -> Stmt:
        if not self.match(Type.STRING):
            raise self.error(self.peek(), "Expect String Value")
        message = Literal(self.previous().literal)
        self.consume(Type.DO, "Expect \'do\' After Option Message")
        action = self.statement()
        return Option(message, action)

    def jumpStatement(self) -> Stmt:
        dest = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        return Jump(dest)

    def exitStatement(self) -> Stmt:
        return Exit()

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