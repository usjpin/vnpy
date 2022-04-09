from token import Token

class RuntimeErr(Exception):
    def __init__(self, token: Token, message: str):
        super(message)
        self.token = token