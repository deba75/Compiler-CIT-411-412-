from copy import deepcopy

# Example grammar (dictionary: non-terminal -> list of productions)
# Grammar with potential left recursion:
# S -> S a | A b | c
# A -> S d | e
grammar = {
    "S": ["S a", "A b", "c"],
    "A": ["S d", "e"]
}

def eliminate_left_recursion(grammar):
    non_terminals = list(grammar.keys())
    new_grammar = deepcopy(grammar)

    # Step 1 & 2: Arrange non-terminals and handle indirect left recursion
    for i in range(len(non_terminals)):
        Ai = non_terminals[i]
        for j in range(i):
            Aj = non_terminals[j]
            new_productions = []
            for prod in new_grammar[Ai]:
                tokens = prod.split()
                if tokens[0] == Aj:
                    # Replace Ai -> Aj α with Ai -> δ1 α | δ2 α ... for each Aj -> δ
                    for delta in new_grammar[Aj]:
                        new_productions.append(delta + " " + " ".join(tokens[1:]))
                else:
                    new_productions.append(prod)
            new_grammar[Ai] = new_productions

        # Step 3: Eliminate immediate left recursion for Ai
        alpha = []  # productions causing left recursion
        beta = []   # productions not causing left recursion
        for prod in new_grammar[Ai]:
            tokens = prod.split()
            if tokens[0] == Ai:
                alpha.append(" ".join(tokens[1:]))
            else:
                beta.append(prod)

        if alpha:
            # Create a new non-terminal Ai'
            Ai_dash = Ai + "'"
            while Ai_dash in new_grammar:
                Ai_dash += "'"
            # Replace Ai productions
            new_grammar[Ai] = [b + " " + Ai_dash for b in beta]
            # Add Ai' productions
            new_grammar[Ai_dash] = [a + " " + Ai_dash for a in alpha] + ["ε"]  # ε = empty string

    return new_grammar

# Eliminate left recursion
new_grammar = eliminate_left_recursion(grammar)
print("S -> S a | A b | c \n A -> S d | e")
# Print the transformed grammar
print("Grammar after eliminating left recursion:")
for nt, prods in new_grammar.items():
    print(f"{nt} -> {' | '.join(prods)}")
