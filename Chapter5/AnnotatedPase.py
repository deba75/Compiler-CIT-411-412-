import sys

class Node:
    """
    A node in the parse tree.
    Grammar: L, E, E', T, T', F, digit, ( ), +, *, n
    """
    def __init__(self, type, children=None, lexval=None):
        self.type = type
        self.children = children if children else []
        self.lexval = lexval  # from digit
        
        # Attributes
        self.val = None  # Synthesized (L, E, T, F)
        self.inh = None  # Inherited (E', T')
        self.syn = None  # Synthesized (E', T')

    def __repr__(self):
        # Helper for debugging
        attrs = []
        if self.val is not None: attrs.append(f"val={self.val}")
        if self.inh is not None: attrs.append(f"inh={self.inh}")
        if self.syn is not None: attrs.append(f"syn={self.syn}")
        if not attrs and self.lexval is not None:
            attrs.append(f"lexval={self.lexval}")
        return f"Node({self.type}, {', '.join(attrs)})"

# --- Step 1: Recursive Descent Parser (Updated) ---

class RecursiveDescentParser:
    """
    This parser creates a parse tree from a non-left-recursive
    version of the grammar from Figure 5.1.
    
    L  -> E n
    E  -> T E'
    E' -> + T E' | ϵ
    T  -> F T'
    T' -> * F T' | ϵ
    F  -> ( E ) | digit
    """
    def __init__(self, input_string):
        # Remove spaces and add end-marker 'n'
        self.input = input_string.replace(" ", "") + "n"
        self.pos = 0
        self.epsilon_node = Node('ϵ') # ϵ (epsilon) node

    def parse(self):
        """ Starts parsing """
        # Start with the start symbol 'L'
        root_node = self.parse_L()
        # If characters remain after parsing, it's an error
        if self.pos < len(self.input):
            raise SyntaxError(f"Could not parse the entire input. Error from: '{self.input[self.pos:]}'")
        return root_node

    def parse_L(self):
        """ Parses the rule L -> E n """
        e_child = self.parse_E()
        if self.pos < len(self.input) and self.input[self.pos] == 'n':
            self.pos += 1 # Consume 'n'
            return Node('L', children=[e_child, 'n'])
        else:
            raise SyntaxError("Expression is missing the 'n' end-marker.")

    def parse_E(self):
        """ Parses the rule E -> T E' """
        t_child = self.parse_T()
        e_prime_child = self.parse_E_prime()
        return Node('E', children=[t_child, e_prime_child])

    def parse_E_prime(self):
        """
        E' -> + T E' (Rule 2)
        E' -> ϵ      (Rule 3)
        """
        if self.pos < len(self.input) and self.input[self.pos] == '+':
            self.pos += 1 # Consume '+'
            t_child = self.parse_T()
            e_prime_1_child = self.parse_E_prime() # Recursive call
            return Node("E'", children=['+', t_child, e_prime_1_child])
        else:
            # Matched rule E' -> ϵ
            return Node("E'", children=[self.epsilon_node])

    def parse_T(self):
        """ Parses the rule T -> F T' """
        f_child = self.parse_F()
        t_prime_child = self.parse_T_prime()
        return Node('T', children=[f_child, t_prime_child])

    def parse_T_prime(self):
        """
        T' -> * F T' (Rule 4)
        T' -> ϵ      (Rule 5)
        """
        if self.pos < len(self.input) and self.input[self.pos] == '*':
            self.pos += 1 # Consume '*'
            f_child = self.parse_F()
            t_prime_1_child = self.parse_T_prime() # Recursive call
            return Node("T'", children=['*', f_child, t_prime_1_child])
        else:
            # Matched rule T' -> ϵ
            return Node("T'", children=[self.epsilon_node])

    def parse_F(self):
        """
        F -> ( E ) (Rule 6)
        F -> digit  (Rule 7)
        """
        if self.pos < len(self.input) and self.input[self.pos] == '(':
            # Matched rule F -> ( E ) (this check must come first)
            self.pos += 1 # Consume '('
            e_child = self.parse_E()
            if self.pos < len(self.input) and self.input[self.pos] == ')':
                self.pos += 1 # Consume ')'
                return Node('F', children=['(', e_child, ')'])
            else:
                raise SyntaxError("Missing closing parenthesis ')'.")
        
        elif self.pos < len(self.input) and self.input[self.pos].isdigit():
            # Matched rule F -> digit
            digit_val = int(self.input[self.pos])
            self.pos += 1 # Consume digit
            digit_node = Node('digit', lexval=digit_val)
            return Node('F', children=[digit_node])
        
        else:
            raise SyntaxError(f"Expected a digit or '(' at character {self.pos}.")


# --- Step 2: Attribute Computation (Updated and Fixed) ---

