import sys

# Add source files to path
sys.path.append('src')
# Set recrusion stack limit higher as parsing/interpreter
#   can have a very tall call stack
sys.setrecursionlimit(5000)

from scan import Scanner
from parse import Parser
from interpret import Interpreter
from print import ASTPrinter

# Initialize interpreter and error variables
interpreter = Interpreter()
hadErr = False
hadRunErr = False

# Function to run source code
def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    # for token in tokens:
    #     print(token)
    parser = Parser(tokens)
    configs, statements, hadErr = parser.parse()
    if hadErr: return
    # for stmt in configs:
    #     print(ASTPrinter().print(stmt))
    # for stmt in statements:
    #     print(ASTPrinter().print(stmt))
    hadRunErr = interpreter.interpret(configs, statements)

# Function to load file and run contents
def runFile(path: str) -> None:
    with open(path) as file:
        run(file.read())
    if hadErr:
        sys.exit(65)
    if hadRunErr:
        sys.exit(70)

# Function to check argument list with vn.py use
def main(argv: list) -> None:
    if len(argv) != 2:
        print("Usage vn [script]")
        sys.exit(64)
    runFile(argv[1])

# Entry point
if __name__ == '__main__':
    main(sys.argv)