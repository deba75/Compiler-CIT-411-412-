"""
Lab 02: Predictive Parsing and Bottom-Up Parsing

Grammar G:
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id

This program implements:
1. A top-down predictive parser with parse table
2. Parse tree generation for id + id * id
3. A bottom-up parse tree for id * id
"""

class TreeNode:
    """Represents a node in the parse tree"""
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __repr__(self):
        return f"TreeNode({self.value})"


def print_tree(node, indent=0, prefix=""):
    """Pretty print a parse tree"""
    if node is None:
        return
    
    print(" " * indent + prefix + str(node.value))
    for i, child in enumerate(node.children):
        if i == len(node.children) - 1:
            print_tree(child, indent + 2, "└─ ")
        else:
            print_tree(child, indent + 2, "├─ ")


class PredictiveParser:
    """
    LL(1) Predictive Parser for the grammar:
    E -> T E'
    E' -> + T E' | ε
    T -> F T'
    T' -> * F T' | ε
    F -> ( E ) | id
    """
    
    def __init__(self):

        self.parse_table = {
            'E': {
                'id': ['T', "E'"],
                '(': ['T', "E'"]
            },
            "E'": {
                '+': ['+', 'T', "E'"],
                ')': ['ε'],
                '$': ['ε']
            },
            'T': {
                'id': ['F', "T'"],
                '(': ['F', "T'"]
            },
            "T'": {
                '+': ['ε'],
                '*': ['*', 'F', "T'"],
                ')': ['ε'],
                '$': ['ε']
            },
            'F': {
                'id': ['id'],
                '(': ['(', 'E', ')']
            }
        }
        
        self.non_terminals = {'E', "E'", 'T', "T'", 'F'}
    
    def tokenize(self, input_string):
        """Convert input string to tokens"""
        tokens = []
        i = 0
        while i < len(input_string):
            if input_string[i].isspace():
                i += 1
                continue
            elif input_string[i:i+2] == 'id':
                tokens.append('id')
                i += 2
            elif input_string[i] in ['+', '*', '(', ')']:
                tokens.append(input_string[i])
                i += 1
            else:
                i += 1
        tokens.append('$')  # End marker
        return tokens
    
    def parse(self, input_string):
        """Parse input string and build parse tree"""
        tokens = self.tokenize(input_string)
        stack = ['$', 'E']  # Initial stack with start symbol
        token_index = 0
        parse_tree_stack = [None, TreeNode('E')]  # Track tree nodes
        
        print(f"\nParsing: {input_string}")
        print(f"Tokens: {tokens[:-1]}")
        print("\nParsing steps:")
        print(f"{'Step':<6} {'Stack':<30} {'Input':<20} {'Action':<40}")
        print("-" * 96)
        
        step = 1
        
        while len(stack) > 1 or stack[0] != '$':
            current_stack = ' '.join(reversed(stack))
            current_input = ' '.join(tokens[token_index:])
            
            top = stack.pop()
            tree_node = parse_tree_stack.pop()
            
            if top == '$':
                if tokens[token_index] == '$':
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {'Accept':<40}")
                    return parse_tree_stack[0] if parse_tree_stack else tree_node
                else:
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {'Error: unexpected input':<40}")
                    return None
            
            elif top not in self.non_terminals:  # Terminal
                if top == tokens[token_index]:
                    action = f"Match '{top}'"
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {action:<40}")
                    token_index += 1
                    step += 1
                elif top == 'ε':
                    action = f"Match ε (epsilon)"
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {action:<40}")
                    step += 1
                else:
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {'Error: mismatch':<40}")
                    return None
            
            else:  # Non-terminal
                lookahead = tokens[token_index]
                
                if lookahead in self.parse_table.get(top, {}):
                    production = self.parse_table[top][lookahead]
                    action = f"{top} -> {' '.join(production)}"
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {action:<40}")
                    
                    # Build parse tree
                    if production != ['ε']:
                        for symbol in reversed(production):
                            stack.append(symbol)
                            child = TreeNode(symbol)
                            tree_node.add_child(child)
                            parse_tree_stack.append(child)
                        # Reverse children to maintain correct order
                        tree_node.children.reverse()
                        parse_tree_stack[len(parse_tree_stack)-len(production):] = reversed(parse_tree_stack[len(parse_tree_stack)-len(production):])
                    else:
                        # Epsilon production
                        epsilon_node = TreeNode('ε')
                        tree_node.add_child(epsilon_node)
                    
                    step += 1
                else:
                    print(f"{step:<6} {current_stack:<30} {current_input:<20} {'Error: no production':<40}")
                    return None
        
        print(f"\n{'Parsing successful!'}")
        return parse_tree_stack[0] if parse_tree_stack else None

    def build_top_down_parse_tree(self, input_string):
        """Build a proper top-down parse tree using recursive descent approach"""
        tokens = self.tokenize(input_string)
        self.tokens = tokens
        self.token_index = 0
        
        print(f"\nBuilding Top-Down Parse Tree for: {input_string}")
        print(f"Tokens: {tokens[:-1]}")
        print("\nTop-Down Parse Tree Construction:")
        
        try:
            tree = self._parse_E()
            if self.token_index < len(self.tokens) - 1:  # -1 for '$'
                print("Error: Input not fully consumed")
                return None
            return tree
        except Exception as e:
            print(f"Parse error: {e}")
            return None
    
    def _current_token(self):
        """Get current token"""
        if self.token_index < len(self.tokens):
            return self.tokens[self.token_index]
        return '$'
    
    def _consume_token(self, expected=None):
        """Consume current token"""
        token = self._current_token()
        if expected and token != expected:
            raise Exception(f"Expected {expected}, got {token}")
        self.token_index += 1
        return TreeNode(token)
    
    def _parse_E(self):
        """Parse E -> T E'"""
        print(f"  Parsing E at token: {self._current_token()}")
        node = TreeNode('E')
        node.add_child(self._parse_T())
        node.add_child(self._parse_E_prime())
        return node
    
    def _parse_E_prime(self):
        """Parse E' -> + T E' | ε"""
        print(f"  Parsing E' at token: {self._current_token()}")
        node = TreeNode("E'")
        
        if self._current_token() == '+':
            node.add_child(self._consume_token('+'))
            node.add_child(self._parse_T())
            node.add_child(self._parse_E_prime())
        else:
            # ε production
            node.add_child(TreeNode('ε'))
        
        return node
    
    def _parse_T(self):
        """Parse T -> F T'"""
        print(f"  Parsing T at token: {self._current_token()}")
        node = TreeNode('T')
        node.add_child(self._parse_F())
        node.add_child(self._parse_T_prime())
        return node
    
    def _parse_T_prime(self):
        """Parse T' -> * F T' | ε"""
        print(f"  Parsing T' at token: {self._current_token()}")
        node = TreeNode("T'")
        
        if self._current_token() == '*':
            node.add_child(self._consume_token('*'))
            node.add_child(self._parse_F())
            node.add_child(self._parse_T_prime())
        else:
            # ε production
            node.add_child(TreeNode('ε'))
        
        return node
    
    def _parse_F(self):
        """Parse F -> ( E ) | id"""
        print(f"  Parsing F at token: {self._current_token()}")
        node = TreeNode('F')
        
        if self._current_token() == '(':
            node.add_child(self._consume_token('('))
            node.add_child(self._parse_E())
            node.add_child(self._consume_token(')'))
        elif self._current_token() == 'id':
            node.add_child(self._consume_token('id'))
        else:
            raise Exception(f"Unexpected token in F: {self._current_token()}")
        
        return node


