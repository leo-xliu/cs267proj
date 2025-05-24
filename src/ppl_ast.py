class Assign:
    def __init__(self, name, expr):
        # store left and right side of assign statements 
        self.name = name
        self.expr = expr


# Node for return statement
# currently very simple as only a single variable can be returned
class Return:
    def __init__(self, name):
        self.name = name


# May change this to a more general class for all functions
# Do not need right now since our only callable is Flip
class Flip:
    def __init__(self, theta):
        # store flip function with its probability 
        if not isinstance(theta, (int, float)):
            raise TypeError(f"Flip argument must be an int or float: got {type(theta).__name__!r}")
        if theta < 0 or theta > 1:
            raise ValueError(f"Flip argument must be a probability between 0 and 1: got {theta!r}")
        self.prob = theta
