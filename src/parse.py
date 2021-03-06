from typing import List

from tok import Token, Type
from expr import *
from stmt import *
from err import ParseErr

# Parser class - takes in a list of tokens and parses the list.
class Parser:
    current = 0
    hadErr = False

    # Constructor - initializes the tokens variable.
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    # Main parse function. While there are tokens to parse, append the 
    # configuration first, then the statements parsed to the end of the list.
    def parse(self) -> List[Stmt]:
        configs = []
        while not self.isAtEnd():
            if self.match(Type.CONFIG):
                configs.append(self.config())
            else:
                break
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return configs, statements, self.hadErr

    def parseErr(self):
        self.hadErr = True
        self.synchronize()
        return None

    # Expression, returns assignment.
    def expression(self) -> Expr:
        return self.assignment()

    # Config statement
    def config(self) -> Stmt:
        # Try to match
        try:
            # If it's width set the width
            if self.match(Type.WIDTH):
                value = self.consume(Type.NUMBER, "Expect Number For Width")
                self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
                return Config(Type.WIDTH, value)
            # If it's height set the height
            if self.match(Type.HEIGHT):
                value = self.consume(Type.NUMBER, "Expect Number For Height")
                self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
                return Config(Type.HEIGHT, value)
            # If it's mode set the mode
            if self.match(Type.MODE):
                value = self.consume(Type.STRING, "Expect \'console\' Or \'graphic\' For Mode")
                self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
                return Config(Type.MODE, value)
            # If it's volume set the volume
            if self.match(Type.VOLUME):
                value = self.consume(Type.NUMBER, "Expect Number Between 0 to 1 For Volume")
                self.consume(Type.SEMICOLON, "Expect \';\' After Config Statement")
                return Config(Type.VOLUME, value)
        except ParseErr:
            return self.parseErr()

    # Declaration statement
    def declaration(self) -> Stmt:
        # Try to match
        try:
            # If it's set call setDeclaration
            if self.match(Type.SET):
                return self.setDeclaration()
            # If it's a function call function
            if self.match(Type.FUN):
                return self.function("function")
            # If it's a scene call sceneDeclaration
            if self.match(Type.SCENE):
                return self.sceneDeclaration()
            # None of the above - call statement
            return self.statement()
        except ParseErr:
            return self.parseErr()
        
    # Scene declaration
    def sceneDeclaration(self) -> Stmt:
        # Create a scene, storing the name and body
        name = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        self.consume(Type.LEFT_BRACE, "Expect \'{\' Before Scene Body")
        body = self.block()
        return Scene(name, body)

    # Statement
    def statement(self) -> Stmt:
        # Image statement
        if self.match(Type.IMAGE):
            return self.imageStatement()
        # Dsiplay statement
        if self.match(Type.DISPLAY):
            return self.displayStatement()
        # Options statement
        if self.match(Type.OPTIONS):
            return self.optionsStatement()
        # Audio statement
        if self.match(Type.AUDIO):
            return self.audioStatement()
        # Delay statement
        if self.match(Type.DELAY):
            return self.delayStatement()
        # Jump statement
        if self.match(Type.JUMP):
            return self.jumpStatement()
        # Exit statement
        if self.match(Type.EXIT):
            return self.exitStatement()
        # If statement
        if self.match(Type.IF):
            return self.ifStatement()
        # Print statement
        if self.match(Type.PRINT):
            return self.printStatement()
        # Return statement
        if self.match(Type.RETURN):
            return self.returnStatement()
        # While statement
        if self.match(Type.WHILE):
            return self.whileStatement()
        # Left Brace statement
        if self.match(Type.LEFT_BRACE):
            return Block(self.block())
        # Expression statement
        return self.expressionStatement()

    #VNPy Specific Statements

    # Image statement. This executes the showing or hiding of images
    # by creating an image with the according type (show or hide).
    def imageStatement(self) -> Stmt:
        if self.match(Type.SHOW):
            path = self.expression()
            self.consume(Type.SEMICOLON, "Expect \';\' After Image")
            return Image(Type.SHOW, path, self.peek())
        if self.match(Type.HIDE):
            path = self.expression()
            self.consume(Type.SEMICOLON, "Expect \';\' After Image")
            return Image(Type.HIDE, path, self.peek())
        raise self.error(self.peek(), "Expect Image Action")

    # Display statement. Displays the value of the expression.
    def displayStatement(self) -> Stmt:
        value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Display")
        return Display(value, self.peek())

    # Options statement. adds all choices and actions to a case dict
    # and creates an Options statement from them.
    def optionsStatement(self) -> Stmt:
        self.consume(Type.LEFT_BRACE, "Expect \'{\' After Options Keyword")
        cases = []
        while not self.check(Type.RIGHT_BRACE) and not self.isAtEnd():
            self.consume(Type.CASE, "Expect \'case\' in Options Block")
            choice = self.expression()
            self.consume(Type.DO, "Expect \'do\' After Case")
            action = self.statement()
            cases.append((choice, action))
        if len(cases) == 0:
            raise self.error(self.peek(), "Can Not Have Empty Options Block")
        elif len(cases) > 6:
            raise self.error(self.peek(), "Can Not Have More Than 6 Cases In Option Block")
        self.consume(Type.RIGHT_BRACE, "Expect \'}\' After Options Block")
        return Options(cases, self.peek())

    # Audio statement. Checks whether to start or stop audio and creates 
    # an audio statement with the correct type (start or stop).
    def audioStatement(self) -> Stmt:
        if self.match(Type.START):
            path = self.expression()
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.START, path, self.peek())
        if self.match(Type.STOP):
            self.consume(Type.SEMICOLON, "Expect \';\' After Audio")
            return Audio(Type.STOP, None, self.peek())
        raise self.error(self.peek(), "Expect Audio Action")

    # Delay statement. Creates a delay statement with the correct 
    # value (how long to delay).
    def delayStatement(self) -> Stmt:
        value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Delay")
        return Delay(value, self.peek())

    # Jump statement. Creates a jump statement with the destination to jump to.
    def jumpStatement(self) -> Stmt:
        dest = self.consume(Type.IDENTIFIER, "Expect Scene Name")
        self.consume(Type.SEMICOLON, "Expect \';\' After Jump")
        return Jump(dest)

    # Exit statement. Creates an exit statement to exit the VN.
    def exitStatement(self) -> Stmt:
        self.consume(Type.SEMICOLON, "Expect \';\' After Exit")
        return Exit()

    #Standard Statements 

    # If statement   
    def ifStatement(self) -> Stmt:
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After \'If\'")
        condition = self.expression()
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After If Condition")
        thenBranch = self.statement()
        # Optional else branch
        elseBranch = None
        if (self.match(Type.ELSE)):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)
    
    # Print statement
    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Value")
        return Print(value)
    
    # Return statement
    def returnStatement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if (not self.check(Type.SEMICOLON)):
            value = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Return Value")
        return Return(keyword, value)

    # Set declaration
    def setDeclaration(self) -> Stmt:
        name = self.consume(Type.IDENTIFIER, "Expect Variable Name")
        initializer = None
        if self.match(Type.EQUAL):   
            initializer = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Variable Declaration")
        return Set(name, initializer)

    # While statement
    def whileStatement(self) -> Stmt:
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After 'while'")
        condition = self.expression()
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After Condition")
        body = self.statement()
        return While(condition, body)

    # Expression statement
    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(Type.SEMICOLON, "Expect \';\' After Expression")
        return Expression(expr)

    # Function - creates a function using the name, params, and body
    def function(self, kind: str) -> Fun:
        name = self.consume(Type.IDENTIFIER, "Expect " + kind + " Name")
        self.consume(Type.LEFT_PAREN, "Expect \'(\' After " + kind + " Name")
        params = []
        if not self.check(Type.RIGHT_PAREN):
            while True:
                if len(params) >= 255:
                    self.error(self.peek(), "Can't Have More Than 255 Params")
                params.append(self.consume(Type.IDENTIFIER, "Expect Param Name"))
                if not self.match(Type.COMMA):
                    break
        self.consume(Type.RIGHT_PAREN, "Expect \')\' After Params")
        self.consume(Type.LEFT_BRACE, "Expect \'{\' Before " + kind + " Body")
        body = self.block()
        return Fun(name, params, body)

    # Block - creates a block of statements
    def block(self) -> List[Stmt]:
        statements = []
        while not self.check(Type.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(Type.RIGHT_BRACE, "Expect \'}\' After Block")
        return statements

    # Assignment - assigns an expression
    def assignment(self) -> Expr:
        expr = self.orExpression()
        if self.match(Type.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            raise self.error(equals, "Invalid assignment target")
        return expr

    # Or expression
    def orExpression(self) -> Expr:
        expr = self.andExpression()
        while self.match(Type.OR):
            oper = self.previous()
            right = self.andExpression()
            expr = Logical(expr, oper, right)
        return expr

    # And expression
    def andExpression(self) -> Expr:
        expr = self.equality()
        while self.match(Type.AND):
            oper = self.previous()
            right = self.equality()
            expr = Logical(expr, oper, right)
        return expr

    # Equality expression
    def equality(self) -> Expr:
        expr = self.comparison()
        while self.match(Type.BANG_EQUAL, Type.EQUAL_EQUAL):
            oper = self.previous()
            right = self.comparison()
            expr = Binary(expr, oper, right)
        return expr

    # Comparison expression
    def comparison(self) -> Expr:
        expr = self.term()
        while self.match(Type.GREATER, Type.GREATER_EQUAL, Type.LESS, Type.LESS_EQUAL):
            oper = self.previous()
            right = self.term()
            expr = Binary(expr, oper, right)
        return expr

    # Term expression
    def term(self) -> Expr:
        expr = self.factor()
        while self.match(Type.MINUS, Type.PLUS):
            oper = self.previous()
            right = self.factor()
            expr = Binary(expr, oper, right)
        return expr

    # Factor expression
    def factor(self) -> Expr:
        expr = self.unary()
        while self.match(Type.SLASH, Type.STAR):
            oper = self.previous()
            right = self.unary()
            expr = Binary(expr, oper, right)
        return expr

    # Unary expression
    def unary(self) -> Expr:
        if self.match(Type.BANG, Type.MINUS):
            oper = self.previous()
            right = self.unary()
            return Unary(oper, right)
        return self.call()

    # Finish call
    def finishCall(self, callee: Expr) -> Expr:
        args = []
        if not self.check(Type.RIGHT_PAREN):
            while True:
                if len(args) >= 255:
                    raise self.error(self.peek(), "Can't Have More Than 255 Arguments")
                args.append(self.expression())
                if not self.match(Type.COMMA):
                    break
        paren = self.consume(Type.RIGHT_PAREN, "Expect \')\' After Arguments")
        return Call(callee, paren, args)
        
    # Call expression
    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(Type.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break
        return expr

    # Primary expressions, such as true, false, nil number, string,
    # identifier, or left paren.
    def primary(self) -> Expr:
        if self.match(Type.FALSE):
            return Literal(False)
        if self.match(Type.TRUE):
            return Literal(True)
        if self.match(Type.NIL):
            return Literal(None)
        if self.match(Type.NUMBER, Type.STRING):
            return Literal(self.previous().literal)
        if self.match(Type.IDENTIFIER):
            return Variable(self.previous())
        if self.match(Type.LEFT_PAREN):
            expr = self.expression()
            self.consume(Type.RIGHT_PAREN, "Expect ) After Expression")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect Expression")

    # Checks a list of types using the check function
    def match(self, *types: List[Type]):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    # Checks that the type is the same as the peeked type
    def check(self, type: Type) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    # Advances the token
    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    # Checks if parser is at the end of the list of tokens
    def isAtEnd(self) -> bool:
        return self.peek().type == Type.EOF

    # Peeks the next token
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    # Looks at the previous token
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    # Consumes the next token
    def consume(self, type: Type, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    # Throws the ParseErr with the given message
    def error(self, token: Token, message: str) -> ParseErr:
        print("Parse Error")
        return ParseErr(token, message)

    # For use in synchronize
    returnCases = [
        Type.SCENE, Type.FUN, Type.SET, Type.IF, Type.WHILE,
        Type.PRINT, Type.RETURN, Type.IMAGE, Type.DISPLAY, Type.OPTIONS,
        Type.AUDIO, Type.WAIT, Type.JUMP, Type.EXIT
    ]

    # If there is an error, we need to synchronize
    def synchronize(self) -> None:
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == Type.SEMICOLON:
                return
            if self.peek in self.returnCases:
                return
            self.advance()