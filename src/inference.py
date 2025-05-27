from src.ppl_parser import Parser
from src.ppl_interpreter import Interpreter
from src.ppl_importance_sampler import Importance_Sampler

INFERENCE_ALGORITHM = {
    "monte_carlo": lambda parsed_program, n: monte_carlo_inference(parsed_program, n), 
    "importance_sampling": lambda parsed_program, n: importance_sampling_inference(parsed_program, n),
    # add other inference algorithms here
}

def pr(program, inference="monte_carlo", n=1000):
    parser = Parser()
    parsed_program = parser.parse(program)
    prob_true = INFERENCE_ALGORITHM[inference](parsed_program, n)
    print(f"True ==> {prob_true:.4f},  False ==> {1-prob_true:.4f}")
    
def monte_carlo_inference(parsed_program, n):
    # simple monte carlo inference by actually running program n times 
    true = 0 
    for _ in range(n):
        interpreter = Interpreter()
        res = interpreter.run(parsed_program)
        if res:
            true += 1
    return true / n 

def importance_sampling_inference(parsed_program, n, report=False):
    # currently does not support observe ...
    expected = 0
    for _ in range(n):
        importance_sampler = Importance_Sampler(parsed_program)
        expected += importance_sampler.sample()
    return expected / n


     
            
