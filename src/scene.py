
from env import Env
from stmt import *

class VNScene:
    def __init__(self, body: List[Stmt], env: Env):
        self.body = body
        self.env = env
    