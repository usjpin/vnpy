
from sympy import GreaterThan
from expr import *
from stmt import *

def to_ascii(path):
    img = Image.open(path)
    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    chars = ["B","S","#","&","@","$","%","*","!",":","."]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image

class ASTPrinter(StmtVisitor, ExprVisitor):
    tabs = 0

    def print(self, stmt: Stmt) -> str:
        return stmt.accept(self)
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def indent(self) -> str:
        return "  " * self.tabs

    def visitExpressionStmt(self, stmt: Expression) -> str:
        ret = self.indent() + "(; "
        ret += self.print(stmt.expression)
        ret += ")"
        return ret

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

    def visitOptionsStmt(self, stmt: Options) -> str:
        ret = self.indent()
        ret += "(options "
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

    def visitDelayStmt(self, stmt: Delay) -> str:
        ret = self.indent() 
        ret += "(delay " + stmt.value.lexeme + ")"
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
    
    def visitBlockStmt(self, stmt: Block) -> str:
        ret = self.indent() + "(block"
        self.tabs += 1
        for statement in stmt.statements:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret

    def visitFunStmt(self, stmt: Fun) -> str:
        ret = self.indent() + "(fun " + stmt.name.lexeme + "("
        for param in stmt.args:
            if param != stmt.args[0]:
                ret += " "
        ret += ") "
        self.tabs += 1
        for statement in stmt.body:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret

    def visitIfStmt(self, stmt: If) -> str:
        ret = self.indent() + "(if "
        ret += self.print(stmt.condition)
        self.tabs += 1
        ret += "\n"
        ret += self.print(stmt.thenBranch)
        if stmt.elseBranch is not None:
            ret += "\n"
            ret += self.print(stmt.elseBranch)
        self.tabs -= 1 
        ret += "\n" + self.indent() + ")"
        return ret

    def visitPrintStmt(self, stmt: Print) -> str:
        ret = self.indent() + "(print "
        ret += self.print(stmt.expression)
        ret += ")"
        return ret

    def visitReturnStmt(self, stmt: Return) -> str:
        ret = self.indent() + "(return "
        ret += self.print(stmt.value)
        ret += ")"
        return ret

    def visitSetStmt(self, stmt: Set) -> str:
        ret = self.indent() + "(var " + stmt.name.lexeme
        if stmt.initializer is not None:
            ret += " = " + self.print(stmt.initializer)
        ret += ")"
        return ret

    def visitWhileStmt(self, stmt: While) ->str:
        ret = self.indent() + "(while "
        ret += self.print(stmt.condition)
        self.tabs += 1
        ret += "\n"
        ret += self.print(stmt.body)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret
    
    def visitAssignExpr(self, expr: Assign) -> str:
        ret = "(= " + expr.name.lexeme + " "
        ret += self.print(expr.value) + ")"
        return ret

    def visitBinaryExpr(self, expr: Binary) -> str:
        ret = "("
        ret += expr.oper.lexeme + " "
        ret += self.print(expr.left) + " "
        ret += self.print(expr.right) + ")"
        return ret

    def visitCallExpr(self, expr: Call) -> str:
        ret = "(call "
        ret += self.print(expr.callee)
        for arg in expr.args:
            ret += " " + self.print(arg)
        ret += ")"
        return ret

    def visitGroupingExpr(self, expr: Grouping) -> str:
        ret = "(group "
        ret += self.print(expr.expression)
        ret += ")"
        return ret

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return "\'" + str(expr.value) + "\'"

    def visitLogicalExpr(self, expr: Logical) -> str:
        ret = "(" + expr.oper.lexeme + " "
        ret += self.print(expr.left) + " "
        ret += self.print(expr.right) + ")"
        return ret
    
    def visitUnaryExpr(self, expr: Unary) -> str:
        ret = "(" + expr.oper.lexeme + " "
        ret += self.print(expr.right) + ")"
        return ret

    def visitVariableExpr(self, expr: Variable) -> str:
        return expr.name.lexeme