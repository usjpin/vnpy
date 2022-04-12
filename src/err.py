
from tok import Token
from call import VNScene

class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        super(message)
        self.token = token

class JumpErr(Exception):
    def __init__(self, scene: VNScene):
        super().__init__(None, None)
        self.scene = scene

class ReturnErr(Exception):
    pass