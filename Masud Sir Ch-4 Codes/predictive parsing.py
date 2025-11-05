class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.lookahead = self.tokens[self.pos] if self.tokens else None

    def match(self, expected):
        if self.lookahead == expected:
            print(f"Matched: {expected}")
            self.pos += 1
            if self.pos < len(self.tokens):
                self.lookahead = self.tokens[self.pos]
            else:
                self.lookahead = None
        else:
            raise SyntaxError(f"Expected {expected}, found {self.lookahead}")

    def stmt(self):
        """ stmt → expr ; | if ( expr ) stmt | for ( optexpr ; optexpr ) stmt | other """
        if self.lookahead == "if":
            print("Applying rule: stmt → if ( expr ) stmt")
            self.match("if")
            self.match("(")
            self.expr()
            self.match(")")
            self.stmt()
        elif self.lookahead == "for":
            print("Applying rule: stmt → for ( optexpr ; optexpr ) stmt")
            self.match("for")
            self.match("(")
            self.optexpr()
            self.match(";")
            self.optexpr()
            self.match(")")
            self.stmt()
        elif self.lookahead == "other":
            print("Applying rule: stmt → other")
            self.match("other")
        elif self.lookahead == "EXPR":   # expr ;
            print("Applying rule: stmt → expr ;")
            self.expr()
            self.match(";")
        else:
            raise SyntaxError(f"Unexpected token {self.lookahead} in stmt")

    def optexpr(self):
        """ optexpr → ε | expr """
        if self.lookahead == "EXPR":
            print("Applying rule: optexpr → expr")
            self.expr()
        elif self.lookahead in [";", ")"]:
            print("Applying rule: optexpr → ε")
            # epsilon → do nothing
        else:
            raise SyntaxError(f"Unexpected token {self.lookahead} in optexpr")

    def expr(self):
        """ expr → placeholder (just consume EXPR) """
        if self.lookahead == "EXPR":
            print("Applying rule: expr → EXPR")
            self.match("EXPR")
        else:
            raise SyntaxError(f"Expected EXPR, found {self.lookahead}")


examples = [
    ["EXPR", ";"],                             # stmt → expr ;
    ["if", "(", "EXPR", ")", "other", "("],         # stmt → if ( expr ) stmt
    ["for", "(", "EXPR", ";", ")", "other"]    # stmt → for ( optexpr ; optexpr ) stmt
]

for i, tokens in enumerate(examples, start=1):
    print(f"\n=== Example {i} ===")
    print("Input:", " ".join(tokens))
    parser = Parser(tokens)
    try:
        parser.stmt()
        if parser.lookahead is None:
            print("Parsing successful ✅\n")
        else:
            print("Parsing ended with extra tokens:", parser.lookahead)
    except SyntaxError as e:
        print("Syntax Error:", e)
