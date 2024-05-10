from primefac import primefac
from random import randint
from sage.all import *
from collections import defaultdict 

B = 5
factor_base = [2, 3, 5]

# get factor base for B
# https://stackoverflow.com/a/3035188
# TODO: implement sieve of eratosthenes
def primes1(n):
    """ Returns  a list of primes <= n """
    n += 1
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]

def check_B_smooth(n, B):
    factors = list(primefac(n)) # TODO: implement primefac
    for f in factors:
        if f > B:
            return False, factors
    return True, factors

def to_matrices(bases, congruences):
    M = [[c[0][base] if base in c[0] else 0 \
            for base in bases] for c in congruences]
    b = [c[1] for c in congruences]
    return M, b

def solve_matrix(M, b, p):
    R = IntegerModRing(p)
    M = matrix(R, M)
    b = vector(R, b)
    return M.solve_right(b)

def factor_list_to_dict(factor_list):
    factor_dict = defaultdict(lambda: 0)
    for factor in factor_list:
        factor_dict[factor] += 1
    return factor_dict

def check_solution(g, factors, solution, p):
    for i in range(len(factors)):
        f = factors[i]
        s = solution[i]
        # print(f'Checking {g}^{s} = {pow(g, s, p)} = {f}')
        if pow(g, s, p) != f:
            return False
    return True

def check_dlog(g, h, x, p):
    return pow(g, x, p) == h

def compute_relations(g, p):
    relations = []
    bases = set()
    while len(relations) <= len(factor_base):
        e = randint(1, p-1)
        g_e = pow(g, e, p)
        B_smooth, factors = check_B_smooth(g_e, B)
        if B_smooth:
            factors_dict = factor_list_to_dict(factors)
            relations.append((factors_dict, e))
            for f in factors_dict.keys():
                bases.add(f)
    return list(bases), relations

def compute_small_dlogs(g, p):
    while True:
        bases, relations = compute_relations(g, p)
        M, b = to_matrices(bases, relations)
        
        solutions = []
        factors = list(set(primefac(p - 1)))
        for f in factors:
            solutions.append([int(i) for i in solve_matrix(M, b, f)])

        combined_solution = []
        residues = list(zip(*solutions))
        for i in range(len(residues)):
            combined_solution.append(CRT(list(residues[i]), factors))
        
        if check_solution(g, bases, combined_solution, p):
            break
    return combined_solution

def solve(g, h, p):
    print(f'Solving {g}^x = {h} mod {p}...')
    small_dlogs = compute_small_dlogs(g, p)
    k = 2
    factors = []
    while True:
        hgk = (h * pow(g, -k, p)) % p
        B_smooth, factors = check_B_smooth(hgk, B)
        if B_smooth:
            break
        k += 1
    
    factors_dict = factor_list_to_dict(factors)
    x = k
    for i in range(len(small_dlogs)):
        x = (x + factors_dict[factor_base[i]] * small_dlogs[i]) % (p - 1)
    if check_dlog(g, h, x, p):
        print(f'Solution found: x = {x}')
    return x

if __name__ == '__main__':
    solve(37, 211, 18443)