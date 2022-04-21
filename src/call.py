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

    def arity() -> int:
        pass

    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        pass

class VNFunction(VNCallable):

    def __init__(self, declaration: Fun, closure: 'env.Env', ): # Change to 'Function'
        self.declaration = declaration
        self.closure = closure

    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self) -> int:
        return self.declaration.args.count

    def call(self, interpreter: 'interpret.Interpreter', arguments: List[Any]) -> Any:
        environment = env.Env(self.closure)
        for i in range(self.declaration.args.count):
            environment.define(self.declaration.args[i].lexeme, arguments[i])
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnErr as r:
            return r.value
        return None


class VNClickCallable(VNCallable):

    def arity() -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"
    
    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        game = interpreter.game
        if game.options is not None:
            return game.getClick()
        raise RuntimeErr(None, "Can Not Call Read Click Native Function")

class VNKeyCallable(VNCallable):

    def arity() -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"
    
    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        game = interpreter.game
        if game.options is not None:
            return game.getClick()
        raise RuntimeErr(None, "Can Not Call Read Key Native Function")