
from expr import *
from stmt import *

# AstPrinter visits both Expr and Stmt types and returns a string.
class ASTPrinter(StmtVisitor, ExprVisitor):
    tabs = 0

    # When calling print on each Expr or Stmt, pass the AstPrinter visitor object.
    def print(self, stmt: Stmt) -> str:
        return stmt.accept(self)
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    # Indent a number of tabs.
    def indent(self) -> str:
        return "  " * self.tabs

    # Visitor for the expression statement. Returns a string
    # representing the expression statement.
    def visitExpressionStmt(self, stmt: Expression) -> str:
        ret = self.indent() + "(; "
        ret += self.print(stmt.expression)
        ret += ")"
        return ret

    # Visitor for the config statement. Returns a string
    # representing the config statement.
    def visitConfigStmt(self, stmt: Config) -> str:
        ret = self.indent()
        ret += "(config " + stmt.config.value
        ret += " " + stmt.value.lexeme + ")"
        return ret

    # Visitor for the image statement. Returns a string
    # representing the image statement.
    def visitImageStmt(self, stmt: Image) -> str:
        ret = self.indent()
        ret += "(image " + stmt.action.value
        ret += " " + self.print(stmt.path) + ")"
        return ret

    # Visitor for the display statement. Returns a string
    # representing the display statement.
    def visitDisplayStmt(self, stmt: Display) -> str:
        ret = self.indent() 
        ret += "(display " + self.print(stmt.value) + ")"
        return ret

    # Visitor for the options statement. Returns a string
    # representing the options statement.
    def visitOptionsStmt(self, stmt: Options) -> str:
        ret = self.indent()
        ret += "(options "
        self.tabs += 1
        # Iterate through all possible cases for the options
        for case in stmt.cases:
            ret += "\n" + self.indent()
            ret += "(case " + self.print(case[0])
            ret += " do\n" + self.indent() + self.print(case[1])
            ret += "\n" + self.indent() + ")"
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret
    
    # Visitor for the audio statement. Returns a string
    # representing the audio statement.
    def visitAudioStmt(self, stmt: Audio) -> str:
        ret = self.indent()
        ret += "(audio " + stmt.action.value
        ret += " " + self.print(stmt.path) + ")"
        return ret

    # Visitor for the delay statement. Returns a string
    # representing the delay statement.
    def visitDelayStmt(self, stmt: Delay) -> str:
        ret = self.indent() 
        ret += "(delay " + self.print(stmt.value) + ")"
        return ret

    # Visitor for the scene statement. Returns a string
    # representing the scene statement.
    def visitSceneStmt(self, stmt: Scene) -> str:
        ret = self.indent()
        ret += "(scene " + stmt.name.lexeme
        self.tabs += 1
        # Iterate and print all statements in the scene body
        for statement in stmt.body:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n)"
        return ret
    
    # Visitor for the jump statement. Returns a string
    # representing the jump statement.
    def visitJumpStmt(self, stmt: Jump) -> str:
        ret = self.indent()
        ret += "(jump " + stmt.dest.lexeme + ")"
        return ret
    
    # Visitor for the exit statement. Returns a string
    # representing the exit statement.
    def visitExitStmt(self, stmt: Exit) -> str:
        return self.indent() + "(exit)"
    
    # Visitor for the block statement. Returns a string
    # representing the block statement.
    def visitBlockStmt(self, stmt: Block) -> str:
        ret = self.indent() + "(block"
        self.tabs += 1
        # Pass the AstVisitor to each Stmt
        for statement in stmt.statements:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret

    # Visitor for the function statement. Returns a string
    # representing the function statement.
    def visitFunStmt(self, stmt: Fun) -> str:
        ret = self.indent() + "(fun " + stmt.name.lexeme + "("
        # Append each argument to the string
        for param in stmt.args:
            if param != stmt.args[0]:
                ret += " "
        ret += ") "
        self.tabs += 1
        # Append each body statement to the string
        for statement in stmt.body:
            ret += "\n" + self.print(statement)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret

    # Visitor for the if statement. Returns a string
    # representing the if statement.
    def visitIfStmt(self, stmt: If) -> str:
        ret = self.indent() + "(if "
        ret += self.print(stmt.condition)
        self.tabs += 1
        ret += "\n"
        ret += self.print(stmt.thenBranch)
        # Add else branch if it exists
        if stmt.elseBranch is not None:
            ret += "\n"
            ret += self.print(stmt.elseBranch)
        self.tabs -= 1 
        ret += "\n" + self.indent() + ")"
        return ret

    # Visitor for the print statement. Returns a string
    # representing the print statement.
    def visitPrintStmt(self, stmt: Print) -> str:
        ret = self.indent() + "(print "
        ret += self.print(stmt.expression)
        ret += ")"
        return ret

    # Visitor for the return statement. Returns a string
    # representing the return statement.
    def visitReturnStmt(self, stmt: Return) -> str:
        ret = self.indent() + "(return "
        ret += self.print(stmt.value)
        ret += ")"
        return ret

    # Visitor for the set statement. Returns a string
    # representing the set statement.
    def visitSetStmt(self, stmt: Set) -> str:
        ret = self.indent() + "(var " + stmt.name.lexeme
        # Add the initializer if it exists
        if stmt.initializer is not None:
            ret += " = " + self.print(stmt.initializer)
        ret += ")"
        return ret

    # Visitor for the while statement. Returns a string
    # representing the while statement.
    def visitWhileStmt(self, stmt: While) ->str:
        ret = self.indent() + "(while "
        # Add the conditional statement and body statements
        ret += self.print(stmt.condition)
        self.tabs += 1
        ret += "\n"
        ret += self.print(stmt.body)
        self.tabs -= 1
        ret += "\n" + self.indent() + ")"
        return ret
    
    # Visitor for the assign expression. Returns a string
    # representing the assign expression.
    def visitAssignExpr(self, expr: Assign) -> str:
        ret = "(= " + expr.name.lexeme + " "
        ret += self.print(expr.value) + ")"
        return ret

    # Visitor for the binary expression. Returns a string
    # representing the binary expression.
    def visitBinaryExpr(self, expr: Binary) -> str:
        ret = "("
        ret += expr.oper.lexeme + " "
        ret += self.print(expr.left) + " "
        ret += self.print(expr.right) + ")"
        return ret

    # Visitor for the call expression. Returns a string
    # representing the call expression.
    def visitCallExpr(self, expr: Call) -> str:
        ret = "(call "
        ret += self.print(expr.callee)
        for arg in expr.args:
            ret += " " + self.print(arg)
        ret += ")"
        return ret

    # Visitor for the grouping expression. Returns a string
    # representing the grouping expression.
    def visitGroupingExpr(self, expr: Grouping) -> str:
        ret = "(group "
        ret += self.print(expr.expression)
        ret += ")"
        return ret

    # Visitor for the literal expression. Returns a string
    # representing the literal expression.
    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return "\'" + str(expr.value) + "\'"

    # Visitor for the logical expression. Returns a string
    # representing the logical expression.
    def visitLogicalExpr(self, expr: Logical) -> str:
        ret = "(" + expr.oper.lexeme + " "
        ret += self.print(expr.left) + " "
        ret += self.print(expr.right) + ")"
        return ret
    
    # Visitor for the unary expression. Returns a string
    # representing the unary expression.
    def visitUnaryExpr(self, expr: Unary) -> str:
        ret = "(" + expr.oper.lexeme + " "
        ret += self.print(expr.right) + ")"
        return ret

    # Visitor for the variable expression. Returns a string
    # representing the variable expression.
    def visitVariableExpr(self, expr: Variable) -> str:
        return expr.name.lexeme