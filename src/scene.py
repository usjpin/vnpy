
from stmt import Stmt

class VNScene:
    options = []
    
    def __init__(self, name):
        self.name = name

    def getOption(self, idx: int) -> Stmt:
        return self.options[idx]

    def addOption(self, stmt: Stmt) -> None:
        self.options.append(stmt)

    def __str__(self) -> str:
        return "scene " + self.name