from abc import ABC, abstractmethod
from typing import Any, List

from tok import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor'):
        pass

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

class Assign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitAssignExpr(self)

class Binary(Expr):
    def __init__(self, left: Expr, oper: Token, right: Expr) -> None:
        self.left = left
        self.oper = oper
        self.right = right
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitBinaryExpr(self)

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, args: List[Expr]) -> None:
        self.callee = callee
        self.paren = paren
        self.args = args
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitCallExpr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitLiteralExpr(self)

class Logical(Expr):
    def __init__(self, left: Expr, oper: Token, right: Expr) -> None:
        self.left = left
        self.oper = oper
        self.right = right
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitLogicalExpr(self)

class Unary(Expr):
    def __init__(self, oper: Token, right: Expr) -> None:
        self.oper = oper
        self.right = right
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitUnaryExpr(self)

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitVariableExpr(self)