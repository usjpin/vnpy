
from stmt import *

class VNScene:
    options = None
    
    def __init__(self, name):
        self.name = name

    def setOptions(self, options: Options):
        self.options = options

    def __str__(self) -> str:
        return "scene " + self.name