from typing import Any, List

import env
from stmt import *
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