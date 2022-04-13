
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
    
    def visitAssignExpr(self, expr: Assign) -> str:
        pass

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"
        return "\'" + str(expr.value) + "\'"