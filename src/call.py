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

    def __init__(self, declaration: Any, closure: 'env.Env'): # Change to 'Function'
        pass

    def __str__(self) -> str:
        pass

    def arity(self) -> int:
        pass

    def call(self, interpreter: 'interpret.Interpreter', arguments: List[Any]) -> Any:
        pass

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