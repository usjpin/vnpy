from abc import ABC, abstractmethod

from expr import Expr

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor'):
        pass

class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt: Stmt):
        pass

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)