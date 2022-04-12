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
        # Check Error Handling
        statements = []
        while not self.isAtEnd():
            if (self.match(Type.CONFIG)):
                statements.append(self.config())
            else:
                break
        while not self.isAtEnd():
            statements.append(self.declaration())
            print(statements[len(statements)-1])
        return statements

    def config(self) -> Stmt:
        # Need Error Handling
        if self.match(Type.WIDTH):
            value = self.consume(Type.NUMBER, "Expect Number For Width")
            self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
            return Config(Type.WIDTH, value)
        if self.match(Type.HEIGHT):
            value = self.consume(Type.NUMBER, "Expect Number For Height")
            self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
            return Config(Type.HEIGHT, value)
        if self.match(Type.MODE):
            value = self.consume(Type.STRING, "Expect \'console\' Or \'graphic\' For Mode")
            self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
            return Config(Type.MODE, value)
        # Need Error Handling

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
        if self.match(Type.IMAGE):
            return self.imageStatement()
        if self.match(Type.DISPLAY):
            return self.displayStatement()
        if self.match(Type.OPTIONS):
            return self.optionsStatement()
        if self.match(Type.AUDIO):
            return self.audioStatement()
        if self.match(Type.WAIT):
            return self.waitStatement()
        if self.match(Type.JUMP):
            return self.jumpStatement()
        if self.match(Type.EXIT):
            return self.exitStatement()
        return self.expressionStatement()

    def imageStatement(self) -> Stmt:
        # Change String to Expr
        if self.match(Type.SHOW):
            path = self.consume(Type.STRING, "Expect String For Image")
            self.consume(Type.SEMICOLON, "Expect \';\' After Image")
            return Image(Type.SHOW, path)
        if self.match(Type.HIDE):
            path = self.consume(Type.STRING, "Expect String For Image")
            self.consume(Type.SEMICOLON, "Expect \';\' After Image")
            return Image(Type.HIDE, path)
        raise self.error(self.peek(), "Expect Image Action")

    def displayStatement(self) -> Stmt:
        # Replace String with Expr
        value = self.consume(Type.STRING, "Expect String For Display")
        self.consume(Type.SEMICOLON, "Expect \';\' After Display")
        return Display(value)

    def optionsStatement(self) -> Stmt:
        # Replace String with Expr
        self.consume(Type.LEFT_BRACE, "Expect \'{\' After Options Keyword")
        cases = []
        while not self.check(Type.RIGHT_BRACE) and not self.isAtEnd():
            self.consume(Type.CASE, "Expect \'case\' in Options Block")
            choice = self.consume(Type.STRING, "Expect String For Case")
            self.consume(Type.DO, "Expect \'do\' After Case")
            action = self.statement()
            cases.append((choice, action))
        self.consume(Type.RIGHT_BRACE, "Expect \'}\' After Options Block")
        return Options(cases)

    def audioStatement(self) -> Stmt:
        # Change String to Expr
        if self.match(Type.START):
            path = self.consume(Type.STRING, "Expect String For Audio")
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.START, path)
        if self.match(Type.STOP):
            path = self.consume(Type.STRING, "Expect String For Audio")
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.STOP, path)
        raise self.error(self.peek(), "Expect Audio Action")

    def waitStatement(self) -> Stmt:
        # Change Stuff to Expr
        # Make choice, click and key just callables?
        '''if self.match(Type.CHOICE):
            self.consume(Type.SEMICOLON, "Expect \';\' After Input")
            return Wait(Type.CHOICE, None)
        if self.match(Type.CLICK):
            value = self.consume(Type.NUMBER, "Expect Number For Click")
            self.consume(Type.SEMICOLON, "Expect \';\' After Input")
            return Wait(Type.CLICK, value)
        if self.match(Type.KEY):
            value = self.consume(Type.NUMBER, "Expect Number For Key")
            self.consume(Type.SEMICOLON, "Expect \';\' After Input")
            return Wait(Type.KEY, value)'''
        if self.match(Type.DELAY):
            value = self.consume(Type.NUMBER, "Expect Number For Wait")
            self.consume(Type.SEMICOLON, "Expect \';\' After Wait")
            return Wait(Type.NUMBER, value)
        raise self.error(self.peek(), "Expect Wait Condition")

    def jumpStatement(self) -> Stmt:
        dest = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        self.consume(Type.SEMICOLON, "Expect \';\' After Jump")
        return Jump(dest)

    def exitStatement(self) -> Stmt:
        self.consume(Type.SEMICOLON, "Expect \';\' After Exit")
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