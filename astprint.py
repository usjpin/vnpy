
from expr import *
from stmt import *

class ASTPrinter(ExprVisitor, StmtVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)
    def print(self, stmt: Stmt):
        return stmt.accept(self)
    
    def visitAssignExpr(self, expr: Assign):
        pass

    def visitExpressionStmt(self, stmt: Expression):
        pass