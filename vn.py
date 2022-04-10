import sys

sys.path.append('src')
sys.setrecursionlimit(5000)

from scan import Scanner
from parse import Parser
from resolve import Resolver
from interpret import Interpreter
from astprint import ASTPrinter

interpreter = Interpreter()
hadErr = False
hadRunErr = False

def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    parser = Parser(tokens)
    statements = parser.parse()
    '''for stmt in statements:
        print(ASTPrinter().print(stmt))'''
    if hadErr: return
    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    if hadErr: return
    interpreter.interpret(statements)


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