from abc import ABC, abstractmethod
from typing import Any

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
    def visitLiteralExpr(self, stmt: Expr):
        pass

class Assign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitAssignExpr(self)
    
class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitLiteralExpr(self)