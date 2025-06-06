import random
# Parsing should fail if program does not meet standards of language 
# Compile time errors should be caught here 
# For example, a statement that results in a bool must follow an assignment

class Assign:
    def __init__(self, var_node, expr):
        # store left and right side of assign statements 
        self.var_node = var_node
        self.expr = expr


# Node for return statement
# May remove this and just use last line in program to indicate return
# That works effortlessly since every statement in the language must result in a bool
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
        self.q_prob = 0.1 if theta < 0.01 else random.uniform(max(0.1, theta - 0.25), min(1, theta + 0.25))

        # Record the sampled value
        self.trace = None

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

# if_path if bool_cond else else_path
class Conditional:
    def __init__(self, bool_cond, if_path, else_path):
        self.bool_cond = bool_cond
        self.if_path = if_path
        self.else_path = else_path

class Observe:
    def __init__(self, expr):
        self.expr = expr