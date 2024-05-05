def bsgs(g,h,p):
    # your code here
    n = int(p**0.5) + 1
    baby = {}
    gi = 1
    for i in range(n):
        baby[gi] = i
        gi = (gi * g) % p
    
    giantstep = modpow(g, -n, p)

    hj = h
    for j in range(n):
        if hj in baby:
            # x = baby[hj] + j * n
            # print('modpow: ' + str(modpow(g, x, p)))
            return baby[hj] + j * n
        hj = (hj * giantstep) % p

    # return x

def modpow(a, n, m):
    prod = 1
    if n < 0:
        x, _ = gcdExtended(a, m)
        a = x % m
        n = -n
    while n != 0:
        if n % 2 == 1:
            prod = (prod * a) % m
            n -= 1
        n = n // 2
        a = (a ** 2) % m
    return prod

def gcdExtended(a, b):
    if a == 0:
        return 0, 1
    x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return x, y
