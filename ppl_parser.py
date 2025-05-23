
class Assign:
    def __init__(self, name, expr):
        # store left and right side of assign statements 
        self.name = name
        self.expr = expr


# May change this to a more general class for all functions
# Do not need right now since our only callable is Flip
class Flip:
    def __init__(self, theta):
        # store flip function with its probability 
        self.prob = theta

class Parser:
    def __init__(self):
        pass

    def parse(self, program):
        # run parse_line() on the entire program and return AST
        pass

    def parse_line(self, line):
        # parse a single line of the program and return it 
        pass