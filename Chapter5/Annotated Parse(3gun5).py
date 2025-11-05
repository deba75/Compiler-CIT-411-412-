class Node:
    """
    Represents a node in the parse tree for the grammar in Fig 5.4.
    It holds attributes for synthesized (val, syn) and inherited (inh) values.
    """
    def __init__(self, type, children=None, lexval=None):
        self.type = type
        self.children = children if children else []
        self.lexval = lexval  # Synthesized, from lexer
        
        # Attributes from the SDD (Figure 5.4)
        self.val = None  # Synthesized (for T, F)
        self.inh = None  # Inherited (for T')
        self.syn = None  # Synthesized (for T')

    def __repr__(self):
        # Helper for debugging
        attrs = []
        if self.val is not None: attrs.append(f"val={self.val}")
        if self.inh is not None: attrs.append(f"inh={self.inh}")
        if self.syn is not None: attrs.append(f"syn={self.syn}")
        if not attrs and self.lexval is not None:
             attrs.append(f"lexval={self.lexval}")
        return f"Node({self.type}, {', '.join(attrs)})"

# --- Step 1: Manually build the parse tree for "3 * 5" ---
# This structure is taken directly from Figure 5.5.

# Leaves
digit3 = Node('digit', lexval=3)
digit5 = Node('digit', lexval=5)
epsilon = Node('ϵ') # Represents the empty string terminal for T' -> ϵ

# Build the parse tree structure (bottom-up)
f_3 = Node('F', children=[digit3])                     # F -> digit (for 3)
f_5 = Node('F', children=[digit5])                     # F -> digit (for 5)
t_prime_1 = Node("T'", children=[epsilon])              # T'1 -> ϵ
t_prime_0 = Node("T'", children=['*', f_5, t_prime_1]) # T' -> * F T'1
root = Node('T', children=[f_3, t_prime_0])            # T -> F T'

# --- Step 2: Compute attributes using a single DFS traversal ---

def compute_annotations(node):
    """
    Computes attributes for the tree based on the SDD in Figure 5.4.
    This traversal implements the data dependencies:
    - Synthesized attributes are computed bottom-up.
    - Inherited attributes are passed top-down.
    """
    
    # Rule 4: F -> digit
    # Computes F.val = digit.lexval
    if node.type == 'F' and node.children[0].type == 'digit':
        digit_child = node.children[0]
        # (No child to recurse on, lexval is pre-set)
        node.val = digit_child.lexval
    
    # Rule 2: T' -> * F T'1
    # (MOVED UP to fix attribute error)
    # This check is safe because it compares a string to a string.
    elif node.type == "T'" and node.children[0] == '*':
        # This node *must* have its 'inh' value from its parent.
        f_child = node.children[1]
        t_prime_1_child = node.children[2]
        
        # 1. We need F.val to compute T'1.inh.
        # Recurse on F child to get its 'val'.
        compute_annotations(f_child) # This triggers Rule 4
        
        # 2. Now we can compute and pass down the inherited attribute.
        # T'1.inh = T'.inh * F.val
        t_prime_1_child.inh = node.inh * f_child.val
        
        # 3. We need T'1.syn to compute T'.syn.
        # Recurse on T'1 child to get its 'syn'.
        compute_annotations(t_prime_1_child) # This triggers Rule 3
        
        # 4. Now we can compute our synthesized attribute.
        # T'.syn = T'1.syn
        node.syn = t_prime_1_child.syn

    # Rule 3: T' -> ϵ
    # (MOVED DOWN) This is now safe, as the '*' case was handled.
    elif node.type == "T'" and node.children[0].type == 'ϵ':
        # This node *must* have received its 'inh' value from its parent
        # before this rule is applied.
        node.syn = node.inh
            
    # Rule 1: T -> F T'
    # Computes T'.inh = F.val
    # Computes T.val = T'.syn
    elif node.type == 'T':
        f_child = node.children[0]
        t_prime_child = node.children[1]
        
        # 1. We need F.val to compute T'.inh.
        # Recurse on F child to get its 'val'.
        compute_annotations(f_child) # This triggers Rule 4
        
        # 2. Now we can compute and pass down the inherited attribute.
        # T'.inh = F.val
        t_prime_child.inh = f_child.val
        
        # 3. We need T'.syn to compute T.val.
        # Recurse on T' child to get its 'syn'.
        compute_annotations(t_prime_child) # This triggers Rule 2
        
        # 4. Now we can compute our synthesized attribute.
        # T.val = T'.syn
        node.val = t_prime_child.syn

# --- Step 3: Pretty-print the tree structure ---

def print_tree_structure(node):
    """
    Prints the root node and calls the recursive helper to draw the tree.
    """
    # Helper to format the attribute string
    def get_attr_str(n):
        attrs = []
        if n.val is not None: attrs.append(f"val={n.val}")
        if n.inh is not None: attrs.append(f"inh={n.inh}")
        if n.syn is not None: attrs.append(f"syn={n.syn}")
        if not attrs and n.lexval is not None:
             attrs.append(f"lexval={n.lexval}") # Show lexval for digits
        
        if not attrs:
            return ""
        return f"({', '.join(attrs)})"

    # Print the root node
    print(f"{node.type} {get_attr_str(node)}")
    
    # Call the recursive function for children
    _print_children(node.children, "", get_attr_str)

def _print_children(children_list, prefix, get_attr_str):
    """
    Recursively prints child nodes with proper connectors (├──, └──).
    """
    if not children_list:
        return
        
    last_child_index = len(children_list) - 1
    
    for i, child in enumerate(children_list):
        is_last = (i == last_child_index)
        
        # Determine the connector and the prefix for the next level
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        if isinstance(child, Node):
            # Print the node
            print(f"{prefix}{connector}{child.type} {get_attr_str(child)}")
            # Recurse
            _print_children(child.children, prefix + child_prefix, get_attr_str)
        else:
            # Print simple terminals like '+' or '*'
            print(f"{prefix}{connector}'{child}'")

# --- Step 4: Run the computation and print the result ---

# First, compute the annotations
compute_annotations(root)

print("\n--- Annotated Parse Tree (After Computation) ---")
print("Input: 3 * 5\n")
# Call the print function
print_tree_structure(root)

print("\n-------------------------------------------")
print(f"Final Result: T.val = {root.val}")
print("-------------------------------------------")