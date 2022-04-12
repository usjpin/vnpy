
from tok import Token

class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        super(message)
        self.token = token

class JumpErr(Exception):
    def __init__(self, dest):
        super().__init__(None, None)
        self.dest = dest

class ReturnErr(Exception):
    pass