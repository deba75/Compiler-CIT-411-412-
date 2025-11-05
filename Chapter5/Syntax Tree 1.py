class Node:
    """Represents a node in the syntax tree"""
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else self.type


def print_tree(node, prefix=""):
    """Recursively prints the tree in a readable structure"""
    print(prefix + str(node))
    for i, child in enumerate(node.children):
        connector = "└── " if i == len(node.children) - 1 else "├── "
        print_tree(child, prefix + connector)


# --- Step 1: Manually build the syntax tree for (a - 4) + c ---
# Structure:
#        +
#       / \
#      -   c
#     / \
#    a   4

id_a = Node("id", "a")
num_4 = Node("num", 4)
id_c = Node("id", "c")

minus_node = Node("operator", "-", [id_a, num_4])
plus_node = Node("operator", "+", [minus_node, id_c])

# Root of the syntax tree
root = plus_node

# --- Step 2: Print the syntax tree ---
print("Syntax Tree for expression: a - 4 + c\n")
print_tree(root)
