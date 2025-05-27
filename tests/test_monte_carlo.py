import unittest
from src.inference import monte_carlo_inference
from src.ppl_ast import *

class TestMonteCarloInference(unittest.TestCase):
    def test_simple_program(self):
        parsed_program = [Return(Flip(0.5))]
        self.assertAlmostEqual(monte_carlo_inference(parsed_program, 10000), 0.5, places=1)

    def test_observe_program(self):
        parsed_program = [Assign(Variable("x"), Flip(0.5)), Observe(Variable("x")), Return(Variable("x"))]
        self.assertAlmostEqual(monte_carlo_inference(parsed_program, 10000), 1, places=2)
