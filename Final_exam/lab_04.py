"""
Lab 04: Grammar Analysis and Parse Tree Construction
Expression: 4 + 3 * 2

Grammar Productions:
1) E → TE'
2) E' → +TE'
3) E' → ε
4) T → FT'
5) T' → *FT'
6) T' → ε
7) F → num

Semantic Rules:
E'.inh = T.val
E.val = E'.syn
E1'.inh = E'.inh + T.val
E'.syn = E1'.syn
E'.syn = E'.inh
T'.inh = F.val
T.val = T'.syn
T1'.inh = T'.inh * F.val
T'.syn = T1'.syn
T'.syn = T'.inh
F.val = num.lexval
"""

class ParseNode:
    def __init__(self, symbol, value=None, children=None):
        self.symbol = symbol
        self.value = value
        self.children = children or []
        self.inh = None  
        self.syn = None  
    
    def __str__(self):
        return f"{self.symbol}(inh={self.inh}, syn={self.syn})"

def solve_lab_problem():
    print("=" * 60)
    print("GRAMMAR ANALYSIS FOR EXPRESSION '4 + 3 * 2'")
    print("=" * 60)
    
    # a) Write down the input expression
    print("\na) Input Expression:")
    print("   4 + 3 * 2")
    
    # b) Apply grammar step-by-step with correct operator precedence
    print("\nb) Grammar Derivation (step-by-step):")
    print("   E → TE'")
    print("   → FT'E'")
    print("   → 4T'E'")
    print("   → 4εE'")
    print("   → 4E'")
    print("   → 4+TE'")
    print("   → 4+FT'E'")
    print("   → 4+3T'E'")
    print("   → 4+3*FT'E'")
    print("   → 4+3*2T'E'")
    print("   → 4+3*2εE'")
    print("   → 4+3*2E'")
    print("   → 4+3*2ε")
    print("   → 4+3*2")
    
    # c) Construct parse tree
    print("\nc) Parse Tree Structure:")
    
    # Root node E
    E = ParseNode("E")
    
   
    T1 = ParseNode("T")
    E_prime1 = ParseNode("E'")
    E.children = [T1, E_prime1]
    
    # T → FT'
    F1 = ParseNode("F")
    T_prime1 = ParseNode("T'")
    T1.children = [F1, T_prime1]
    
    # F → num (4)
    num1 = ParseNode("num", 4)
    F1.children = [num1]
    
    # T' → ε
    epsilon1 = ParseNode("ε")
    T_prime1.children = [epsilon1]
    
    # E' → +TE'
    plus = ParseNode("+")
    T2 = ParseNode("T")
    E_prime2 = ParseNode("E'")
    E_prime1.children = [plus, T2, E_prime2]
    
    # T → FT' (for 3*2)
    F2 = ParseNode("F")
    T_prime2 = ParseNode("T'")
    T2.children = [F2, T_prime2]
    
    # F → num (3)
    num2 = ParseNode("num", 3)
    F2.children = [num2]
    
    # T' → *FT'
    multiply = ParseNode("*")
    F3 = ParseNode("F")
    T_prime3 = ParseNode("T'")
    T_prime2.children = [multiply, F3, T_prime3]
    
    # F → num (2)
    num3 = ParseNode("num", 2)
    F3.children = [num3]
    
    # T' → ε
    epsilon2 = ParseNode("ε")
    T_prime3.children = [epsilon2]
    
    # E' → ε
    epsilon3 = ParseNode("ε")
    E_prime2.children = [epsilon3]
    
    def print_tree(node, indent=0, prefix="", is_last=True):
        # Current node
        connector = "└── " if is_last else "├── "
        if indent == 0:
            connector = ""
        
        if node.value is not None:
            print(f"{prefix}{connector}{node.symbol} ({node.value})")
        else:
            print(f"{prefix}{connector}{node.symbol}")
        
        # Prepare prefix for children
        if indent == 0:
            child_prefix = ""
        else:
            child_prefix = prefix + ("    " if is_last else "│   ")
        
        # Print children with connections
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            print_tree(child, indent + 1, child_prefix, is_last_child)
    
    print_tree(E)
    
    # d) Annotate with inherited and synthesized attributes
    print("\nd) Attribute Annotation:")
    
   
    num1.syn = 4
    num2.syn = 3
    num3.syn = 2
    
    F1.syn = num1.syn  
    F2.syn = num2.syn  
    F3.syn = num3.syn  
    
    
    T_prime1.inh = F1.syn  # 4
    T_prime1.syn = T_prime1.inh  
    
    T_prime3.inh = F3.syn  # 2
    T_prime3.syn = T_prime3.inh  # 2
    
   
    T_prime2.inh = F2.syn  # 3
    
    T_prime2.syn = T_prime2.inh * F3.syn  
    
    # T.val = T'.syn
    T1.syn = T_prime1.syn  
    T2.syn = T_prime2.syn  
    
    # E'.inh = T.val
    E_prime1.inh = T1.syn  # 4
    
    # E1'.inh = E'.inh + T.val
    E_prime2.inh = E_prime1.inh + T2.syn  
    
    
    E_prime2.syn = E_prime2.inh  
    
   
    E_prime1.syn = E_prime2.syn  
    
   
    E.syn = E_prime1.syn  # 10
    
    print(f"   F₁.val = {F1.syn}")
    print(f"   T'₁.inh = {T_prime1.inh}, T'₁.syn = {T_prime1.syn}")
    print(f"   T₁.val = {T1.syn}")
    print(f"   F₂.val = {F2.syn}")
    print(f"   F₃.val = {F3.syn}")
    print(f"   T'₃.inh = {T_prime3.inh}, T'₃.syn = {T_prime3.syn}")
    print(f"   T'₂.inh = {T_prime2.inh}, T'₂.syn = {T_prime2.syn}")
    print(f"   T₂.val = {T2.syn}")
    print(f"   E'₁.inh = {E_prime1.inh}, E'₁.syn = {E_prime1.syn}")
    print(f"   E'₂.inh = {E_prime2.inh}, E'₂.syn = {E_prime2.syn}")
    print(f"   E.val = {E.syn}")
    
    # e) Bottom-up evaluation
    print("\ne) Bottom-up Evaluation Process:")
    print("   Step 1: F₁.val = num₁.lexval = 4")
    print("   Step 2: T'₁.syn = T'₁.inh = F₁.val = 4")
    print("   Step 3: T₁.val = T'₁.syn = 4")
    print("   Step 4: F₂.val = num₂.lexval = 3")
    print("   Step 5: F₃.val = num₃.lexval = 2")
    print("   Step 6: T'₃.syn = T'₃.inh = F₃.val = 2")
    print("   Step 7: T'₂.syn = T'₂.inh * F₃.val = 3 * 2 = 6")
    print("   Step 8: T₂.val = T'₂.syn = 6")
    print("   Step 9: E'₂.inh = E'₁.inh + T₂.val = 4 + 6 = 10")
    print("   Step 10: E'₂.syn = E'₂.inh = 10")
    print("   Step 11: E'₁.syn = E'₂.syn = 10")
    print("   Step 12: E.val = E'₁.syn = 10")
    
    # f) Show final result
    print("\nf) Final Result:")
    print(f"   E.val = {E.syn}")
    print(f"   Therefore, 4 + 3 * 2 = {E.syn}")
    
    print("\n" + "=" * 60)
    print("VERIFICATION:")
    print("The grammar correctly handles operator precedence:")
    print("- Multiplication (*) has higher precedence than addition (+)")
    print("- Expression evaluates as: 4 + (3 * 2) = 4 + 6 = 10")
    print("=" * 60)

if __name__ == "__main__":
    solve_lab_problem()



