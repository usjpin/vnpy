
from expr import *
from stmt import *

class ASTPrinter(StmtVisitor, ExprVisitor):
    def print(self, stmt: Stmt):
        return stmt.accept(self)
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitExpressionStmt(self, stmt: Expression) -> str:
        pass

    def visitShowStmt(self, stmt: Show):
        return "(show " + self.print(stmt.path) + ")"

    def visitWaitStmt(self, stmt: Wait):
        return "(wait " + self.print(stmt.number) + ")"
    
    def visitAssignExpr(self, expr: Assign) -> str:
        pass

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"
        return str(expr.value)