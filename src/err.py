
from tok import Token
from call import VNScene

class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

class JumpErr(Exception):
    def __init__(self, scene: VNScene):
        self.scene = scene

class ReturnErr(Exception):
    pass