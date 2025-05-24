from src.ppl_ast import *
import random

class Interpreter():
    def __init__(self):
        # Map variable names to stored value 
        self.vars = {}
    
    def run(self, program):
        # Evaluate the entire program sequentially following the array of statements 
        for statement in program:
            if isinstance(statement, Assign):
                self.eval_assign(statement)
            elif isinstance(statement, Return):
                return self.eval_return(statement)
            elif isinstance(statement, Flip):
                # Trivial, do nothing 
                continue
            else: # Unknown statement type
                raise NotImplementedError(
                    f"Unknown statement type: {type(statement).__name__}"
                )

    def eval_assign(self, assign_node: Assign):
        # Evaluate right side of an assignment and assign it to variable
        if isinstance(assign_node.expr, bool):
            self.vars[assign_node.name] = assign_node.expr
        elif isinstance(assign_node.expr, Flip):
            self.vars[assign_node.name] = self.eval_flip(assign_node.expr)
        else:
            raise NotImplementedError(
                f"Unknown assignment expression: {type(assign_node.expr).__name__}"
            )

    def eval_flip(self, flip_node: Flip):
        # Evaluate the Flip construct
        if flip_node.prob > random.random():
            return True
        return False
    
    def eval_return(self, return_node: Return):
        # Evaluate return by returning value stored in mapping
        # Variable does not exist 
        if return_node.name not in self.vars:
            raise NameError(f"Undefined return variable: {return_node.name!r}")
        return self.vars[return_node.name]

