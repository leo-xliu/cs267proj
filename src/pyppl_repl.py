import cmd
from src.ppl_parser import Parser
from src.ppl_interpreter import Interpreter, InferenceMode, ObserveReject
from src.inference import pr_helper
from src.tokenizer import tokenize

class PPLShell(cmd.Cmd):
    intro  = "You have now entered the PyPPL REPL! Type .help for commands."
    prompt = "pyppl> "

    def __init__(self):
        super().__init__()
        self.parser  = Parser()
        self.program = []             
        self.mode    = "rejection_sampling"
        self.n       = 10000        

    def do_run(self, arg):
        """run [algorithm] [n]   — execute inference on the current program"""
        parts = arg.split()
        if parts:
            alg = parts[0]
            if alg == "rejection":
                self.mode = "rejection_sampling"
            elif alg == "importance":
                self.mode = "importance_sampling"
            elif alg == "mcmc":
                self.mode = "mcmc"
        if len(parts) > 1:
            self.n = int(parts[1])
        pr_helper(self.program, 0, self.mode , self.n, False)

    def do_reset(self, arg):
        """reset — clear all statements from the current program"""
        self.program.clear()
        print("Program cleared.")

    def do_exit(self, arg):
        """exit — quit the REPL"""
        return True

    def default(self, line):
        """
        Called when the user enters anything that isn't a do_* command.
        Treat it as a PPL statement and try to parse it.
        """
        try:
            tokens = tokenize(line)
            node, _ = self.parser.parse(tokens)
        except Exception as e:
            print(f"Parse error: {e}")
        else:
            self.program.extend(node)
            print(f"Added: {line}")

def main():
    PPLShell().cmdloop()

if __name__ == "__main__":
    main()