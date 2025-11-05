"""

Grammar G:
E -> + T E | E 
E -> T E'
E' -> + T E' | ε
T -> F T'  
T' -> * F T' | ε
F -> ( E ) | id
"""

class FirstFollowComputer:
    """Computes FIRST and FOLLOW sets for a context-free grammar"""
    
    def __init__(self):
        # Define the grammar productions
        # Format: LHS -> [RHS1, RHS2, ...]
        self.grammar = {
            'E': [['T', "E'"]],
            "E'": [['+', 'T', "E'"], ['ε']],
            'T': [['F', "T'"]],
            "T'": [['*', 'F', "T'"], ['ε']],
            'F': [['(', 'E', ')'], ['id']]
        }
        
        self.non_terminals = set(self.grammar.keys())
        self.terminals = {'+', '*', '(', ')', 'id', 'ε', '$'}
        
        self.first_sets = {}
        self.follow_sets = {}
        
        # Initialize FIRST and FOLLOW sets
        for nt in self.non_terminals:
            self.first_sets[nt] = set()
            self.follow_sets[nt] = set()
    
    def compute_first_sets(self):
        """Compute FIRST sets for all non-terminals"""
        changed = True
        
        while changed:
            changed = False
            
            for lhs in self.grammar:
                for production in self.grammar[lhs]:
                    # Get FIRST of the production
                    first_prod = self.first_of_production(production)
                    
                    # Add to FIRST(lhs) if new
                    old_size = len(self.first_sets[lhs])
                    self.first_sets[lhs].update(first_prod)
                    if len(self.first_sets[lhs]) > old_size:
                        changed = True
    
    def first_of_production(self, production):
        """Compute FIRST set of a production (sequence of symbols)"""
        if not production or production == ['ε']:
            return {'ε'}
        
        first = set()
        
        for i, symbol in enumerate(production):
            if symbol in self.terminals:
                first.add(symbol)
                break
            elif symbol in self.non_terminals:
                symbol_first = self.first_sets[symbol].copy()
                symbol_first.discard('ε')
                first.update(symbol_first)
                
                # If ε not in FIRST(symbol), stop
                if 'ε' not in self.first_sets[symbol]:
                    break
                # If this is the last symbol and all previous had ε
                elif i == len(production) - 1:
                    first.add('ε')
        
        return first
    
    def compute_follow_sets(self):
        """Compute FOLLOW sets for all non-terminals"""
        # Add $ to FOLLOW of start symbol
        self.follow_sets['E'].add('$')
        
        changed = True
        
        while changed:
            changed = False
            
            for lhs in self.grammar:
                for production in self.grammar[lhs]:
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:
                            # Rest of production after this symbol
                            beta = production[i + 1:]
                            
                            old_size = len(self.follow_sets[symbol])
                            
                            if beta:
                                # FIRST(β) - {ε} goes to FOLLOW(symbol)
                                first_beta = self.first_of_production(beta)
                                first_beta_no_eps = first_beta.copy()
                                first_beta_no_eps.discard('ε')
                                self.follow_sets[symbol].update(first_beta_no_eps)
                                
                                # If ε in FIRST(β), add FOLLOW(lhs)
                                if 'ε' in first_beta:
                                    self.follow_sets[symbol].update(self.follow_sets[lhs])
                            else:
                                # β is empty, add FOLLOW(lhs)
                                self.follow_sets[symbol].update(self.follow_sets[lhs])
                            
                            if len(self.follow_sets[symbol]) > old_size:
                                changed = True
    
    def display_sets(self):
        """Display computed FIRST and FOLLOW sets"""
        print("=" * 80)
        print("FIRST AND FOLLOW SETS COMPUTATION")
        print("=" * 80)
        
        print("\nGrammar Productions:")
        for lhs in self.grammar:
            for production in self.grammar[lhs]:
                rhs = ' '.join(production)
                print(f"  {lhs} -> {rhs}")
        
        print("\n" + "-" * 50)
        print("FIRST SETS:")
        print("-" * 50)
        for nt in sorted(self.non_terminals):
            first_list = sorted(list(self.first_sets[nt]))
            print(f"  FIRST({nt}) = {{{', '.join(first_list)}}}")
        
        print("\n" + "-" * 50)
        print("FOLLOW SETS:")
        print("-" * 50)
        for nt in sorted(self.non_terminals):
            follow_list = sorted(list(self.follow_sets[nt]))
            print(f"  FOLLOW({nt}) = {{{', '.join(follow_list)}}}")


