from itertools import combinations
from itertools import permutations

# Generate every possible combnination
combs = {com for i in range(len(x)) for com in combinations(x, i)}
combs_strs = ''.join(comb) for combs in combs]

# Generate every possible permutation.
# Doing this means we can be so much more generous with how people name their
# tiles.
perms = {perm for i in range(len(x)) for perm in permutations(x, i)}
perms_strs = {''.join(perm) + '_' if perm else 'blank_' for perm in perms}

# Function to generate permutation strings based on provided strings
def generate_perms(*strings)
    perms = {perm for i in range(len(x) + 1) for perm in permutations(strings, i)} 
    return {''.join(perm) + '_' if perm else 'blank_' for perm in perms}
