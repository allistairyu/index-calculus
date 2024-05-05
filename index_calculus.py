from primefac import primefac
from random import randint
from sage.all import *
from collections import defaultdict 

# PARAM_P = 18443
# B = 5
# g = 37
# h = 211
PARAM_P = 941
B = 5
g = 627
h = 18

# get factor base
# https://stackoverflow.com/a/3035188
# TODO: implement sieve of eratosthenes
def primes1(n):
    """ Returns  a list of primes < n """
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

def factor_list_to_dict(factor_list):
    factor_dict = defaultdict(lambda: 0)
    for factor in factor_list:
        # if factor not in factor_dict:
        #     factor_dict[factor] = 0
        factor_dict[factor] += 1
    return factor_dict

def index_calculus(g, h, p, B, factor_base):
    # Step 1: Find a prime factor base B
    # print(factor_base)
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
    print(relations)
    print(bases)
    return bases, relations

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

def main():
    factor_base = primes1(B + 1)
    bases, relations = index_calculus(g, h, PARAM_P, B, factor_base)
    # bases = {2,3,5}
    # relations = [({2: 3, 3: 4, 5: 1}, 12708), ({2: 3, 5: 2}, 11311), ({2: 3, 3: 3, 5: 1}, 15400), ({2: 3, 3: 1, 5: 4}, 2731)]
    M, b = to_matrices(bases, relations)

    solutions = []
    factors = list(set(primefac(PARAM_P - 1))) # TODO: generalize
    for f in factors:
        solutions.append([int(i) for i in solve_matrix(M, b, f)])

    combined_solution = []
    residues = list(zip(*solutions)) # transpose

    for i in range(len(residues)):
        combined_solution.append(CRT(list(residues[i]), factors))

    print(combined_solution)
    # combined_solution = [5733,15750,6277]
    
    # TODO: check solution
    k = 0
    factors = []
    while True:
        k = randint(1, PARAM_P - 1)
        # k = 9549
        # k = 6004
        hgk = (h * pow(g, -k, PARAM_P)) % PARAM_P
        B_smooth, factors = check_B_smooth(hgk, B)
        if B_smooth:
            print('k: ' + str(k))
            print('factors: ' + str(factors))
            break
    
    factors_dict = factor_list_to_dict(factors)
    
    result = k
    for i in range(len(combined_solution)):
        result = (result + factors_dict[factor_base[i]] * combined_solution[i]) % (PARAM_P - 1)

    print(result)


if __name__ == '__main__':
    main()