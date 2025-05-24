class Assign:
    def __init__(self, name, expr):
        # store left and right side of assign statements 
        self.name = name
        self.expr = expr


# Node for return statement
# currently very simple as only a single variable can be returned
class Return:
    def __init__(self, expr):
        self.expr = expr

class Flip:
    def __init__(self, theta):
        # store flip function with its probability 
        if not isinstance(theta, (int, float)):
            raise TypeError(
                f"Flip argument must be an int or float: got {type(theta).__name__!r}")
        if theta < 0 or theta > 1:
            raise ValueError(
                f"Flip argument must be a probability between 0 and 1: got {theta!r}")
        self.prob = theta

# May have been better if we created a single class for boolean operators 
# and just have an attribute be the type
class BinaryOperator:
    def __init__(self, l_expr, r_expr):
        self.l_expr = l_expr
        self.r_expr = r_expr

class Or(BinaryOperator):
    pass

class And(BinaryOperator):
    pass

class Not:
    def __init__(self, expr):
        self.expr = expr

class Variable:
    def __init__(self, name):
        self.name = name