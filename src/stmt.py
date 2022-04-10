from abc import ABC, abstractmethod
from typing import List

from tok import Token
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
    @abstractmethod
    def visitSceneStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitOptionStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitJumpStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitExitStmt(self, stmt: Stmt):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)

class Show(Stmt):
    def __init__(self, path: Expr) -> None:
        self.path = path
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitShowStmt(self)
    
class Wait(Stmt):
    def __init__(self, number: Expr) -> None:
        self.number = number
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitWaitStmt(self)

class Scene(Stmt):
    def __init__(self, name: Token, body: List[Stmt]) -> None:
        self.name = name
        self.body = body
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitSceneStmt(self)

class Option(Stmt):
    def __init__(self, message: Expr, action: Stmt):
        self.message = message
        self.action = action
    def accept(self, visitor: StmtVisitor):
        return visitor.visitOptionStmt(self)

class Jump(Stmt):
    def __init__(self, dest: Token):
        self.dest = dest
    def accept(self, visitor: StmtVisitor):
        return visitor.visitJumpStmt(self)

class Exit(Stmt):
    def __init__(self):
        pass
    def accept(self, visitor: StmtVisitor):
        return visitor.visitExitStmt(self)