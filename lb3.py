# ==========================
# Lab03 : Compiler Design
# Part 1: FIRST and FOLLOW set calculation
# Part 2: Generate Three Address Code (TAC)
# ==========================

# ---------- PART 1: FIRST and FOLLOW SET ----------
grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F": [["(", "E", ")"], ["id"]]
}

terminals = {"id", "+", "*", "(", ")", "ε"}
non_terminals = grammar.keys()
FIRST = {nt: set() for nt in non_terminals}
FOLLOW = {nt: set() for nt in non_terminals}

print("========== GRAMMAR ==========")
for nt, prods in grammar.items():
    print(f"{nt} → {' | '.join(' '.join(p) for p in prods)}")

# --- Compute FIRST ---
def compute_FIRST(X):
    if X in terminals:
        return {X}
    for production in grammar[X]:
        for symbol in production:
            if symbol == X:
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

# --- Compute FOLLOW ---
start_symbol = "E"
FOLLOW[start_symbol].add("$")

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

print("\n========== FIRST SETS ==========")
for nt in non_terminals:
    print(f"FIRST({nt}) = {FIRST[nt]}")

print("\n========== FOLLOW SETS ==========")
for nt in non_terminals:
    print(f"FOLLOW({nt}) = {FOLLOW[nt]}")




# ---------- PART 2: THREE ADDRESS CODE (TAC) ----------
print("\n\n========== THREE ADDRESS CODE (TAC) ==========")
expr = "a = (-c * b) + (-c * d)"
print("Input Expression:", expr, "\n")

temp_count = 1
TAC = []

# Compute -c only once (Optimization)
t1 = f"t{temp_count} = -c"; temp_count += 1

# Multiply t1 * b and t1 * d
t2 = f"t{temp_count} = t1 * b"; temp_count += 1
t3 = f"t{temp_count} = t1 * d"; temp_count += 1

# Add the two results
t4 = f"t{temp_count} = t2 + t3"; temp_count += 1

# Assign final result to a
t5 = f"a = t4"

TAC = [t1, t2, t3, t4, t5]

for line in TAC:
    print(line)
