import sys
from typing import List

from expr import *
from stmt import *
from game import *
from runerr import RuntimeErr
from env import Env

class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):
        self.globals = Env()
        self.env = globals
        self.locals = {}
        self.game = VNGUIGame(500, 500)

    def interpret(self, statements: List[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeErr as e:
            pass
    
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitExpressionStmt(self, stmt: Expression):
        pass

    def visitDisplayStmt(self, stmt: Display):
        #print("Interpreting Display")
        self.game.display(self.evaluate(stmt.path))

    def visitWaitStmt(self, stmt: Wait):
        #print("Interpreting Wait")
        self.game.wait(self.evaluate(stmt.number))

    def visitSceneStmt(self, stmt: Scene):
        pass

    def visitOptionsStmt(self, stmt: Options):
        pass

    def visitJumpStmt(self, stmt: Jump):
        pass

    def visitExitStmt(self, stmt: Exit):
        sys.exit(0)

    def visitAssignExpr(self, expr: Assign):
        pass

    def visitLiteralExpr(self, expr: Literal):
        return expr.value
