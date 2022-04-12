import sys
from typing import List

from expr import *
from stmt import *
from game import *
from env import Env
from call import *
from err import *

class Interpreter(ExprVisitor, StmtVisitor):

    def __init__(self):
        self.globals = Env()
        self.env = self.globals
        self.current = 0
        self.locals = {}
        self.config = {
            'width': 500,
            'height': 500,
            'mode': 'graphic'
        }

    def interpret(self, configs: List[Config], statements: List[Stmt]) -> None:
        # Error Handling
        try:
            for statement in configs:
                self.execute(statement)
            if self.config["mode"] == "graphic":
                self.game = VNGUIGame(self.config["width"], self.config["height"])
            else:
                self.game = VNConsoleGame()
            for statement in statements:
                self.execute(statement)
        except RuntimeErr as e:
            pass
        
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitConfigStmt(self, stmt: Config):
        self.config[stmt.config.value] = stmt.value.literal

    def visitSceneStmt(self, stmt: Scene):
        scene = VNScene(stmt.body, self.env)
        self.env.define(stmt.name.lexeme, scene)

    def visitImageStmt(self, stmt: Image):
        pass

    def visitDisplayStmt(self, stmt: Display):
        #print("Interpreting Display")
        #self.game.display(self.evaluate(stmt.path))
        pass

    def visitOptionsStmt(self, stmt: Options):
        pass

    def visitAudioStmt(self, stmt: Audio):
        pass

    def visitWaitStmt(self, stmt: Wait):
        #print("Interpreting Wait")
        #self.game.wait(self.evaluate(stmt.number))
        pass

    def visitJumpStmt(self, stmt: Jump):
        scene = self.env.get(stmt.dest.lexeme)
        if not isinstance(scene, VNScene):
            raise RuntimeErr(stmt.dest, "Jump Destination Must Be Scene")
        raise JumpErr(scene)

    def visitExitStmt(self, stmt: Exit):
        sys.exit(0)

    def visitExpressionStmt(self, stmt: Expression):
        pass

    def visitAssignExpr(self, expr: Assign):
        pass

    def visitLiteralExpr(self, expr: Literal):
        return expr.value