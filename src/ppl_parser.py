from src.ppl_ast import *

class Parser:
    def __init__(self):
        pass

    def parse(self, program):
        # run parse_line() on the entire program and return AST
        pass

    # ******* Need to enforce that that after an assignment must be a statement that results in a bool *******
    # easiest way may be to restructure assign as a two part that ends up resulting in a bool
    def parse_line(self, line):
        # parse a single line of the program and return it 
        pass