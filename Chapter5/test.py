# Leftmost derivation (reads grammar)
from collections import defaultdict

# --- read grammar ---
n = int(input().strip())                   # number of lines
G = defaultdict(list); NT = set()
for _ in range(n):
    lhs, rhs = map(str.strip, input().split("->"))
    NT.add(lhs); prods = [p.replace(" ", "") for p in rhs.split("|")]
    G[lhs].extend([p for p in prods if p])

target = input("target: ").strip()

def derive(symbols, steps):
    s = "".join(symbols)
    if s == target: return steps + [s]
    if len(s) > len(target): return None
    # prune by terminal prefix match
    pref = []
    for ch in symbols:
        if ch in NT: break
        pref.append(ch)
    if not target.startswith("".join(pref)): return None
    # expand leftmost nonterminal
    for i, ch in enumerate(symbols):
        if ch in NT:
            for prod in G[ch]:
                nxt = symbols[:i] + list(prod) + symbols[i+1:]
                res = derive(nxt, steps + [s])
                if res: return res
            return None
    return None

der = derive(["S"], [])
if der:
    print("Leftmost derivation:")
    for i, st in enumerate(der): print(f"Step {i}: {st}")
else:
    print("No derivation found.")
