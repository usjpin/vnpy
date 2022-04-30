from typing import Any, List

import env
from stmt import *
from err import *
import interpret

# Class created for scenes
class VNScene:

    # Constructor using the scene body and environment
    def __init__(self, body: List[Stmt], env: 'env.Env'):
        self.body = body
        self.env = env

#Class created for callable functions
class VNCallable:

    #Function to check how many args are expected
    def arity() -> int:
        pass

    # Call the function using the args passed in an interpreter in case it is necessary
    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        pass

# Class for VNFunctions
class VNFunction(VNCallable):

    # Constructor using function declaration and current closure
    def __init__(self, declaration: Fun, closure: 'env.Env', ):
        self.declaration = declaration
        self.closure = closure

    # toString function for printing VNFuncitons
    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"

    # Returns number of args needed in function declaration
    def arity(self) -> int:
        return len(self.declaration.args)

    def call(self, interpreter: 'interpret.Interpreter', arguments: List[Any]) -> Any:
        # Create new env when called
        environment = env.Env(self.closure)
        # Parse args in envirionment
        for i in range(len(self.declaration.args)):
            environment.define(self.declaration.args[i].lexeme, arguments[i])
        try:
            # Try to execute body of function
            interpreter.executeBlock(self.declaration.body, environment)
        # Return value returned from function
        except ReturnErr as r:
            return r.value
        return None

# Class for VNClickCallable
class VNClickCallable(VNCallable):

    # No args needed
    def arity() -> int:
        return 0

    # Print simple native function obj
    def __str__(self) -> str:
        return "<native fn>"

    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        # Get game from current interpreter
        game = interpreter.game

        # Return action that occurs when clicked
        if game.options is not None:
            return game.getClick()

        # No action on click specified
        raise RuntimeErr(None, "Can Not Call Read Click Native Function")

# VNKeyCallable class
class VNKeyCallable(VNCallable):

    # No args needed
    def arity() -> int:
        return 0

    # Print simple native function obj
    def __str__(self) -> str:
        return "<native fn>"
    
    def call(interpreter: 'interpret.Interpreter', args: List[Any]) -> Any:
        # Get game from current interpreter
        game = interpreter.game

        # Return action that occurs when clicked
        if game.options is not None:
            return game.getClick()

        # No action on click specified
        raise RuntimeErr(None, "Can Not Call Read Key Native Function")