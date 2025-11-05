import sys
import re

# --- Step 1: New Node class (from user) ---
class Node:
    """Represents a node in the syntax tree"""
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def __repr__(self):
        # Display helper
        if self.value is not None:
            return f"{self.type} ({self.value})"
        elif self.type in ['+', '-']:
             return f"operator ({self.type})"
        return self.type

# --- Step 2: Recursive Descent Parser (builds Syntax Tree) ---

class SyntaxTreeParser:
    """
    This parser creates a syntax tree from an input string
    based on the grammar and rules from Figure 5.13.
    
    Grammar:
    E  -> T E'
    E' -> + T E' | - T E' | ϵ
    T  -> ( E ) | id | num
    
    Semantic Rules build the tree directly.
    """
    def __init__(self, input_string):
        self.input = input_string
        self.tokens = self.tokenize(input_string)
        self.pos = 0

    def tokenize(self, text):
        """A simple tokenizer."""
        token_specs = [
            ('num',    r'\d+'),
            ('id',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('op',     r'[+\-]'), # + or -
            ('lparen', r'\('),
            ('rparen', r'\)'),
            ('skip',   r'[ \t]+'), # whitespace
            ('mismatch', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        tokens = []
        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'skip':
                continue
            elif kind == 'mismatch':
                raise SyntaxError(f"Illegal character: {value}")
            
            if kind == 'num':
                value = int(value) # Convert numbers
            
            tokens.append((kind, value))
        tokens.append(('eof', None)) # End-of-file token
        return tokens

    def current_token(self):
        """Returns the current token without consuming it."""
        return self.tokens[self.pos]

    def consume(self, expected_kind=None, expected_value=None):
        """Consumes the current token and moves to the next."""
        kind, value = self.current_token()
        if expected_kind and kind != expected_kind:
            raise SyntaxError(f"Expected {expected_kind} but got {kind}")
        if expected_value and value != expected_value:
             raise SyntaxError(f"Expected {expected_value} but got {value}")
        self.pos += 1
        return (kind, value)

    def parse(self):
        """Starts the parsing process."""
        # Start symbol is E
        root_node = self.parse_E()
        # After parsing E, we must be at the end of the input
        if self.current_token()[0] != 'eof':
            raise SyntaxError(f"Unexpected token at end of input: {self.current_token()}")
        return root_node

    def parse_E(self):
        """ E -> T E' """
        # Rule 1 (part 1): E'.inh = T.node
        t_node = self.parse_T()
        # Pass the inherited attribute (the node) to E'
        e_node = self.parse_E_prime(t_node)
        # Rule 1 (part 2): E.node = E'.syn
        return e_node

    def parse_E_prime(self, inh_node):
        """
        E' -> + T E' (Rule 2)
        E' -> - T E' (Rule 3)
        E' -> ϵ      (Rule 4)
        'inh_node' is the inherited attribute E'.inh
        """
        kind, value = self.current_token()

        if kind == 'op':
            if value == '+':
                # Rule 2: E' -> + T E'1
                self.consume(kind, value) # Consume '+'
                t_node = self.parse_T()
                # E'1.inh = new Node('+', E'.inh, T.node)
                new_inh_node = Node('operator', '+', [inh_node, t_node])
                # E'.syn = E'1.syn
                syn_node = self.parse_E_prime(new_inh_node)
                return syn_node
            
            elif value == '-':
                # Rule 3: E' -> - T E'1
                self.consume(kind, value) # Consume '-'
                t_node = self.parse_T()
                # E'1.inh = new Node('-', E'.inh, T.node)
                new_inh_node = Node('operator', '-', [inh_node, t_node])
                # E'.syn = E'1.syn
                syn_node = self.parse_E_prime(new_inh_node)
                return syn_node
        
        # Rule 4: E' -> ϵ
        # E'.syn = E'.inh
        return inh_node # Pass the inherited node up

    def parse_T(self):
        """
        T -> ( E ) (Rule 5)
        T -> id     (Rule 6)
        T -> num    (Rule 7)
        """
        kind, value = self.current_token()

        if kind == 'lparen':
            # Rule 5: T -> ( E )
            self.consume('lparen')
            e_node = self.parse_E()
            self.consume('rparen')
            # T.node = E.node
            return e_node
        
        elif kind == 'id':
            # Rule 6: T -> id
            self.consume('id')
            # T.node = new Leaf(id, id.entry)
            return Node('id', value)
        
        elif kind == 'num':
            # Rule 7: T -> num
            self.consume('num')
            # T.node = new Leaf(num, num.val)
            return Node('num', value)
        
        else:
            raise SyntaxError(f"Expected '(', 'id', or 'num', but got {kind}")

# --- Step 3: New print function (from user) ---

def print_tree(node, prefix="", connector=""):
    """Recursively prints the tree in a readable structure"""
    if prefix == "": # Root node
        print(str(node))
    else:
        print(prefix + connector + str(node))
    
    if node.children:
        next_prefix = prefix + ("│   " if connector == "├── " else "    ")
        for i, child in enumerate(node.children):
            is_last = (i == len(node.children) - 1)
            next_connector = "└── " if is_last else "├── "
            print_tree(child, next_prefix, next_connector)

# --- Step 4: Run the Code ---

def main():
    """
    Takes input from the user, parses it into a syntax tree,
    and prints the result.
    """
    try:
        user_input = input("Enter an expression (e.g., a-4+c or (a+b)*5): ")
        
        if not user_input:
            print("Input is empty.")
            return

        # 1. Create parser and build syntax tree
        parser = SyntaxTreeParser(user_input)
        root = parser.parse()

        # 2. Print the result
        print(f"\n--- Syntax Tree for '{user_input}' ---")
        print_tree(root)
        print("\n-------------------------------------------")

    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# If this script is run directly, call main()
if __name__ == "__main__":
    main()

