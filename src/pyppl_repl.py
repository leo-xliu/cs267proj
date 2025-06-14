import cmd
from ppl_parser import Parser
from ppl_interpreter import Interpreter, InferenceMode, ObserveReject

class PPLShell(cmd.Cmd):
    intro  = "You have now entered the PyPPL REPL! Type .help for commands."
    prompt = "pyppl> "

    def __init__(self):
        super().__init__()
        self.parser  = Parser()
        self.program = []              # list of AST statements
        self.mode    = InferenceMode.REJECTION
        self.n       = 1000            # default sample count

    def do_run(self, arg):
        """run [algorithm] [n]   — execute inference on the current program"""
        parts = arg.split()
        if parts:
            alg = parts[0]
            if alg in ("rejection", "importance"):
                self.mode = (
                  InferenceMode.REJECTION   if alg=="rejection"
                  else InferenceMode.IMPORTANCE
                )
        if len(parts) > 1:
            self.n = int(parts[1])

        interp = Interpreter(mode=self.mode)
        # dispatch based on mode
        if self.mode is InferenceMode.REJECTION:
            true, total = 0, 0
            for _ in range(self.n):
                interp = Interpreter(mode=self.mode)
                try:
                    res = interp.run(self.program)
                except ObserveReject:
                    continue
                total += 1
                if res: true += 1
            print(f"P(true) ≈ {true/total:.4f}")
        else:
            num, den = 0.0, 0.0
            for _ in range(self.n):
                interp = Interpreter(mode=self.mode)
                val, w = interp.run(self.program)
                num += (1 if val else 0) * w
                den += w
            print(f"P(true) ≈ {num/den:.4f}")

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
        We'll treat it as a PPL statement and try to parse it.
        """
        try:
            stmt = self.parser.parse_line(line)
        except Exception as e:
            print(f"Parse error: {e}")
        else:
            self.program.append(stmt)
            print(f"Added: {line}")

if __name__ == "__main__":
    PPLShell().cmdloop()
