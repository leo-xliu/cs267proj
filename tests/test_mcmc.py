# Unit Testing for Metropolis Hastings MCMC
import unittest
from src.ppl_ast import *
from src.inference import markov_chain_monte_carlo_metropolis_hastings, rejection_sampling

class TestInterpreter(unittest.TestCase):
    def test_eval_program1(self):
        parsed_program = [
            Assign(Variable("x"), Flip(0.6), 
                   Assign(Variable("y"), Flip(0.3), 
                          Or(Variable("x"), Variable("y"))))
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.72, delta=0.03)

    def test_network_example(self):
        parsed_program = [
            Assign(Variable("S1"), True,
                   Assign(Variable("route"), Flip(0.5), 
                          Assign(Variable("S2"), Conditional(Variable("route"), Variable("S1"), False), 
                                 Assign(Variable("S3"), Conditional(Variable("route"), False, Variable("S1")),
                                        Assign(Variable("S4"), Or(
                                            And(Variable("S2"), Not(Flip(0.01))),
                                            And(Variable("S3"), Not(Flip(0.001)))
                                        ), 
                                            Observe(Not(Variable("S4")))))))),
            Variable("S2")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 50000)
        self.assertAlmostEqual(res, (0.5 * 0.01) / (0.5 * (0.01 + 0.001)), delta=0.05)

    def test_eval_program3(self):
        # x = True, y = false, z = true  ==> 0.6 * 0.6
        # x = False, y = false, z = true ==> 0.4 * 0.3
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.6), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.4), Flip(0.7)),
                    Assign(
                        Variable("z"), Not(Variable("y")), 
                        Variable("z"))
                )      
            )
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.36 + 0.12, delta=0.03)

    def test_eval_program4(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.6), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.4), Flip(0.7)),
                    Assign(
                        Variable("x"), Conditional(Variable("y"), False, Variable("x")),
                        Variable("x")
                    )
                )
            )
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.36, delta=0.02)
    
    def test_eval_program5(self):
        # 1 - 0.4*0.2 = 1 - 0.08 = 0.92
        parsed_program = [
            Assign(Variable("x"), Flip(0.6),
                   Assign(Variable("y"), Flip(0.8), 
                          Observe(Or(Variable("x"), Variable("y"))))),
            Variable("x")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.6 / 0.92, delta=0.03)

    def test_eval_program6(self):
        # 1 - 0.999 * 0.999 = 0.001999
        parsed_program = [
            Assign(Variable("x"), Flip(0.001), 
                   Assign(Variable("y"), Flip(0.001), 
                          Observe(Or(Variable("x"), Variable("y"))))),
            Variable("x")
        ]
        res = rejection_sampling(parsed_program, 500000)
        self.assertAlmostEqual(res, 0.001 / 0.001999, delta=0.035)

    def test_eval_program7(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.5), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.7), Flip(0.4)),
                    Observe(Or(Variable("x"), Variable("y")))
                )
            ),
            Assign(
                Variable("x"), Conditional(Variable("y"), Flip(0.9), Flip(0.2)),
                Observe(Variable("x"))
            ),
            Variable("x")
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 1, delta=0.03)

    def test_eval_program8(self):
        parsed_program = [
            Assign(
                Variable("x"), Flip(0.5), 
                Assign(
                    Variable("y"), Conditional(Variable("x"), Flip(0.7), Flip(0.4)),
                    Observe(Or(Variable("x"), Variable("y")))
                )
            ),
            Assign(
                Variable("x"), Conditional(Variable("y"), Flip(0.9), Flip(0.2)),
                Variable("x")
            ),
        ]
        res = markov_chain_monte_carlo_metropolis_hastings(parsed_program, 10000)
        self.assertAlmostEqual(res, 0.75, delta=0.03)

if __name__ == "__main__":
    unittest.main()