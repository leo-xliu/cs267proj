from src.ppl_ast import *
import random
from enum import Enum, auto

class ObserveReject(Exception):
    # For rejection sampling on conditioned probability 
    # Catching an exception lets us bubble up chain of functions without return statements everywhere
    pass

class InferenceMode(Enum):
    REJECTION = auto()
    IMPORTANCE = auto()
    MCMC = auto()
    # Add more if needed

class Interpreter():
    def __init__(self, observe_reject=True, mode:InferenceMode=InferenceMode.REJECTION, nflips:int=0):
        # Map variable names to stored value 
        self.vars = {}
        self.observe_reject = observe_reject
        self.mode = mode
        self.weight = 1.0

        # MCMC
        self.initial_state_set = False
        self.nflips = nflips
        self.flip_idx = 0

    def set_mode(self, new_mode):
        self.mode = new_mode

    def run(self, program):  
        if self.initial_state_set:
            # generate initial valid state
            while True:
                try:
                    self.set_mode(InferenceMode.REJECTION)
                    res = self.eval_program(program)
                    self.set_mode(InferenceMode.MCMC)
                    self.initial_state_set = True
                    return res, self.weight
                except ObserveReject:
                    # reset
                    self.weight = 1.0
                    continue  

        self.weight = 1.0   # reset
        res = self.eval_program(program)

        if self.mode == InferenceMode.REJECTION:
            return res
        elif self.mode == InferenceMode.IMPORTANCE:
            return res, self.weight
        elif self.mode == InferenceMode.MCMC:
            # in next proposal state, update next Flip        
            self.flip_idx = (self.flip_idx + 1) % self.nflips
            return res, self.weight
        else:
            raise ValueError(f"Unsupported mode: {self.mode!r}")
        
    def eval_program(self, program):
        # Evaluate the entire program sequentially following the array of statements 
        for i in range(0, len(program)-1):
            self.eval_statement(program[i])
        return self.eval_statement(program[-1], True)
            
    def eval_statement(self, statement, require_return=False):
        if isinstance(statement, Assign):
            return self.eval_assign(statement)
        elif isinstance(statement, Conditional):
            return self.eval_conditional(statement)
        elif isinstance(statement, Observe):
            return self.eval_observe(statement)
        elif not require_return: # Short circuit
            # Only issue is we will never have an unknown statement for no required return
            # This should be taken care by the parser anyway
            return
        elif isinstance(statement, bool):
            return statement
        elif isinstance(statement, Flip):
            return self.eval_flip(statement)
        elif isinstance(statement, And):
            return self.eval_and(statement)
        elif isinstance(statement, Or):
            return self.eval_or(statement)
        elif isinstance(statement, Not):
            return self.eval_not(statement)
        elif isinstance(statement, Variable):
            return self.eval_variable(statement)
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
        self.vars[assign_node.var_node.name] = self.eval_statement(assign_node.expr, True)

        # Enforce second expression
        return self.eval_statement(assign_node.next_expr, True)

    def eval_flip(self, flip_node: Flip):
        # Evaluate the Flip construct
        p = flip_node.prob
        if self.mode is InferenceMode.IMPORTANCE:
            q = flip_node.q_prob
            # Sample under q
            z = q > random.random()

            # importance weight update: p(z)/q(z)
            if z:
                self.weight *= (p/q)
            else:
                self.weight *= ((1-p)/(1-q))
            return z
        
        elif self.mode is InferenceMode.MCMC:
            # generate proposal state
            if flip_node.id == self.flip_idx:
                flip_node.trace = random.random() < p
        elif self.mode is InferenceMode.REJECTION:
            flip_node.trace = random.random() < p
        else:
            raise ValueError(f"{self.mode} is not a valid sampling algorithm.")

        # weight is the joint prob (z, obs)
        self.weight *= p if flip_node.trace else (1-p)
        return flip_node.trace
    
    def eval_or(self, or_node: Or):
        return self.eval_statement(or_node.l_expr, True) or self.eval_statement(or_node.r_expr, True)

    def eval_and(self, and_node: And):
        return self.eval_statement(and_node.l_expr, True) and self.eval_statement(and_node.r_expr, True)

    def eval_not(self, not_node: Not):
        return not self.eval_statement(not_node.expr, True)

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
        if self.eval_statement(cond_node.bool_cond, True):
            return self.eval_statement(cond_node.if_path, True)
        else:
            return self.eval_statement(cond_node.else_path, True)
        
    def eval_observe(self, obs_node: Observe):
        res = self.eval_statement(obs_node.expr, True)
        if not res:
            if self.mode is InferenceMode.REJECTION:
                raise ObserveReject()
            elif self.mode is InferenceMode.IMPORTANCE:
                self.weight *= 0.0
            elif self.mode is InferenceMode.MCMC:
                self.weight *= 0.0
                return False
        return True