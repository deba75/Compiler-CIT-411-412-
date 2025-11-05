# Lab03 - Optimized Three Address Code (TAC)
expr = "a = (-c * b) + (-c * d)"

print("Input Expression:", expr)
print("\nOptimized Three Address Code (TAC):")

temp_count = 1
TAC = []

# Compute -c only once
t1 = f"t{temp_count} = -c"; temp_count += 1

# Multiply t1 * b and t1 * d
t2 = f"t{temp_count} = t1 * b"; temp_count += 1
t3 = f"t{temp_count} = t1 * d"; temp_count += 1

# Add the two results
t4 = f"t{temp_count} = t2 + t3"; temp_count += 1

# Assign to a
t5 = f"a = t4"

TAC = [t1, t2, t3, t4, t5]

for line in TAC:
    print(line)
