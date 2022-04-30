from abc import ABC, abstractmethod
from typing import Any, List

from tok import Token

# Implementation of the visitor pattern. Each type has an associated
# "accept" method, and each visitor has a "visit" method. This allows
# for dynamic dispatch of each type.
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor'):
        pass

# Visit expressions for all types
class ExprVisitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitBinaryExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitCallExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitGroupingExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitLiteralExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitLogicalExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitUnaryExpr(self, expr: Expr):
        pass
    @abstractmethod
    def visitVariableExpr(self, expr: Expr):
        pass

# Each of the following class definitions contains a constructor and
# an Accept statement.

# Assign Expr. Contains a name and a value.
class Assign(Expr):
    # Assign Expr constructor
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value
    # Assign Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitAssignExpr(self)

# Binary Expr. Contains a left, operation, and right.
class Binary(Expr):
    # Binary Expr constructor
    def __init__(self, left: Expr, oper: Token, right: Expr) -> None:
        self.left = left
        self.oper = oper
        self.right = right
    # Binary Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitBinaryExpr(self)

# Call Expr. Contains a callee, parent, and args.
class Call(Expr):
    # Call Expr constructor
    def __init__(self, callee: Expr, paren: Token, args: List[Expr]) -> None:
        self.callee = callee
        self.paren = paren
        self.args = args
    # Call Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitCallExpr(self)

# Grouping Expr. Contains an expression.
class Grouping(Expr):
    # Grouping Expr constructor
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    # Grouping Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitGroupingExpr(self)

# Literal Expr. Contains a value.
class Literal(Expr):
    # Literal Expr constructor
    def __init__(self, value: Any):
        self.value = value
    # Literal Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitLiteralExpr(self)

# Logical Expr. Contains a left, operation, and right.
class Logical(Expr):
    # Logical Expr constructor
    def __init__(self, left: Expr, oper: Token, right: Expr) -> None:
        self.left = left
        self.oper = oper
        self.right = right
    # Logical Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitLogicalExpr(self)

# Unary Expr. Contains an operation and right.
class Unary(Expr):
    # Unary Expr constructor
    def __init__(self, oper: Token, right: Expr) -> None:
        self.oper = oper
        self.right = right
    # Unary Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitUnaryExpr(self)

# Variable Expr. Contains a name.
class Variable(Expr):
    # Variable Expr constructor
    def __init__(self, name: Token):
        self.name = name
    # Variable Expr visitor function
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitVariableExpr(self)