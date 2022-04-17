import os
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
        self.locals = {}
        self.config = {
            'width': 500,
            'height': 500,
            'mode': 'graphic',
            'volume': 0.5
        }
        self.globals.define("readClick", VNClickCallable())
        self.globals.define("readKey", VNClickCallable())

    def interpret(self, configs: List[Config], statements: List[Stmt]) -> None:
        # Error Handling
        try:
            for statement in configs:
                self.execute(statement)
        except RuntimeErr as e:
            pass
        if self.config["mode"] == "graphic":
            self.game = VNGUIGame(
                self.config["width"],
                self.config["height"],
                self.config["volume"]
            )
        else:
            self.game = VNConsoleGame()
        while statements is not None:
            current = statements
            statements = None
            try:
                for statement in current:
                    self.execute(statement)
            except JumpErr as j:
                self.env = j.scene.env
                statements = j.scene.body
            except ReturnErr as r:
                pass
            except RuntimeErr as e:
                print("Runtime Error")
                pass
        
    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def resolvePath(self, path: Token) -> str:
        if not os.path.exists(path.literal):
            raise RuntimeErr(path, "Path \'" + path.literal + "\' Does Not Exist")
        return path.literal

    def visitConfigStmt(self, stmt: Config):
        print("Interpreting Config")
        self.config[stmt.config.value] = stmt.value.literal

    def visitSceneStmt(self, stmt: Scene):
        print("Interpreting Scene")
        scene = VNScene(stmt.body, self.env)
        self.env.define(stmt.name.lexeme, scene)

    def visitImageStmt(self, stmt: Image):
        print("Interpreting Image")
        if self.config["mode"] == "console":
            raise RuntimeErr(stmt.action, "Cannot Use Image In Console Mode")
        if stmt.action == Type.SHOW:
            self.game.showImage(self.resolvePath(stmt.path))
        elif stmt.action == Type.HIDE:
            self.game.hideImage(self.resolvePath(stmt.path))
        self.game.render()

    def visitDisplayStmt(self, stmt: Display):
        print("Interpreting Display")
        self.game.display(stmt.value.literal)
        self.game.render()

    def visitOptionsStmt(self, stmt: Options):
        print("Interpreting Options")
        choice = self.game.popOptions(stmt.cases)
        choice.accept(self)

    def visitAudioStmt(self, stmt: Audio):
        print("Interpreting Audio")
        if self.config["mode"] == "console":
            raise RuntimeErr(stmt.action, "Cannot Use Audio In Console Mode")
        if stmt.action == Type.START:
            self.game.startAudio(self.resolvePath(stmt.path))
        elif stmt.action == Type.STOP:
            self.game.stopAudio()

    def visitDelayStmt(self, stmt: Delay):
        print("Interpreting Delay")
        self.game.delay(stmt.value.literal)

    def visitJumpStmt(self, stmt: Jump):
        print("Interpreting Jump")
        scene = self.env.get(stmt.dest.lexeme)
        if not isinstance(scene, VNScene):
            raise RuntimeErr(stmt.dest, "Jump Destination Must Be Scene")
        raise JumpErr(scene)

    def visitExitStmt(self, stmt: Exit):
        print("Interpreting Exit")
        sys.exit(0)

    def visitExpressionStmt(self, stmt: Expression):
        pass

    def visitAssignExpr(self, expr: Assign):
        pass

    def visitLiteralExpr(self, expr: Literal):
        return expr.value