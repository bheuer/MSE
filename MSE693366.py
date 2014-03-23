from math import factorial

def binom(n,k):
    if not 0<=k<=n:return 0
    return factorial(n)/(factorial(n-k)*factorial(k))

cache = {}
def A(N,M,L,K):
    if (N,M,L,K) in cache:
        return cache[N,M,L,K]
    if N==0:
        if L==0 and K==0:return 1
        else:return 0
    s = 0
    for k in xrange(K+1):
        for l in xrange(k+1):
            l1 = (K-k-(L-l))
            l2 = (K-k+L-l)
            if l1>=0 and l2>=0:
                s+=A(N-1,M,l,k)*binom(2*l,l1)*binom(M-2*l,l2)
    cache[N,M,L,K] = s
    return s
    
print A(10,10,0,10)
