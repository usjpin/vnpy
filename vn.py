import sys

from scan import Scanner
from parse import Parser
from resolve import Resolver
from interpret import Interpreter

interpreter = Interpreter()
haderr = False
hadRunErr = False

def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    parser = Parser(tokens)
    statements = parser.parse()
    if (haderr): return
    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    if (haderr): return
    interpreter.interpret(statements)


def runFile(path: str) -> None:
    with open(path) as file:
        err, runerr = run(path)
    if err:
        sys.exit(65)
    if runerr:
        sys.exit(70)


def main(argv: list) -> None:
    if len(argv) != 2:
        print("Usage vn [script]")
        sys.exit(64)
    runFile(argv[1])

if __name__ == '__main__':
    main(sys.argv)