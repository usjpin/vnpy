
from expr import *
from stmt import *

class ASTPrinter(StmtVisitor, ExprVisitor):
    tabs = 0

    def print(self, stmt: Stmt) -> str:
        return stmt.accept(self)
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def indent(self) -> str:
        return "  " * self.tabs

    def visitExpressionStmt(self, stmt: Expression) -> str:
        pass

    def visitConfigStmt(self, stmt: Config) -> str:
        ret = self.indent()
        ret += "(config " + stmt.config.value
        ret += " " + stmt.value.lexeme + ")"
        return ret

    def visitImageStmt(self, stmt: Image) -> str:
        ret = self.indent()
        ret += "(image " + stmt.action.value
        ret += " " + stmt.path.lexeme + ")"
        return ret

    def visitDisplayStmt(self, stmt: Display) -> str:
        ret = self.indent() 
        ret += "(display " + stmt.value.lexeme + ")"
        return ret

    def visitOptionStmt(self, stmt: Option) -> str:
        ret = self.indent()
        ret += "(option "
        self.tabs += 1
        for case in stmt.cases:
            ret += "\n" + self.indent()
            ret += "(case " + case[0].lexeme
            ret += " do\n" + self.indent() + self.print(case[1])
            ret += "\n" + self.indent() + ")"
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret
    
    def visitAudioStmt(self, stmt: Audio) -> str:
        ret = self.indent()
        ret += "(audio " + stmt.action.value
        ret += " " + stmt.path.lexeme + ")"
        return ret

    def visitWaitStmt(self, stmt: Wait) -> str:
        ret = self.indent() 
        ret += "(wait " + stmt.action.value
        if stmt.value is not None:
            ret += " " + stmt.value.lexeme
        ret += ")"
        return ret

    def visitSceneStmt(self, stmt: Scene) -> str:
        ret = self.indent()
        ret += "(scene " + stmt.name.lexeme
        self.tabs += 1
        for statement in stmt.body:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n)"
        return ret
    
    def visitJumpStmt(self, stmt: Jump) -> str:
        ret = self.indent()
        ret += "(jump " + stmt.dest.lexeme + ")"
        return ret
    
    def visitExitStmt(self, stmt: Exit) -> str:
        return self.indent() + "(exit)"
    
    def visitAssignExpr(self, expr: Assign) -> str:
        pass

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"
        return "\'" + str(expr.value) + "\'"