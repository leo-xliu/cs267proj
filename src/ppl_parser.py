from src.ppl_ast import *

class Parser:
    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        ast = []
        self.nflips = 0

        while self.peek()[0] != "EOP":
            # skip empty lines
            if self.peek()[0] == "NEWLINE":
                self.eat("NEWLINE")
                continue
            node = self.parse_next_line()
            ast.append(node)
        return ast, self.nflips
    
    def peek(self):
        return self.tokens[self.pos]

    def eat(self, expected_type):
        token_type, token_val = self.peek()
        if token_type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token_type}")
        self.pos += 1
        return token_type, token_val

    def parse_next_line(self):
        # three distinct variations: assignment, observe, boolean expression 
        type, _ = self.peek()
        # assignment + expression 
        if type == "VAR" and self.tokens[self.pos+1][0] == "ASSIGN": # protected by EOP 
            return self.parse_assign()
        # observation
        if type == "OBSERVE":
            return self.parse_observe()
        # expression 
        return self.parse_expr()

    def parse_assign(self):
        _, name = self.eat("VAR")
        self.eat("ASSIGN")
        expr = self.parse_expr()
        # remove all empty lines first 
        while self.peek()[0] == "NEWLINE":
            self.eat("NEWLINE")

        # reinforce second expression 
        next_expr = self.parse_next_line()

        return Assign(Variable(name), expr, next_expr)

    def parse_observe(self):
        self.eat("OBSERVE")
        self.eat("LPAREN")
        expr = self.parse_expr()
        self.eat("RPAREN")
        return Observe(expr)

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.peek()[0] == "OR":
            self.eat("OR")
            rhs = self.parse_and()
            node = Or(node, rhs)
        return node

    def parse_and(self):
        node = self.parse_not()
        while self.peek()[0] == "AND":
            self.eat("AND")
            rhs = self.parse_not()
            node = And(node, rhs)
        return node

    def parse_not(self):
        if self.peek()[0] == "NOT":
            self.eat("NOT")
            return Not(self.parse_not())
        return self.parse_primary()

    def parse_primary(self):
        type, val = self.peek()
        if type == "BOOLEAN":
            self.eat("BOOLEAN")
            return True if val == "True" else False
        if type == "VAR":
            self.eat("VAR")
            return Variable(val)
        if type == "FLIP":
            self.eat("FLIP")
            self.eat("LPAREN")
            num = float(self.eat("NUMBER")[1])
            self.eat("RPAREN")
            self.nflips += 1
            return Flip(num, id=self.nflips - 1)
        if type == "IF":
            self.eat("IF")
            cond = self.parse_expr()
            self.eat("THEN")
            then_b = self.parse_expr()
            self.eat("ELSE")
            else_b = self.parse_expr()
            return Conditional(cond, then_b, else_b)
        if type == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_expr()
            self.eat("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token {type}")