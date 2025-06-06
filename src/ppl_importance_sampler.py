# Deprecated for now 
# from src.ppl_ast import *
# from src.ppl_interpreter import Interpreter, InferenceMode

# class Importance_Sampler():
#     def __init__(self, program):
#         # Map variable names to stored sampled_value 
#         self.program = program
#         self.interpreter = Interpreter(mode=InferenceMode.IMPORTANCE)
#         self.p_weight, self.q_weight = 1, 1

#     def sample(self, report=False):
#         # Sample vars from "Q" distribution (i.e. q_prob)
#         res = self.interpreter.run(self.program) 
#         self.compute_weight()

#         if report:
#             print(f"Sample run variables = \n {self.interpreter.vars}\n")
#             print(f"p_weight = {self.p_weight}\n")
#             print(f"q_weight = {self.q_weight}\n")
#             print(f"return = {res}")

#         return res * (self.p_weight / self.q_weight)
    
#     def compute_weight(self):
#         for statement in self.program:
#             if isinstance(statement, Assign):
#                 self.get_prob_assign(statement)
#             elif isinstance(statement, Return): 
#                 self.get_prob_return(statement)
#                 return
#             elif isinstance(statement, Conditional):
#                 self.get_prob_conditional(statement)
#             # Trivial, do nothing 
#             elif isinstance(statement, Flip):
#                 continue
#             elif isinstance(statement, And):
#                 continue
#             elif isinstance(statement, Or):
#                 continue
#             elif isinstance(statement, Not):
#                 continue
#             else:
#                 raise NotImplementedError(
#                     f"Unknown statement type: {type(statement).__name__}"
#                 )

#     def get_prob_assign(self, assign_node: Assign):
#         # Evaluate right side of an assignment and assign it to variable
#         # left side will always be a variable node 
#         if not isinstance(assign_node.var_node, Variable):
#             raise TypeError(
#                 f"Invalid type in assignment: {type(assign_node.var_node).__name__}"
#             )
#         if isinstance(assign_node.expr, bool):
#             return
#         elif isinstance(assign_node.expr, Flip):
#             self.get_prob_flip(assign_node.expr)
#         elif isinstance(assign_node.expr, Or):
#             self.get_prob_or(assign_node.expr)
#         elif isinstance(assign_node.expr, And):
#             self.get_prob_and(assign_node.expr)
#         elif isinstance(assign_node.expr, Not):
#             self.get_prob_not(assign_node.expr)
#         elif isinstance(assign_node.expr, Variable):
#             return
#         elif isinstance(assign_node.expr, Conditional):
#             self.get_prob_conditional(assign_node.expr)
#         else:
#             raise NotImplementedError(
#                 f"Unknown assignment expression: {type(assign_node.expr).__name__}"
#             )
    
#     def get_prob_flip(self, flip_node: Flip):
#         # flip was not executed in the trace
#         if flip_node.trace is None:
#             return
        
#         if flip_node.trace:
#             self.p_weight *= flip_node.prob
#             self.q_weight *= flip_node.q_prob
#         else:
#             self.p_weight *= 1 - flip_node.prob
#             self.q_weight *= 1 - flip_node.q_prob

#         # reset for next sample iteration
#         flip_node.trace = None
    
#     def get_prob_or(self, or_node: Or):
#         # Ex:   x = flip(0.7) or z
#         self.get_prob_bool(or_node.l_expr)
#         self.get_prob_bool(or_node.r_expr)

#     def get_prob_and(self, and_node: And):
#         self.get_prob_bool(and_node.l_expr)
#         self.get_prob_bool(and_node.r_expr)

#     def get_prob_not(self, not_node: Not):
#         self.get_prob_bool(not_node.expr)

#     def get_prob_bool(self, node):
#         if isinstance(node, Flip):
#             self.get_prob_flip(node)
#         elif isinstance(node, bool):
#             return
#         elif isinstance(node, Assign):
#             self.get_prob_assign(node)
#         elif isinstance(node, Or):
#             self.get_prob_or(node)
#         elif isinstance(node, And):
#             self.get_prob_and(node)
#         elif isinstance(node, Not):
#             self.get_prob_not(node)
#         elif isinstance(node, Variable):
#             return
#         elif isinstance(node, Conditional):
#             self.get_prob_conditional(node)
#         else:
#             raise NotImplementedError(f"Boolean operand not supported: {type(node).__name__}")
        
#     def get_prob_return(self, return_node: Return):
#         self.get_prob_bool(return_node.expr)
    
#     def get_prob_conditional(self, cond_node: Conditional):
#         # path taken is determined by the record of a value in Flip
#         self.get_prob_bool(cond_node.if_path)
#         self.get_prob_bool(cond_node.else_path)