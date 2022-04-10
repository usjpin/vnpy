from typing import List

from sympy import evaluate

from expr import *
from game import Game
from runerr import RuntimeErr
from stmt import *
from env import Env

class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):
        self.globals = Env()
        self.env = globals
        self.locals = {}
        self.game = Game(500, 500)

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

    def visitShowStmt(self, stmt: Show):
        #print("Interpreting Show")
        self.game.show(self.evaluate(stmt.path))

    def visitWaitStmt(self, stmt: Wait):
        #print("Interpreting Wait")
        self.game.wait(self.evaluate(stmt.number))

    def visitAssignExpr(self, expr: Assign):
        pass

    def visitLiteralExpr(self, expr: Literal):
        return expr.value
