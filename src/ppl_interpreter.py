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
            elif isinstance(statement, And):
                continue
            elif isinstance(statement, Or):
                continue
            elif isinstance(statement, Not):
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
        elif isinstance(assign_node.expr, Or):
            self.vars[assign_node.name] = self.eval_or(assign_node.expr)
        elif isinstance(assign_node.expr, And):
            self.vars[assign_node.name] = self.eval_and(assign_node.expr)
        elif isinstance(assign_node.expr, Not):
            self.var[assign_node.name] = self.eval_not(assign_node.expr)
        elif isinstance(assign_node.expr, Variable):
            self.var[assign_node.name] = self.eval_variable(assign_node.expr)
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
        return self.eval_bool(return_node.expr)
    
    def eval_or(self, or_node: Or):
        return self.eval_bool(or_node.l_expr) or self.eval_bool(or_node.r_expr)

    def eval_and(self, and_node: And):
        return self.eval_bool(and_node.l_expr) and self.eval_bool(and_node.r_expr)

    def eval_not(self, not_node: Not):
        return not self.eval_bool(not_node.expr)

    def eval_bool(self, node):
        if isinstance(node, Flip):
            return self.eval_flip(node)
        elif isinstance(node, bool):
            return node
        elif isinstance(node, Or):
            return self.eval_or(node)
        elif isinstance(node, And):
            return self.eval_and(node)
        elif isinstance(node, Not):
            return self.eval_not(node)
        elif isinstance(node, Variable):
            return self.eval_variable(node)
        else:
            raise NotImplementedError(f"Boolean operand not supported: {type(node).__name__}")

    def eval_variable(self, var_node):
        if var_node.name not in self.vars:
            raise NameError(f"Undefined return variable: {var_node.name!r}")
        return self.vars[var_node.name]