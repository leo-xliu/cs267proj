from src.ppl_ast import *
import random

class Interpreter():
    def __init__(self):
        # Map variable names to stored value 
        self.vars = {}
        self.mode = None
    
    def run(self, program, mode=None):
        # Evaluate the entire program sequentially following the array of statements 
        if mode is not None:
            self.mode = "Importance sampling"

        for statement in program:
            if isinstance(statement, Assign):
                self.eval_assign(statement)
            elif isinstance(statement, Return): 
                return self.eval_return(statement)
            elif isinstance(statement, Conditional):
                self.eval_conditional(statement)
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
        # left side will always be a variable node 
        if not isinstance(assign_node.var_node, Variable):
            raise TypeError(
                f"Invalid type in assignment: {type(assign_node.var_node).__name__}"
            )
        if isinstance(assign_node.expr, bool):
            self.vars[assign_node.var_node.name] = assign_node.expr
        elif isinstance(assign_node.expr, Flip):
            self.vars[assign_node.var_node.name] = self.eval_flip(assign_node.expr)
        elif isinstance(assign_node.expr, Or):
            self.vars[assign_node.var_node.name] = self.eval_or(assign_node.expr)
        elif isinstance(assign_node.expr, And):
            self.vars[assign_node.var_node.name] = self.eval_and(assign_node.expr)
        elif isinstance(assign_node.expr, Not):
            self.vars[assign_node.var_node.name] = self.eval_not(assign_node.expr)
        elif isinstance(assign_node.expr, Variable):
            self.vars[assign_node.var_node.name] = self.eval_variable(assign_node.expr)
        elif isinstance(assign_node.expr, Conditional):
            self.vars[assign_node.var_node.name] = self.eval_conditional(assign_node.expr)
        else:
            raise NotImplementedError(
                f"Unknown assignment expression: {type(assign_node.expr).__name__}"
            )

    def eval_flip(self, flip_node: Flip):
        # Evaluate the Flip construct
        prob = flip_node.prob if self.mode is None else flip_node.q_prob
        if prob > random.random():
            flip_node.trace = True
        else:
            flip_node.trace = False
        return flip_node.trace
    
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
        elif isinstance(node, Assign):
            return self.eval_assign(node)
        elif isinstance(node, Or):
            return self.eval_or(node)
        elif isinstance(node, And):
            return self.eval_and(node)
        elif isinstance(node, Not):
            return self.eval_not(node)
        elif isinstance(node, Variable):
            return self.eval_variable(node)
        elif isinstance(node, Conditional):
            return self.eval_conditional(node)
        else:
            raise NotImplementedError(f"Boolean operand not supported: {type(node).__name__}")

    def eval_variable(self, var_node: Variable):
        # Safe guard but not needed since other methods only call this if it is a variable type
        if not isinstance(var_node, Variable):
            raise TypeError(
                f"Invalid variable evaluation type: {type(var_node).__name__}"
            )
        if var_node.name not in self.vars:
            raise NameError(f"Undefined return variable: {var_node.name!r}")
        return self.vars[var_node.name]
    
    def eval_conditional(self, cond_node: Conditional):
        if self.eval_bool(cond_node.bool_cond):
            return self.eval_bool(cond_node.if_path)
        else:
            return self.eval_bool(cond_node.else_path)