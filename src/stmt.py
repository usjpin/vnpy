from abc import ABC, abstractmethod
from typing import List, Tuple

from tok import Token, Type
from expr import Expr

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor'):
        pass

class StmtVisitor(ABC):
    @abstractmethod
    def visitConfigStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitSceneStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitImageStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitDisplayStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitOptionStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitAudioStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitWaitStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitJumpStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitExitStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitExpressionStmt(self, stmt: Stmt):
        pass

class Config(Stmt):
    def __init__(self, config: Type, value: Token) -> None:
        self.config = config
        self.value = value
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitConfigStmt(self)

class Scene(Stmt):
    def __init__(self, name: Token, body: List[Stmt]) -> None:
        self.name = name
        self.body = body
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitSceneStmt(self)

class Image(Stmt):
    def __init__(self, action: Type, path: Token) -> None:
        self.action = action
        self.path = path
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitImageStmt(self)

class Display(Stmt):
    def __init__(self, value: Token) -> None:
        self.value = value
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitDisplayStmt(self)

class Option(Stmt):
    def __init__(self, cases: List[Tuple[Token, Stmt]]) -> None:
        self.cases = cases
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitOptionStmt(self)

class Audio(Stmt):
    def __init__(self, action: Type, path: Token) -> None:
        self.action = action
        self.path = path
    def accept(self, visitor: StmtVisitor):
        return visitor.visitAudioStmt(self)
    
class Wait(Stmt):
    def __init__(self, action: Type, value: Token) -> None:
        self.action = action
        self.value = value
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitWaitStmt(self)

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

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)