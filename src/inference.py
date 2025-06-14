from src.ppl_parser import Parser
from src.ppl_interpreter import Interpreter, ObserveReject, InferenceMode

INFERENCE_ALGORITHM = {
    "rejection_sampling": lambda parsed_program, n: rejection_sampling(parsed_program, n), 
    "importance_sampling": lambda parsed_program, n: importance_sampling_inference(parsed_program, n),
    "mcmc": lambda parsed_program, n: markov_chain_monte_carlo_metropolis_hastings(parsed_program, n),
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
        interpreter = Interpreter(mode=InferenceMode.REJECTION)
        try: 
            res = interpreter.run(parsed_program)
        except ObserveReject:
            rejects += 1
            continue
        if res:
            true += 1
    return true / (n - rejects) 

def importance_sampling_inference(parsed_program, n):
    num, den = 0.0, 0.0
    for _ in range(n):
        interp = Interpreter(mode=InferenceMode.IMPORTANCE)
        res, w = interp.run(parsed_program)
        num += (1 if res else 0) * w
        den += w
    return num/den

def markov_chain_monte_carlo_metropolis_hastings(parsed_program, n, nflips=0):
    burn_in = max(10, n // 10) # use 10% of iterations as burn in
    true, kept = 0, 0

    interp = Interpreter(mode=InferenceMode.MCMC, nflips=nflips)
    curr_res, curr_weight = interp.run(parsed_program)

    for i in range(burn_in + n):
        new_res, new_weight = interp.run(parsed_program)
        
        if curr_weight == 0 or new_weight > 0:
            curr_res, curr_weight = new_res, new_weight

        if i >= burn_in and curr_weight > 0:
            kept += 1
            if curr_res:
                true += 1

    return true / kept if kept else 0.0
     
            
