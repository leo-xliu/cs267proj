import unittest
from src.inference import rejection_sampling
from src.ppl_ast import *

class TestRejectionSampling(unittest.TestCase):
    def test_simple_program(self):
        parsed_program = [Return(Flip(0.5))]
        self.assertAlmostEqual(rejection_sampling(parsed_program, 10000), 0.5, places=1)

    def test_observe_program(self):
        parsed_program = [Assign(Variable("x"), Flip(0.5)), Observe(Variable("x")), Return(Variable("x"))]
        self.assertAlmostEqual(rejection_sampling(parsed_program, 10000), 1, places=2)
