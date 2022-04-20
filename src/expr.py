from abc import ABC, abstractmethod
from typing import Any, List

from tok import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor'):
        pass

class ExprVisitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitBinaryExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitCallExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitGetExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitGroupingExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitLiteralExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitLogicalExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitSetExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitSuperExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitThisExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitUnaryExpr(self, stmt: Expr):
        pass
    @abstractmethod
    def visitVariableExpr(self, stmt: Expr):
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

class Get(Expr):
    def __init__(self, obj: Expr, name: Token) -> None:
        self.obj = obj
        self.name = name
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitGetExpr(self)

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

class Set(Expr):
    def __init__(self, obj: Expr, name: Token, value: Expr) -> None:
        self.obj = obj
        self.name = name
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitSetExpr(self)

class Super(Expr):
    def __init__(self, keyword: Token, method: Token) -> None:
        self.keyword = keyword
        self.method = method
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitSuperExpr(self)

class This(Expr):
    def __init__(self, keyword: Token) -> None:
        self.keyword = keyword
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitThisExpr(self)

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