from typing import Any, List

import env
from stmt import *
from err import *
import interpret

class VNScene:

    def __init__(self, body: List[Stmt], env: 'env.Env'):
        self.body = body
        self.env = env

class VNCallable:

    def arity(self) -> int:
        pass

    def call(self, interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        pass

class VNFunction(VNCallable):

    def __init__(self, declaration: Fun, closure: 'env.Env', ): # Change to 'Function'
        self.declaration = declaration
        self.closure = closure

    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self) -> int:
        return len(self.declaration.args)

    def call(self, interpreter: 'interpret.Interpreter', arguments: List[Any]) -> Any:
        environment = env.Env(self.closure)
        for i in range(len(self.declaration.args)):
            environment.define(self.declaration.args[i].lexeme, arguments[i])
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnErr as r:
            return r.value
        return None

class VNClickCallable(VNCallable):

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn - click>"
    
    def call(self, interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        tmpTok = Token(None, None, None, -1)
        interpreter.checkGraphic(tmpTok, "Can Not Wait Click In Non-Graphic Mode")
        interpreter.game.getClick()

class VNKeyCallable(VNCallable):

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn - key>"
    
    def call(self, interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        tmpTok = Token(None, None, None, -1)
        interpreter.checkGraphic(tmpTok, "Can Not Wait Key In Non-Graphic Mode")
        interpreter.game.getKey()