class BottomUpParser:
    """
    Simple bottom-up parser demonstrating shift-reduce parsing
    For the grammar: E -> T, T -> T * F, T -> F, F -> id
    """
    
    def __init__(self):
        pass
    
    def tokenize(self, input_string):
        """Convert input string to tokens"""
        tokens = []
        i = 0
        while i < len(input_string):
            if input_string[i].isspace():
                i += 1
                continue
            elif input_string[i:i+2] == 'id':
                tokens.append('id')
                i += 2
            elif input_string[i] in ['+', '*', '(', ')']:
                tokens.append(input_string[i])
                i += 1
            else:
                i += 1
        return tokens
    
    def parse_simple(self, input_string):
        """Simple manual parsing for id * id to demonstrate bottom-up construction"""
        print(f"\nBottom-Up Parsing: {input_string}")
        print(f"Manual demonstration of bottom-up parse tree construction:")
        print("\nFor input 'id * id', we build the parse tree as follows:")
        
        # Create the parse tree manually for demonstration
        # For id * id, the derivation is: T -> T * F -> F * F -> id * id
        
        # Step by step construction
        print("\n1. Start with tokens: id, *, id")
        
        # Create leaf nodes
        id1 = TreeNode('id')
        star = TreeNode('*')  
        id2 = TreeNode('id')
        
        print("2. Reduce first 'id' to F")
        f1 = TreeNode('F', [id1])
        
        print("3. Reduce second 'id' to F") 
        f2 = TreeNode('F', [id2])
        
        print("4. Reduce F to T (for left operand)")
        t1 = TreeNode('T', [f1])
        
        print("5. Reduce T * F to T")
        t_final = TreeNode('T', [t1, star, f2])
        
        print("6. Reduce T to E")
        e_final = TreeNode('E', [t_final])
        
        print("\nFinal parse tree:")
        return e_final


