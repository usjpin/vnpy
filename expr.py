from abc import ABC, abstractmethod

from token import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor'):
        pass

class ExprVisitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, stmt: Expr):
        pass

class Assign(Expr):
    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value
    def accept(self, visitor: ExprVisitor) -> None:
        return visitor.visitAssignExpr(self)