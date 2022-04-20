from pyclbr import Function
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
        configs = []
        while not self.isAtEnd():
            if self.match(Type.CONFIG):
                configs.append(self.config())
            else:
                break
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
            #print(statements[len(statements)-1])
        return configs, statements

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
        if self.match(Type.VOLUME):
            value = self.consume(Type.NUMBER, "Expect Number Between 0 to 1 For Volume")
            self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
            return Config(Type.VOLUME, value)
        # Need Error Handling

    def declaration(self) -> Stmt:
        try:
            if self.match(Type.SET):
                return self.setDeclaration()
            if self.match(Type.FUN):
                return Function("function")
            if self.match(Type.SCENE):
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

    def setDeclaration(self) -> Stmt:
        name = self.consume(Type.IDENTIFIER, "Expect Variable Name.")
        initializer = None
        if self.match(Type.EQUAL):
            initializer = Expr
        self.consume(Type.SEMICOLON, "Expect \';\' After Variable Declaration.")
        return Stmt(name, initializer)

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
        if self.match(Type.DELAY):
            return self.delayStatement()
        if self.match(Type.JUMP):
            return self.jumpStatement()
        if self.match(Type.EXIT):
            return self.exitStatement()
        if self.match(Type.IF):
            return self.ifStatement()
        if self.match(Type.PRINT):
            return self.printStatement()
        if self.match(Type.RETURN):
            return self.returnStatement()
        if self.match(Type.WHILE):
            return self.whileStatement()
        if self.match(Type.LEFT_BRACE):
            return Stmt(self.block())
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
        if len(cases) == 0:
            raise self.error(self.peek(), "Can Not Have Empty Options Block")
        elif len(cases) > 6:
            raise self.error(self.peek(), "Can Not Have More Than 6 Cases In Option Block")
        self.consume(Type.RIGHT_BRACE, "Expect \'}\' After Options Block")
        return Options(cases)

    def audioStatement(self) -> Stmt:
        # Change String to Expr
        if self.match(Type.START):
            path = self.consume(Type.STRING, "Expect String For Audio")
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.START, path)
        if self.match(Type.STOP):
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.STOP, None)
        raise self.error(self.peek(), "Expect Audio Action")

    def delayStatement(self) -> Stmt:
        # Change Stuff to Expr
        value = self.consume(Type.NUMBER, "Expect Number For Delay")
        self.consume(Type.SEMICOLON, "Expect \';\' After Delay")
        return Delay(value)

    def jumpStatement(self) -> Stmt:
        dest = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        self.consume(Type.SEMICOLON, "Expect \';\' After Jump")
        return Jump(dest)

    def exitStatement(self) -> Stmt:
        self.consume(Type.SEMICOLON, "Expect \';\' After Exit")
        return Exit()
    
    def ifStatement(self) -> Stmt:
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After \'If\'.")
        condition = self.expression()
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After If Condition.")
        thenBranch = self.statement()
        elseBranch = None
        if (self.match(Type.ELSE)):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)
    
    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Value.")
        return Print(value)
    
    def returnStatement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if (not self.check(Type.SEMICOLON)):
            value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Return Value.")
        return Stmt(keyword, value)

    def whileStatement(self) -> Stmt:
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After 'while'.")
        condition = self.expression()
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After Condition.")
        body = self.statement()
        return Return(condition, body)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Expression")
        return Expression(expr)

    def function(self, kind: str) -> Function:
        name = self.consume(Type.IDENTIFIER, "Expect " + kind + " Name.")
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After " + kind + " Name.")
        params = []
        if not self.check(Type.RIGHT_PAREN):
            while True:
                if params.count >= 255:
                    self.error(self.peek(), "Can't Have More Than 255 Params.")
                params.append(self.consume(Type.IDENTIFIER, "Expect Param Name."))
                if not self.match(Type.COMMA):
                    break
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After Params.")
        self.consume(Type.LEFT_BRACE, "Expect \'{\' Before " + kind + " Body.")
        body = self.block()
        return Function(name, params, body)

    def assignment(self) -> Expr:
        expr = self.orExpression()
        if self.match(Type.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if expr.__getattribute__ == type(Variable):
                name = Variable(expr).name
                return Assign(name, value)
            elif expr.__getattribute__ == type(Get):
                get = Get(expr)
                return Set(get.obj, get.name, value)
            Error(equals, "Invalid assignment target")
        return expr

    def orExpression(self) -> Expr:
        expr = self.andExpression()
        while self.match(Type.OR):
            oper = self.previous()
            right = self.andExpression()
            expr = Logical(expr, oper, right)
        return expr

    def andExpression(self) -> Expr:
        expr = self.equality()
        while self.match(Type.AND):
            oper = self.previous()
            right = self.equality()
            expr = Logical(expr, oper, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(Type.BANG_EQUAL, Type.EQUAL_EQUAL):
            oper = self.previous()
            right = self.comparison()
            expr = Binary(expr, oper, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(Type.GREATER, Type.GREATER_EQUAL, Type.LESS, Type.LESS_EQUAL):
            oper = self.previous()
            right = self.term()
            expr = Binary(expr, oper, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self.match(Type.MINUS, Type.PLUS):
            oper = self.previous()
            right = self.factor()
            expr = Binary(expr, oper, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(Type.SLASH, Type.STAR):
            oper = self.previous()
            right = self.unary()
            expr = Binary(expr, oper, right)
        return expr

    def unary(self) -> Expr:
        if self.match(Type.BANG, Type.MINUS):
            oper = self.previous()
            right = self.unary()
            return Unary(oper, right)
        return self.call()

    def finishCall(self, callee: Expr) -> Expr:
        args = []
        if not self.check(Type.RIGHT_PAREN):
            while True:
                if args.count >= 255:
                    Error(self.peek(), "Can't Have More Than 255 Arguments.")
                args.append(self.expression())
                if self.match(Type.COMMA):
                    break
        
    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(Type.LEFT_PAREN):
                expr = self.finishCall(expr)
            elif self.match(Type.DOT):
                name = self.consume(Type.IDENTIFIER, "Expect Property Name After \'.\'.")
                expr = Get(expr, name)
            else:
                break
        return expr

    def primary(self) -> Expr:
        pass #Was here

    def match(self, *types: List[Type]):
        for type in types:
            if self.check(type):
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