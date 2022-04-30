import os
import sys
from typing import List

from expr import *
from stmt import *
from game import *
from env import Env
from call import *
from err import *

# Interpreter class. Responsible for interpreting, executing, evaluating,
# resolving, etc. It also utilizes the visitor pattern
class Interpreter(ExprVisitor, StmtVisitor):

    # Default constructor. Initialize globals, env, locals, and config
    def __init__(self):
        self.globals = Env()
        self.env = self.globals
        self.locals = {}
        self.config = {
            'width': 500,
            'height': 500,
            'mode': 'graphic',
            'volume': 0.5
        }
        self.globals.define("waitClick", VNClickCallable())
        self.globals.define("waitKey", VNKeyCallable())

    # Interpret a list of statements
    def interpret(self, configs: List[Config], statements: List[Stmt]) -> None:
        # Error Handling
        try:
            for statement in configs:
                self.execute(statement)
        except RuntimeErr as e:
            e.printErr()
            return True
        # If specified to be graphic, start GUI version. Else start console version.
        if self.config["mode"] == "graphic":
            self.game = VNGUIGame(
                self.config["width"],
                self.config["height"],
                self.config["volume"]
            )
        else:
            self.game = VNConsoleGame()
        # Execute each statement, catching errors if they occur
        while statements is not None:
            current = statements
            statements = None
            try:
                for statement in current:
                    self.execute(statement)
            except JumpErr as j:
                self.env = j.scene.env
                statements = j.scene.body
                #print('Trying to Jump')
                #print(self.env)
                #print(statements)
            except ReturnErr as r:
                self.value = r.value
            except RuntimeErr as e:
                e.printErr()
                return True
        return False

    # Execute a statement
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    # Evaluate an expression, utilizing the visitor pattern
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    # Execute a block of statements given an env
    def executeBlock(self, statements: List[Stmt], environment: Env):
        # Store previous environment
        previous = self.env
        # Try to execute each statement and update the environment
        try:
            self.env = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous

    # Resolves the given path or causes an error if it doesn't exist
    def resolvePath(self, path: str, tok: Token) -> str:
        if not os.path.exists(path):
            raise RuntimeErr(tok, "Path \'" + path + "\' Does Not Exist")
        return path

    # Checks to ensure that the graphic mode is on.
    def checkGraphic(self, tok: Token, msg: str) -> None:
        if self.config["mode"] != "graphic":
            raise RuntimeErr(tok, msg)

    # Config statement visitor function. Sets the config values to what is given.
    def visitConfigStmt(self, stmt: Config):
        # print("Interpreting Config")
        self.config[stmt.config.value] = stmt.value.literal

    # Scene statement visitor function. Instantiates and defines
    # the given scene.
    def visitSceneStmt(self, stmt: Scene):
        # print("Interpreting Scene")
        scene = VNScene(stmt.body, self.env)
        self.env.define(stmt.name.lexeme, scene)

    # Image statement visitor function. Determines whether to show or hide
    # the given image and rerenders the UI.
    def visitImageStmt(self, stmt: Image):
        # print("Interpreting Image")
        self.checkGraphic(stmt.action, "Cannot Use Image In Non-Graphic Mode")
        if stmt.action == Type.SHOW:
            path = self.evaluate(stmt.path)
            if not isinstance(path, str):
                raise RuntimeErr(stmt.tok, "Image Path Must Be A String")
            self.game.showImage(self.resolvePath(path, stmt.tok))
        elif stmt.action == Type.HIDE:
            path = self.evaluate(stmt.path)
            if not isinstance(path, str):
                raise RuntimeErr(stmt.tok, "Image Path Must Be A String")
            self.game.hideImage(self.resolvePath(path, stmt.tok))
        self.game.render()

    # Display statement visitor function. Displays the given value and rerenders.
    def visitDisplayStmt(self, stmt: Display):
        # print("Interpreting Display")
        message = self.evaluate(stmt.value)
        if not isinstance(message, str):
            raise RuntimeErr(stmt.tok, "Display Message Must Be A String")
        self.game.display(message)
        self.game.render()

    # Options statement visitor function. Pops (displays) the options (all cases).
    def visitOptionsStmt(self, stmt: Options):
        # print("Interpreting Options")
        cases = []
        for case in stmt.cases:
            text = self.evaluate(case[0])
            if not isinstance(text, str):
                raise RuntimeErr(stmt.tok, "Options Text Must Be A String")
            cases.append((self.evaluate(case[0]), case[1]))
        choice = self.game.popOptions(cases)
        choice.accept(self)

    # Audio statement visitor function. Determines whether to start
    # or stop the given audio.
    def visitAudioStmt(self, stmt: Audio):
        # print("Interpreting Audio")
        self.checkGraphic(stmt.action, "Cannot Use Audio In Non-Graphic Mode")
        if stmt.action == Type.START:
            path = self.evaluate(stmt.path)
            if not isinstance(path, str):
                raise RuntimeErr(stmt.tok, "Audio Path Must Be A String")
            self.game.startAudio(self.resolvePath(path, stmt.tok))
        elif stmt.action == Type.STOP:
            self.game.stopAudio()

    # Delay statement visitor function. Delays the given amount of time.
    def visitDelayStmt(self, stmt: Delay):
        # print("Interpreting Delay")
        value = self.evaluate(stmt.value)
        if not isinstance(value, float):
            raise RuntimeErr(stmt.tok, "Delay Value Must Be Number")
        self.game.delay(value)

    # Jump statement visitor function. Gets the destination and raises
    # a JumpErr to signal that it needs to "jump" to the given scene.
    def visitJumpStmt(self, stmt: Jump):
        # print("Interpreting Jump")
        scene = self.env.get(stmt.dest)
        if not isinstance(scene, VNScene):
            raise RuntimeErr(stmt.dest, "Jump Destination Must Be Scene")
        raise JumpErr(scene)

    # Exit statement visitor function. Exits the game.
    def visitExitStmt(self, stmt: Exit):
        # print("Interpreting Exit")
        sys.exit(0)

    # Set statement visitor function. Evaluates the initializer
    # then defines the variable given name and value.
    def visitSetStmt(self, stmt: Set):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.env.define(stmt.name.lexeme, value)
        return None

    # Block statement visitor function. Executes a block of statements.
    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statements, Env(self.env))
        return None

    # Expression statement visitor function. Evaluates the given expression.
    def visitExpressionStmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    # Function statement visitor function. Creates a new VNFunction and
    # defines it given the name and associated function.
    def visitFunStmt(self, stmt: Fun):
        function = VNFunction(stmt, self.env)
        self.env.define(stmt.name.lexeme, function)
        return None

    # If statement visitor function. Evaluates whether the condition
    # statement is true or false and executes the correct branch accordingly.
    def visitIfStmt(self, stmt: If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    # Print statement visitor function. Evaluates the given expression
    # then prints the string version of it.
    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    # Return statement visitor function. Evaluates the return value
    # then returns it through raising a ReturnErr.
    def visitReturnStmt(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnErr(value)

    # While statement visitor function. Creates a loop of evaluating
    # the condition statement and executes the body while it is true.
    def visitWhileStmt(self, stmt: While):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    # Assign expression visitor function. Evaluates the expression value
    # and either reassigns the value (if the name already exists) or
    # creates a new token with given name and value.
    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)
        if expr in self.locals:
            self.env.assign(self.locals.get(expr), expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    # Binary expression visitor function. 
    def visitBinaryExpr(self, expr: Binary):
        # Evaluates both left and right expressions and gets the expression type.
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        exprType = expr.oper.type

        # Checks what the type is and compares the two expressions accordingly.
        if exprType == Type.BANG_EQUAL:
            return not self.isEqual(left, right)
        if exprType == Type.EQUAL_EQUAL:
            return self.isEqual(left, right)
        if exprType == Type.GREATER:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) > float(right)
        if exprType == Type.GREATER_EQUAL:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) >= float(right)
        if exprType == Type.LESS:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) < float(right)
        if exprType == Type.LESS_EQUAL:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) <= float(right)
        if exprType == Type.MINUS:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) - float(right)
        if exprType == Type.PLUS:
            if left is not None and isinstance(left, float) and right is not None and isinstance(right, float):
                return float(left) + float(right)
            if left is not None and isinstance(left, str) and right is not None and isinstance(right, str):
                return str(left) + str(right)
        if exprType == Type.SLASH:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) / float(right)
        if exprType == Type.STAR:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) * float(right)
        return None

    # Call expression visitor statement. Evaluates the callee and args given
    # and calls the function if it exists and has the right number of arguments.
    def visitCallExpr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.args:
            arguments.append(self.evaluate(argument))
        if callee is None or not isinstance(callee, VNCallable):
            raise RuntimeErr(expr.paren, "Can Only Call Functions")
        function: VNCallable = callee
        if len(arguments) != function.arity():
            raise RuntimeErr(expr.paren, "Expected " + function.arity() + " Arguments But Got " + len(arguments))
        return function.call(self, arguments)

    # Grouping expression visitor function. Evaluates the given expression.
    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    # Literal expression visitor function. Returns the value of the expression.
    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    # Logical expression visitor function. Checks whether it is an
    # "or" or "and" statement and evaluates the logical expression accordingly.
    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.oper.type == Type.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(expr.right)

    # Unary expression visitor function. Evaluates the expression based
    # on whether it is followed by ! or - and returns the result.
    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        exprType = expr.oper.type
        if exprType == Type.BANG:
            return not self.isTruthy(right)
        if exprType == Type.MINUS:
            self.checkNumberOperand(expr.oper, right)
            return -float(right)
        return None
    
    # Variable expression visitor function. Looks up whether the variable
    # exists and returns the result.
    def visitVariableExpr(self, expr: Set):
        return self.lookUpVariable(expr.name, expr)

    # Helper functions

    # Looks up the variable in the local and global dicts, returning
    # the resulting value.
    def lookUpVariable(self, name: Token, expr: Expr):
        if expr in self.locals:
            return self.env.get(name.lexeme)
        else:
            return self.globals.get(name)
    
    # Checks that the operand is a float type. Throws if otherwise.
    def checkNumberOperand(self, oper: Token, operand: Any):
        if operand is not None and isinstance(operand, float):
            return
        raise RuntimeErr(oper, "Operand Must Be A Number")

    # Checks if both arguments are floats. Throws if not.
    def checkNumberOperands(self, oper: Token, left: Any, right: Any):
        if left is not None and isinstance(left, float) and right is not None and isinstance(right, float):
            return
        raise RuntimeErr(oper, "Operands Must Be Numbers")

    # Checks if the object is a truthy value. If so, return the 
    # literall bool value. Otherwise, return true.
    def isTruthy(self, obj: Any):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True
    
    # Checks if two objects are equal to each other.
    def isEqual(self, a: Any, b: Any):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    # Stringifies the given object.
    def stringify(self, obj: Any):
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:len(text) - 2]
            return text
        return str(obj)