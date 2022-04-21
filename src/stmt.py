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
    def visitOptionsStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitAudioStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitDelayStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitJumpStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitExitStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitBlockStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitExpressionStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitFunStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitIfStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitPrintStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitReturnStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitSetStmt(self, stmt: Stmt):
        pass
    @abstractmethod
    def visitWhileStmt(self, stmt: Stmt):
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

class Options(Stmt):
    def __init__(self, cases: List[Tuple[Token, Stmt]]) -> None:
        self.cases = cases
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitOptionsStmt(self)

class Audio(Stmt):
    def __init__(self, action: Type, path: Token) -> None:
        self.action = action
        self.path = path
    def accept(self, visitor: StmtVisitor):
        return visitor.visitAudioStmt(self)
    
class Delay(Stmt):
    def __init__(self, value: Token) -> None:
        self.value = value
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitDelayStmt(self)

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

class Set(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitSetStmt(self)

class Block(Stmt):
    def __init__(self, statements: List[Stmt]) -> None:
        self.statements = statements
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitBlockStmt(self)

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)

class Fun(Stmt):
    def __init__(self, name: Token, args: List[Token], body: List[Stmt]) -> None:
        self.name = name
        self.args = args
        self.body = body
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitFunStmt(self)

class If(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt) -> None:
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitIfStmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitPrintStmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr) -> None:
        self.keyword = keyword
        self.value = value
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitReturnStmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitWhileStmt(self)