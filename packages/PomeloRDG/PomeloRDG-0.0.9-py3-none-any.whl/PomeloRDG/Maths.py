def fac(x):
    res = 1
    for i in range(1, x + 1):
        res *= i
    return res

def a(n, m):
    return fac(n) // fac(n - m)

def c(n, m):
    m = min(m, n - m)
    return a(n, m) // a(m, m)

def gcd(a, b):
    return a if not b else gcd(b, a % b)

def lcm(a, b):
    return a * b // gcd(a, b)

def exgcd(a, b):
    x,  y,  s,  t = 1, 0, 0, 1
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x, s = s, x - q * s
        y, t = t, y - q * t
    return (x, y, a)

def sqrt(x):
    err, cur = 1e-6, x
    while abs(x - cur * cur) > err:
        cur = (cur + x / cur) / 2
    return cur

def fib(n):
    if n < 2:
        return n
    x, y = fib((n >> 1) - 1), fib(n >> 1)
    if n & 0x1:
        x += y
        return x * x + y * y
    else:
        return y * (y + 2 * x)
    
def ispri(x):
    if not x or x == 1:
        return False
    if x == 2:
        return True
    for i in range(3, int(sqrt(x)) + 1):
        if not x % i:
            return False
    return True

def lsieve(n):
    cnt, st, pri = 0, [True] * (n + 1), [0] * (n + 1)
    st[0] = st[1] = False
    for i in range(2, n + 1):
        if st[i]:
            pri[cnt] = i
            cnt += 1
        for j in range(cnt):
            if pri[j] * i > n: 
                break
            st[pri[j] * i] = False
            if not i % pri[j]: 
                break
    return st[0:]

def getpri(n):
    st, pri = lsieve(n), []
    for i in range(n + 1):
        if st[i]:
            pri.append(i)
    return pri

def factor(x):
    st = lsieve(x)
    faclst = []
    for i in range(2, int(sqrt(x)) + 1):
        if not st[i]:
            continue
        cnt = 0
        while not x % i:
            cnt += 1
            x /= i
        if cnt:
            faclst.append((i, cnt))
    if x > 1:
        faclst.append((x, 1))
    return faclst

def catalan(n):
    x = y = 1
    for i in range(2, n + 1):
        x, y = (x * (n + i), y * i)
    return x // y

def phi(x):
    if x == 1:
        return 1
    factors = factor(x)
    ans = x
    for pri in factors:
        ans = int(ans / pri[0] * (pri[0] - 1))
    return ans

def miu(x):
    if x == 1:
        return 1
    factors = factor(x)
    for pri in factors:
        if pri[1] > 1:
            return 0
    return 1 - (len(factors) and 1) * 2

def dectob(n, base):
    convertString = "0123456789ABCDEF"
    if n < base:
        return convertString[n]
    else:
        return dectob(n // base, base) + convertString[n % base]