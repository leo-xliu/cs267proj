from src.ppl_parser import Parser
from src.ppl_interpreter import Interpreter, ObserveReject, InferenceMode

INFERENCE_ALGORITHM = {
    "rejection_sampling": lambda parsed_program, n: rejection_sampling(parsed_program, n), 
    "importance_sampling": lambda parsed_program, n: importance_sampling_inference(parsed_program, n),
    # add other inference algorithms here
}

def pr(program, inference="rejection_sampling", n=1000):
    parser = Parser()
    parsed_program = parser.parse(program)
    prob_true = INFERENCE_ALGORITHM[inference](parsed_program, n)
    print(f"True ==> {prob_true:.4f},  False ==> {1-prob_true:.4f}")
    
def rejection_sampling(parsed_program, n):
    # simple monte carlo inference by actually running program n times 
    true = 0 
    rejects = 0
    for _ in range(n):
        interpreter = Interpreter(observe_reject=True, mode=InferenceMode.REJECTION)
        try: 
            res = interpreter.run(parsed_program)
        except ObserveReject:
            rejects += 1
            continue
        if res:
            true += 1
    return true / (n - rejects) 

def importance_sampling_inference(parsed_program, n, report=False):
    # currently does not support observe ...
    expected = 0
    for _ in range(n):
        interpreter = Interpreter(observe_reject=False, mode=InferenceMode.IMPORTANCE)
        expected += interpreter.run(parsed_program)
    return expected / n


     
            
