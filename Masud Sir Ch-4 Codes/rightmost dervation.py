# Grammar definition
# S -> SS+ | SS* | a
grammar = {
    "S": ["SS+", "SS*", "a"]
}

def rightmost_derivation(symbols, target, derivation):
    """
    Recursive function to generate rightmost derivation.
    symbols: current list of symbols (terminals + non-terminals)
    target: target string to derive
    derivation: list of derivation steps so far
    """
    current = "".join(symbols)

    # If current string matches target, derivation complete
    if current == target:
        derivation.append(current)
        return derivation

    # If current string is longer than target, backtrack
    if len(current) > len(target):
        return None

    # Expand rightmost non-terminal
    for i in reversed(range(len(symbols))):
        sym = symbols[i]
        if sym in grammar:
            for production in grammar[sym]:
                new_symbols = symbols[:i] + list(production) + symbols[i+1:]
                result = rightmost_derivation(new_symbols, target, derivation + [current])
                if result:
                    return result
            return None  # No production worked
    return None  # No non-terminal left and target not matched

# Example input string
target_string = "aa+a*"

# Generate rightmost derivation
derivation_steps = rightmost_derivation(["S"], target_string, [])

# Print the derivation
if derivation_steps:
    print(f"Grammar S -> SS+ | SS* | a")
    print(f"Rightmost derivation for '{target_string}':")
    for i, step in enumerate(derivation_steps):
        print(f"Step {i}: {step}")
else:
    print(f"No derivation found for the string '{target_string}'.")
