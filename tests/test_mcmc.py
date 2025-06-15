# Unit Testing for Metropolis Hastings MCMC
import unittest
from src.ppl_ast import *
from src.inference import markov_chain_monte_carlo_metropolis_hastings, rejection_sampling

class TestInterpreter(unittest.TestCase):
    def test_eval_program1(self):
        parsed_program = [
            Assign(Variable("x"), Flip(0.6, id=0), 
                   Assign(Variable("y"), Flip(0.3, id=1), 
                          Or(Variable("x"), Variable("y"))))
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=2)
        self.assertAlmostEqual(res, 0.72, delta=0.05)

    def test_network_example(self):
        parsed_program = [
            Assign(Variable("S1"), True,
                   Assign(Variable("route"), Flip(0.5, id=0), 
                          Assign(Variable("S2"), Conditional(Variable("route"), Variable("S1"), False), 
                                 Assign(Variable("S3"), Conditional(Variable("route"), False, Variable("S1")),
                                        Assign(Variable("S4"), Or(
                                            And(Variable("S2"), Not(Flip(0.01, id=1))),
                                            And(Variable("S3"), Not(Flip(0.001, id=2)))
                                        ), 
                                            Observe(Not(Variable("S4")))))))),
            Variable("S2")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 75000, nflips=3)
        self.assertAlmostEqual(res, (0.5 * 0.01) / (0.5 * (0.01 + 0.001)), delta=0.05)

    def test_eval_program3(self):
        # x = True, y = false, z = true  ==> 0.6 * 0.6
        # x = False, y = false, z = true ==> 0.4 * 0.3
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.6, id=0), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.4, id=1), Flip(0.7, id=2)),
                    Assign(
                        Variable("z"), Not(Variable("y")), 
                        Variable("z"))
                )      
            )
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=3)
        self.assertAlmostEqual(res, 0.36 + 0.12, delta=0.05)

    def test_eval_program4(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.6, id=0), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.4, id=1), Flip(0.7, id=2)),
                    Assign(
                        Variable("x"), Conditional(Variable("y"), False, Variable("x")),
                        Variable("x")
                    )
                )
            )
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=3)
        self.assertAlmostEqual(res, 0.36, delta=0.05)
    
    def test_eval_program5(self):
        # 1 - 0.4*0.2 = 1 - 0.08 = 0.92
        parsed_program = [
            Assign(Variable("x"), Flip(0.6, id=0),
                   Assign(Variable("y"), Flip(0.8, id=1), 
                          Observe(Or(Variable("x"), Variable("y"))))),
            Variable("x")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=2)
        self.assertAlmostEqual(res, 0.6 / 0.92, delta=0.05)

    def test_eval_program6(self):
        # 1 - 0.999 * 0.999 = 0.001999
        parsed_program = [
            Assign(Variable("x"), Flip(0.001, id=0), 
                   Assign(Variable("y"), Flip(0.001, id=1), 
                          Observe(Or(Variable("x"), Variable("y"))))),
            Variable("x")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 500000, nflips=2)
        self.assertAlmostEqual(res, 0.001 / 0.001999, delta=0.05)

    def test_eval_program7(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.5, id=0), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.7, id=1), Flip(0.4, id=2)),
                    Observe(Or(Variable("x"), Variable("y")))
                )
            ),
            Assign(
                Variable("x"), Conditional(Variable("y"), Flip(0.9, id=3), Flip(0.2, id=4)),
                Observe(Variable("x"))
            ),
            Variable("x")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=5)
        self.assertAlmostEqual(res, 1, delta=0.05)

    def test_eval_program8(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.5, id=0), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.7, id=1), Flip(0.4, id=2)),
                    Observe(Or(Variable("x"), Variable("y")))
                )
            ),
            Assign(
                Variable("x"), Conditional(Variable("y"), Flip(0.9, id=3), Flip(0.2, id=4)),
                Variable("x")
            ),
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000, nflips=5)
        self.assertAlmostEqual(res, 0.75, delta=0.05)

if __name__ == "__main__":
    unittest.main()