def compute_annotations(node):
    """
    Computes the attributes for the tree.
    Implements the synthesized rules from Fig 5.1 using the 
    inherited attribute technique from Fig 5.4.
    """
    
    # --- F Rules ---
    # Rule 6: F -> ( E ) (this check must come before rule 7)
    if node.type == 'F' and node.children[0] == '(':
        e_child = node.children[1]
        compute_annotations(e_child) # Go compute E.val
        node.val = e_child.val # F.val = E.val

    # Rule 7: F -> digit
    elif node.type == 'F' and node.children[0].type == 'digit':
        digit_child = node.children[0]
        # (compute_annotations(digit_child) - not needed)
        node.val = digit_child.lexval # F.val = digit.lexval

    # --- T' Rules (multiplication) ---
    # Rule 4: T' -> * F T'1
    elif node.type == "T'" and node.children[0] == '*':
        f_child = node.children[1]
        t_prime_1_child = node.children[2]
        
        compute_annotations(f_child) # Go compute F.val
        
        # T'1.inh = T'.inh * F.val (left operand * right operand)
        t_prime_1_child.inh = node.inh * f_child.val 
        
        compute_annotations(t_prime_1_child) # Recursion
        
        node.syn = t_prime_1_child.syn # T'.syn = T'1.syn

    # Rule 5: T' -> ϵ (end of multiplication)
    elif node.type == "T'" and node.children[0].type == 'ϵ':
        node.syn = node.inh # T'.syn = T'.inh (pass the accumulated value up)
            
    # --- T Rule ---
    # Rule: T -> F T'
    elif node.type == 'T':
        f_child = node.children[0]
        t_prime_child = node.children[1]
        
        compute_annotations(f_child) # Go compute F.val
        
        # T'.inh = F.val (pass left operand down)
        t_prime_child.inh = f_child.val 
        
        compute_annotations(t_prime_child) # Go compute T'.syn
        
        node.val = t_prime_child.syn # T.val = T'.syn (pass result up)

    # --- E' Rules (addition) ---
    # Rule 2: E' -> + T E'1
    elif node.type == "E'" and node.children[0] == '+':
        t_child = node.children[1]
        e_prime_1_child = node.children[2]
        
        compute_annotations(t_child) # Go compute T.val
        
        # E'1.inh = E'.inh + T.val (left sum + right operand)
        e_prime_1_child.inh = node.inh + t_child.val
        
        compute_annotations(e_prime_1_child) # Recursion
        
        node.syn = e_prime_1_child.syn # E'.syn = E'1.syn

    # Rule 3: E' -> ϵ (end of addition)
    elif node.type == "E'" and node.children[0].type == 'ϵ':
        node.syn = node.inh # E'.syn = E'.inh (pass the accumulated value up)

    # --- E Rule ---
    # Rule: E -> T E'
    elif node.type == 'E':
        t_child = node.children[0]
        e_prime_child = node.children[1]
        
        compute_annotations(t_child) # Go compute T.val
        
        # E'.inh = T.val (pass left operand down)
        e_prime_child.inh = t_child.val
        
        compute_annotations(e_prime_child) # Go compute E'.syn
        
        node.val = e_prime_child.syn # E.val = E'.syn (pass result up)

    # --- L Rule ---
    # Rule 1: L -> E n
    elif node.type == 'L':
        e_child = node.children[0]
        compute_annotations(e_child) # Go compute E.val
        node.val = e_child.val # L.val = E.val

# --- Step 3: Print Tree (Unchanged) ---

def print_tree_structure(node):
    """
    Prints the root node and calls the recursive helper to draw the tree.
    """
    def get_attr_str(n):
        attrs = []
        if n.val is not None: attrs.append(f"val={n.val}")
        if n.inh is not None: attrs.append(f"inh={n.inh}")
        if n.syn is not None: attrs.append(f"syn={n.syn}")
        if not attrs and n.lexval is not None:
            attrs.append(f"lexval={n.lexval}")
        if not attrs: return ""
        return f"({', '.join(attrs)})"

    print(f"{node.type} {get_attr_str(node)}")
    _print_children(node.children, "", get_attr_str)

def _print_children(children_list, prefix, get_attr_str):
    if not children_list:
        return
    last_child_index = len(children_list) - 1
    for i, child in enumerate(children_list):
        is_last = (i == last_child_index)
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        if isinstance(child, Node):
            print(f"{prefix}{connector}{child.type} {get_attr_str(child)}")
            _print_children(child.children, prefix + child_prefix, get_attr_str)
        else:
            print(f"{prefix}{connector}'{child}'")

# --- Step 4: Run the Code ---

def main():
    """
    Takes input from the user, parses, annotates, and shows the result.
    """
    try:
        # User input line is re-enabled
        user_input = input("Enter an expression (e.g., 3*5+4 or 3*(5+4)): ")
        
        if not user_input:
            print("Input is empty.")
            return

        # 1. Create parser and build parse tree
        parser = RecursiveDescentParser(user_input)
        root = parser.parse()

        # 2. Compute attributes in the tree
        compute_annotations(root)

        # 3. Print the result
        print(f"\n--- Annotated parse tree for '{user_input}' ---")
        print_tree_structure(root)
        print("\n-------------------------------------------")
        print(f"Final Result: L.val = {root.val}")
        print("-------------------------------------------")

    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# If this script is run directly, call main()
if __name__ == "__main__":
    main()

