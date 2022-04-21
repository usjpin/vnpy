import os
import sys
from typing import List

from expr import *
from stmt import *
from game import *
from env import Env
from call import *
from err import *

class Interpreter(ExprVisitor, StmtVisitor):

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
        # self.globals.define("readClick", VNClickCallable())
        # self.globals.define("readKey", VNClickCallable())

    def interpret(self, configs: List[Config], statements: List[Stmt]) -> None:
        # Error Handling
        try:
            for statement in configs:
                self.execute(statement)
        except RuntimeErr as e:
            e.printErr()
        if self.config["mode"] == "graphic":
            self.game = VNGUIGame(
                self.config["width"],
                self.config["height"],
                self.config["volume"]
            )
        else:
            self.game = VNConsoleGame()
        while statements is not None:
            current = statements
            statements = None
            try:
                for statement in current:
                    self.execute(statement)
            except JumpErr as j:
                self.env = j.scene.env
                statements = j.scene.body
            except ReturnErr as r:
                self.value = r.value
            except RuntimeErr as e:
                e.printErr()
        
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def executeBlock(self, statements: List[Stmt], environment: Env):
        previous = self.env
        try:
            self.env = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous

    def resolvePath(self, path: Token) -> str:
        if not os.path.exists(path.literal):
            raise RuntimeErr(path, "Path \'" + path.literal + "\' Does Not Exist")
        return path.literal

    def visitConfigStmt(self, stmt: Config):
        print("Interpreting Config")
        self.config[stmt.config.value] = stmt.value.literal

    def visitSceneStmt(self, stmt: Scene):
        print("Interpreting Scene")
        scene = VNScene(stmt.body, self.env)
        self.env.define(stmt.name.lexeme, scene)

    def visitImageStmt(self, stmt: Image):
        print("Interpreting Image")
        if self.config["mode"] == "console":
            raise RuntimeErr(stmt.action, "Cannot Use Image In Console Mode")
        if stmt.action == Type.SHOW:
            self.game.showImage(self.resolvePath(stmt.path))
        elif stmt.action == Type.HIDE:
            self.game.hideImage(self.resolvePath(stmt.path))
        self.game.render()

    def visitDisplayStmt(self, stmt: Display):
        print("Interpreting Display")
        self.game.display(stmt.value.literal)
        self.game.render()

    def visitOptionsStmt(self, stmt: Options):
        print("Interpreting Options")
        choice = self.game.popOptions(stmt.cases)
        choice.accept(self)

    def visitAudioStmt(self, stmt: Audio):
        print("Interpreting Audio")
        if self.config["mode"] == "console":
            raise RuntimeErr(stmt.action, "Cannot Use Audio In Console Mode")
        if stmt.action == Type.START:
            self.game.startAudio(self.resolvePath(stmt.path))
        elif stmt.action == Type.STOP:
            self.game.stopAudio()

    def visitDelayStmt(self, stmt: Delay):
        print("Interpreting Delay")
        self.game.delay(stmt.value.literal)

    def visitJumpStmt(self, stmt: Jump):
        print("Interpreting Jump")
        scene = self.env.get(stmt.dest.lexeme)
        if not isinstance(scene, VNScene):
            raise RuntimeErr(stmt.dest, "Jump Destination Must Be Scene")
        raise JumpErr(scene)

    def visitExitStmt(self, stmt: Exit):
        print("Interpreting Exit")
        sys.exit(0)

    def visitSetStmt(self, stmt: Set):
        value = None
        if stmt.value != None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statements, Env(self.env))
        return None

    def visitExpressionStmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    def visitFunStmt(self, stmt: Fun):
        pass #TODO implement

    def visitIfStmt(self, stmt: If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch != None:
            self.execute(stmt.elseBranch)
        return None

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitReturnStmt(self, stmt: Return):
        value = None
        if stmt.value != None:
            value = self.evaluate(stmt.value)
        raise Return(value)

    def visitWhileStmt(self, stmt: While):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)
        if expr in self.locals:
            self.env.assign(self.locals.get(expr), expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        exprType = expr.oper.type
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
            if left != None and isinstance(left, float) and right != None and isinstance(right, float):
                return float(left) + float(right)
            if left != None and isinstance(left, str) and right != None and isinstance(right, str):
                return str(left) + str(right)
        if exprType == Type.SLASH:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) / float(right)
        if exprType == Type.STAR:
            self.checkNumberOperands(expr.oper, left, right)
            return float(left) * float(right)
        return None

    def visitCallExpr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.args:
            arguments.append(self.evaluate(argument))
        if callee == None or not isinstance(callee, VNFunction) and not isinstance(callee, Scene):
            raise RuntimeErr(expr.paren, "Can Only Call Function And Classes.")
        function = VNCallable(callee)
        if arguments.count != function.arity():
            raise RuntimeErr(expr.paren, "Expected " + function.arity() + " Arguments But Got " + arguments.count + ".")
        return function.call(self, arguments)

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.oper.type == Type.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(expr.right)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        exprType = expr.oper.type
        if exprType == Type.BANG:
            return not self.isTruthy(right)
        if exprType == Type.MINUS:
            self.checkNumberOperand(expr.oper, right)
        return None
    
    def visitVariableExpr(self, expr: Set):
        return self.lookUpVariable(expr.name, expr)

    def lookUpVariable(self, name: Token, expr: Expr):
        if expr in self.locals:
            return self.env.get(self.locals.get(expr), name.lexeme)
        else:
            return self.globals.get(name)
    
    def checkNumberOperand(self, oper: Token, operand: Any):
        if operand != None and isinstance(operand, float):
            return
        raise RuntimeErr(oper, "Operand Must Be A Number.")

    def checkNumberOperands(self, oper: Token, left: Any, right: Any):
        if left != None and isinstance(left, float) and right != None and isinstance(right, float):
            return
        raise RuntimeErr(oper, "Operands Must Be Numbers.")

    def isTruthy(self, obj: Any):
        if obj == None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True
    
    def isEqual(self, a: Any, b: Any):
        if a == None and b == None:
            return True
        if a == None:
            return False
        return a == b

    def stringify(self, obj: Any):
        if obj == None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:len(text) - 2]
            return text
        return str(obj)