# Example Grammar
grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F": [["(", "E", ")"], ["id"]]
}

non_terminals = grammar.keys()
terminals = {"id", "+", "*", "(", ")", "ε"}  # include ε as terminal

FIRST = {nt: set() for nt in non_terminals}
FOLLOW = {nt: set() for nt in non_terminals}

# Display grammar
print("Grammar:")
for nt, prods in grammar.items():
    prod_str = [" ".join(p) for p in prods]
    print(f"{nt} → {' | '.join(prod_str)}")
print("\n")

# --- Compute FIRST sets ---
def compute_FIRST(X):
    if X in terminals:
        return {X}  # treat terminals and ε as their own FIRST
    for production in grammar[X]:
        for symbol in production:
            if symbol == X:  # avoid infinite recursion
                break
            first_sym = compute_FIRST(symbol)
            FIRST[X].update(first_sym - {"ε"})
            if "ε" not in first_sym:
                break
        else:
            FIRST[X].add("ε")
    return FIRST[X]

for nt in non_terminals:
    compute_FIRST(nt)

# --- Compute FOLLOW sets ---
start_symbol = "E"
FOLLOW[start_symbol].add("$")  # end of input

def compute_FOLLOW():
    changed = True
    while changed:
        changed = False
        for nt in non_terminals:
            for production in grammar[nt]:
                for i, B in enumerate(production):
                    if B in non_terminals:
                        follow_before = FOLLOW[B].copy()
                        beta = production[i+1:]
                        if beta:
                            first_beta = set()
                            for symbol in beta:
                                first_sym = compute_FIRST(symbol)
                                first_beta.update(first_sym - {"ε"})
                                if "ε" not in first_sym:
                                    break
                            else:
                                FOLLOW[B].update(FOLLOW[nt])
                            FOLLOW[B].update(first_beta)
                        else:
                            FOLLOW[B].update(FOLLOW[nt])
                        if follow_before != FOLLOW[B]:
                            changed = True

compute_FOLLOW()

# --- Print FIRST and FOLLOW sets ---
print("FIRST sets:")
for nt in non_terminals:
    print(f"FIRST({nt}) = {FIRST[nt]}")

print("\nFOLLOW sets:")
for nt in non_terminals:
    print(f"FOLLOW({nt}) = {FOLLOW[nt]}")
