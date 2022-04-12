from typing import Any, List

from env import Env
from stmt import Function
from interpret import Interpreter

class Return(Exception):

    def __init__(self, value: Any):
        self.value = value

class VNCallable:

    def arity() -> int:
        pass

    def call(interpreter: Interpreter, args: List[Any]) -> Any:
        pass
    
class VNFunction(VNCallable):

    def __init__(self, declaration: Function, closure: Env):
        pass

    def __str__(self) -> str:
        pass

    def arity(self) -> int:
        pass
    
    def call(self, interpreter: Interpreter, arguments: List[Any]) -> Any:
        pass 