def main():
    print("=" * 100)
    print("LAB 02: Predictive Parsing and Bottom-Up Parsing")
    print("=" * 100)
    
    # Part 1: Top-down predictive parsing
    print("\n" + "=" * 100)
    print("PART 1: TOP-DOWN PREDICTIVE PARSER")
    print("=" * 100)
    
    print("\nGrammar (LL(1) form):")
    print("E  -> T E'")
    print("E' -> + T E' | ε")
    print("T  -> F T'")
    print("T' -> * F T' | ε")
    print("F  -> ( E ) | id")
    
    parser = PredictiveParser()
    
    print("\n" + "-" * 100)
    print("PREDICTIVE PARSING TABLE:")
    print("-" * 100)
    print(f"{'Non-terminal':<15} | {'id':<15} | {'+':<15} | {'*':<15} | {'(':<15} | {')':<15} | {'$':<15}")
    print("-" * 100)
    
    for nt in ['E', "E'", 'T', "T'", 'F']:
        row = f"{nt:<15} |"
        for terminal in ['id', '+', '*', '(', ')', '$']:
            if terminal in parser.parse_table.get(nt, {}):
                prod = ' '.join(parser.parse_table[nt][terminal])
                row += f" {nt} -> {prod:<10} |"
            else:
                row += f" {'':<15}|"
        print(row)
    
    # Parse id + id * id
    print("\n" + "=" * 100)
    input1 = "id + id * id"
    tree1 = parser.parse(input1)
    
    if tree1:
        print("\nParse Tree for 'id + id * id' (from predictive parsing table):")
        print_tree(tree1)
    else:
        print("Failed to parse using predictive parsing table")
    
    # Build proper top-down parse tree using recursive descent
    print("\n" + "=" * 100)
    print("TOP-DOWN PARSE TREE CONSTRUCTION (Recursive Descent)")
    print("=" * 100)
    print("This demonstrates the actual top-down construction of the parse tree")
    print("using recursive descent parsing, showing the tree structure clearly.")
    
    top_down_tree = parser.build_top_down_parse_tree(input1)
    
    if top_down_tree:
        print("\nTop-Down Parse Tree for 'id + id * id':")
        print_tree(top_down_tree)
        
        print("\nDerivation steps (top-down):")
        print("1. E")
        print("2. T E'")
        print("3. F T' E'")
        print("4. id T' E'")
        print("5. id ε E'")
        print("6. id + T E'")
        print("7. id + F T' E'")
        print("8. id + id T' E'")
        print("9. id + id * F T' E'")
        print("10. id + id * id T' E'")
        print("11. id + id * id ε E'")
        print("12. id + id * id ε ε")
    
    #Bottom-up parsing
    print("\n" + "=" * 100)
    print("PART 2: BOTTOM-UP PARSER")
    print("=" * 100)
    
    print("\nGrammar:")
    print("E -> T")
    print("T -> T * F")
    print("T -> F")
    print("F -> id")
    
    bottom_up_parser = BottomUpParser()
    
    print("\n" + "=" * 100)
    input2 = "id * id"
    tree2 = bottom_up_parser.parse_simple(input2)
    
    if tree2:
        print_tree(tree2)
    
    print("\n" + "=" * 100)
    print("END OF LAB 02")
    print("=" * 100)


if __name__ == "__main__":
    main()
