
from tok import Token, Type
from typing import Any

# Class for Runtime Errors
class RuntimeErr(Exception):
    # Constructor given token and error message
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
    # Function to print error to console
    def printErr(self):
        print(self.message + "\n[line " + str(self.token.line) + "]")

# Class for error while parsing
class ParseErr(Exception):
    # Constructor given token and error message - note that it also prints on instantiation
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.printErr()

    # Print the error with or without line specified
    def printErr(self):
        if self.token.type == Type.EOF:
            print("[line " + str(self.token.line)+ "] Error At End: " + self.message)
        else:
            print("[line " + str(self.token.line) + "] Error At \'" + self.token.lexeme + "\':" + self.message)

# Class for Scan Error
class ScanErr(Exception):
    # Constructor given token and error message - note that it also prints on instantiation
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.printErr()
    # Print the error with or without line specified
    def printErr(self):
        if self.token.type == Type.EOF:
            print("[line " + str(self.token.line) + "] Error At End: " + self.message)
        else:
            print("[line " + str(self.token.line) + "] Error At \'" + self.token.lexeme + "\':" + self.message)

# Jump error - used when jumping to scenes
class JumpErr(Exception):
    # Constructor given scene
    def __init__(self, scene): # Fix Type
        self.scene = scene

# Return error - used when returning a value
class ReturnErr(Exception):
    # Constructor given value
    def __init__(self, value: Any):
        self.value = value