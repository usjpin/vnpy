
from tok import Token, Type
from call import VNScene
from typing import Any

class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
    def printErr(self):
        print(self.message + "\n[line " + self.token.line + "]")

class ParseErr(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.printErr()
    def printErr(self):
        if self.token.type == Type.EOF:
            print("[line " + self.token.line + "] Error At End: " + self.message)
        else:
            print("[line " + self.token.line + "] Error At \'" + self.token.lexeme + "\':" + self.message)

class ScanErr(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        self.printErr()
    def printErr(self):
        if self.token.type == Type.EOF:
            print("[line " + self.token.line + "] Error At End: " + self.message)
        else:
            print("[line " + self.token.line + "] Error At \'" + self.token.lexeme + "\':" + self.message)

class JumpErr(Exception):
    def __init__(self, scene: VNScene):
        self.scene = scene

class ReturnErr(Exception):
    def __init__(self, value: Any):
        self.value = value