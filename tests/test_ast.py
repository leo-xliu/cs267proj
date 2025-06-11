import unittest
from src.ppl_ast import *

class TestASTComponents(unittest.TestCase):
    def test_assign_object_initialization(self):
        assign_node = Assign(
                        Variable("x"), Conditional(Variable("y"), False, Variable("x")),
                        Variable("x")
                    )
        self.assertEqual(assign_node.var_node, Variable("x"))
        self.assertEqual(assign_node.expr, Conditional(Variable("y"), False, Variable("x")))
        self.assertEqual(assign_node.next_expr, Variable("x"))

        # Must assign value to a Variable
        self.assertRaises(TypeError, Assign, "string", 1, 2)

    def test_flip_object_initialization(self):
        # Assigning valid probabilities
        self.assertEqual(Flip(0.5).prob, 0.5)
        self.assertEqual(Flip(0).prob, 0)
        self.assertEqual(Flip(1).prob, 1)

        # Invalid probabilities 
        self.assertRaises(TypeError, Flip, "string")
        self.assertRaises(ValueError, Flip, 100)
        self.assertRaises(ValueError, Flip, -0.5)

    def test_or_object_initialization(self):
        or_node = Or(Variable("x"), Flip(0.5))
        self.assertEqual(or_node.l_expr, Variable("x"))
        self.assertEqual(or_node.r_expr, Flip(0.5))

    def test_and_object_initialization(self):
        and_node = And(Variable("x"), Flip(0.5))
        self.assertEqual(and_node.l_expr, Variable("x"))
        self.assertEqual(and_node.r_expr, Flip(0.5))

    def test_not_object_initialization(self):
        not_node = Not(Or(Variable("x"), Flip(0.5)))
        self.assertEqual(not_node.expr, Or(Variable("x"), Flip(0.5)))

    def test_variable_initialization(self):
        var_node = Variable("x")
        self.assertEqual(var_node.name, "x")

    def test_observe_initialization(self):
        obs_node = Observe(And(Variable("x"), Flip(0.5)))
        self.assertEqual(obs_node.expr, And(Variable("x"), Flip(0.5)))

    def test_conditional_initialization(self):
        cond_node = Conditional(Flip(0.4), Variable("x"), Flip(0.7))
        self.assertEqual(cond_node.bool_cond, Flip(0.4))
        self.assertEqual(cond_node.if_path, Variable("x"))
        self.assertEqual(cond_node.else_path, Flip(0.7))

if __name__ == "__main__":
    unittest.main()
