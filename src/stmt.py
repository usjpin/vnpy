from abc import ABC, abstractmethod
from typing import List, Tuple

from tok import Token, Type
from expr import Expr

# Implementation of the visitor pattern. Each type has an
# associate "accept" method, and each visitor has a "visit" method.
# This allows for dynamic dispatch of each type.
class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor'):
        pass

# All visitor expressions for each type of statement
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

# Each of the following class definitions contains a
# constructor and an accept statement.

# Config Stmt has a config and value
class Config(Stmt):
    # Config Stmt constructor
    def __init__(self, config: Type, value: Token) -> None:
        self.config = config
        self.value = value
    # Config Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitConfigStmt(self)

# Scene Stmt has a name and body of statements
class Scene(Stmt):
    # Scene Stmt constructor
    def __init__(self, name: Token, body: List[Stmt]) -> None:
        self.name = name
        self.body = body
    # Scene Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitSceneStmt(self)

# Image Stmt has an action, path, and token
class Image(Stmt):
    # Image Stmt constructor
    def __init__(self, action: Type, path: Expr, tok: Token) -> None:
        self.action = action
        self.path = path
        self.tok = tok
    # Image Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitImageStmt(self)

# Display Stmt has a value and token
class Display(Stmt):
    # Display Stmt constructor
    def __init__(self, value: Expr, tok: Token) -> None:
        self.value = value
        self.tok = tok
    # Display Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitDisplayStmt(self)

# Options Stmt has a list of cases and a token
class Options(Stmt):
    # Options Stmt constructor
    def __init__(self, cases: List[Tuple[Expr, Stmt]], tok: Token) -> None:
        self.cases = cases
        self.tok = tok
    # Options Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitOptionsStmt(self)

# Audio Stmt has an action, path, and token
class Audio(Stmt):
    # Audio Stmt constructor
    def __init__(self, action: Type, path: Expr, tok: Token) -> None:
        self.action = action
        self.path = path
        self.tok = tok
    # Audio Stmt visitor function
    def accept(self, visitor: StmtVisitor):
        return visitor.visitAudioStmt(self)
    
# Delay Stmt has a value and token
class Delay(Stmt):
    # Delay Stmt constructor
    def __init__(self, value: Expr, tok: Token) -> None:
        self.value = value
        self.tok = tok
    # Delay Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitDelayStmt(self)

# Jump Stmt has a destination
class Jump(Stmt):
    # Jump Stmt constructor
    def __init__(self, dest: Token):
        self.dest = dest
    # Jump Stmt visitor function
    def accept(self, visitor: StmtVisitor):
        return visitor.visitJumpStmt(self)

# Exit Stmt has nothing
class Exit(Stmt):
    # Exit Stmt constructor
    def __init__(self):
        pass
    # Exit Stmt visitor function
    def accept(self, visitor: StmtVisitor):
        return visitor.visitExitStmt(self)

# Set Stmt has a name and initializer
class Set(Stmt):
    # Set Stmt constructor
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer
    # Set Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitSetStmt(self)

# Block Stmt has a list of statements
class Block(Stmt):
    # Block Stmt constructor
    def __init__(self, statements: List[Stmt]) -> None:
        self.statements = statements
    # Block Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitBlockStmt(self)

# Expression Stmt has an expression
class Expression(Stmt):
    # Expression Stmt constructor
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    # Expression Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitExpressionStmt(self)

# Fun Stmt has a name, list of arguments, and list of body statements
class Fun(Stmt):
    # Fun Stmt constructor
    def __init__(self, name: Token, args: List[Token], body: List[Stmt]) -> None:
        self.name = name
        self.args = args
        self.body = body
    # Fun Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitFunStmt(self)

# If Stmt has a condition, thenBranch, and elseBranch
class If(Stmt):
    # If Stmt constructor
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt) -> None:
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    # If Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitIfStmt(self)

# Print Stmt has an expression
class Print(Stmt):
    # Print Stmt constructor
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    # Print Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitPrintStmt(self)

# Return Stmt has a keyword and a value
class Return(Stmt):
    # Return Stmt constructor
    def __init__(self, keyword: Token, value: Expr) -> None:
        self.keyword = keyword
        self.value = value
    # Return Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitReturnStmt(self)

# While Stmt has a condition and body
class While(Stmt):
    # While Stmt constructor
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body
    # While Stmt visitor function
    def accept(self, visitor: StmtVisitor) -> None:
        return visitor.visitWhileStmt(self)