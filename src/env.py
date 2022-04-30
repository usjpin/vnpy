from typing import Any

from tok import Token
from err import *

# Class to establish environment
class Env:
    values = {}

    # Constructor
    def __init__(self, enclosing: 'Env' = None):
        self.enclosing = enclosing
    
    def define(self, name: str, value: Any) -> None:
        # Bind new name to value in dict
        self.values[name] = value

    def assign(self, name: Token, value: Any) -> None:
        # Evaluate RHS for val and search in curr env
        if name.lexeme in self.values:
            # If it is in dict, update value
            self.values[name.lexeme] = value
            return
        # If not in current env, check enclosing envs
        if self.enclosing is not None:
            # Assign value to token in enclosing env
            self.enclosing.assign(name, value)
            return
        # Var not found in any environments - undefined, raise runtime error
        raise RuntimeErr(name, "Undefined Variable \'" + name.lexeme + "\' During Assignment.")

    def get(self, name: Token) -> Any:
        # Check for var in env's dict
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        # Not found in current env - check enclosing envs
        if self.enclosing is not None:
            return self.enclosing.get(name)
        # Not found in any env
        raise RuntimeErr(name, "Undefined Variable \'" + name.lexeme + "\'")
