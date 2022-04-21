import sys

sys.path.append('src')
sys.setrecursionlimit(5000)

from scan import Scanner
from parse import Parser
from interpret import Interpreter
from print import ASTPrinter

interpreter = Interpreter()
hadErr = False
hadRunErr = False

def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    # for token in tokens:
    #     print(token)
    parser = Parser(tokens)
    configs, statements, hadErr = parser.parse()
    if hadErr: return
    for stmt in configs:
        print(ASTPrinter().print(stmt))
    for stmt in statements:
        print(ASTPrinter().print(stmt))
    hadRunErr = interpreter.interpret(configs, statements)


def runFile(path: str) -> None:
    with open(path) as file:
        run(file.read())
    if hadErr:
        sys.exit(65)
    if hadRunErr:
        sys.exit(70)


def main(argv: list) -> None:
    if len(argv) != 2:
        print("Usage vn [script]")
        sys.exit(64)
    runFile(argv[1])

if __name__ == '__main__':
    main(sys.argv)