class ThreeAddressCodeGenerator:
    """Generates three-address code for arithmetic expressions"""
    
    def __init__(self):
        self.temp_count = 0
        self.code = []
    
    def new_temp(self):
        """Generate a new temporary variable"""
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def tokenize(self, expr):
        """Simple tokenizer for arithmetic expressions"""
        tokens = []
        i = 0
        while i < len(expr):
            if expr[i].isspace():
                i += 1
            elif expr[i].isalpha():
                # Variable name
                j = i
                while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            elif expr[i] in '+-*/()=':
                tokens.append(expr[i])
                i += 1
            else:
                i += 1
        return tokens
    
    def infix_to_postfix(self, tokens):
        """Convert infix expression to postfix using Shunting Yard algorithm"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operators = []
        
        for token in tokens:
            if token.isalnum():  # Operand
                output.append(token)
            elif token in precedence:  # Operator
                while (operators and operators[-1] != '(' and
                       operators[-1] in precedence and
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators:
                    operators.pop()  # Remove '('
        
        while operators:
            output.append(operators.pop())
        
        return output
    
    def generate_code(self, postfix):
        """Generate three-address code from postfix expression"""
        stack = []
        
        for token in postfix:
            if token.isalnum():  # Operand
                stack.append(token)
            else:  # Operator
                if len(stack) >= 2:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    temp = self.new_temp()
                    
                    instruction = f"{temp} = {operand1} {token} {operand2}"
                    self.code.append(instruction)
                    stack.append(temp)
        
        return stack[0] if stack else None
    
    def process_assignment(self, expr):
        """Process assignment expression like 'a = (c + b) * (c * d)'"""
        # Split by '=' to get variable and expression
        if '=' in expr:
            parts = expr.split('=', 1)
            var = parts[0].strip()
            expression = parts[1].strip()
        else:
            var = "result"
            expression = expr
        
        # Tokenize and convert to postfix
        tokens = self.tokenize(expression)
        postfix = self.infix_to_postfix(tokens)
        
        # Generate three-address code
        result_temp = self.generate_code(postfix)
        
        # Add final assignment
        if result_temp:
            self.code.append(f"{var} = {result_temp}")
        
        return postfix, result_temp
    
    def display_code_generation(self, expr):
        """Display the complete code generation process"""
        print("\n" + "=" * 80)
        print("THREE-ADDRESS CODE GENERATION")
        print("=" * 80)
        
        print(f"\nInput Expression: {expr}")
        
        # Reset for this expression
        self.temp_count = 0
        self.code = []
        
        postfix, result = self.process_assignment(expr)
        
        print(f"\nPostfix Expression: {' '.join(postfix)}")
        
        print(f"\nThree-Address Code:")
        print("-" * 40)
        for i, instruction in enumerate(self.code, 1):
            print(f"  {i}. {instruction}")
        
        print(f"\nDerivation steps:")
        print("-" * 40)
        step = 1
        temp_count = 0
        stack = []
        
        for token in postfix:
            if token.isalnum():
                stack.append(token)
                print(f"  {step}. Push operand '{token}' to stack")
            else:
                if len(stack) >= 2:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    temp_count += 1
                    temp = f"t{temp_count}"
                    
                    print(f"  {step}. Generate: {temp} = {operand1} {token} {operand2}")
                    stack.append(temp)
            step += 1


def main():
    print("LAB 03: FIRST/FOLLOW Sets and Three-Address Code Generation")
    print("=" * 80)
    
    # Part 1: FIRST and FOLLOW sets computation
    ff_computer = FirstFollowComputer()
    ff_computer.compute_first_sets()
    ff_computer.compute_follow_sets()
    ff_computer.display_sets()
    
    # Part 2: Three-address code generation
    code_gen = ThreeAddressCodeGenerator()
    
    # Generate code for the specific expression from the lab
    expression = "a = (c + b) * (c * d)"
    code_gen.display_code_generation(expression)
    
    print("\n" + "=" * 40)
    print("END")
    print("=" * 40)


if __name__ == "__main__":
    main()
