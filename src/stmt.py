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
    @abstractmethod
    def visitShowStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitWaitStmt(self, stmt: Stmt):
        pass

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)

class Show(Stmt):
    def __init__(self, path: str) -> None:
        self.path = path
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitShowStmt(self)
    
class Wait(Stmt):
    def __init__(self, number: float) -> None:
        self.number = number
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitWaitStmt(self)