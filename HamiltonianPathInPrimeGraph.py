#
# This code is intended to help users of Mathematics Stack Exchange
# making experiments related to the problem stated in 
# http://math.stackexchange.com/questions/653764/how-to-either-prove-or-disprove-if-it-is-possible-to-arrange-a-series-of-numbers
#
# author: benh
# 28.01.2014, way too late at night
#

from numpy import ones
from math import sqrt
from copy import deepcopy
from random import choice

#Primes are stored up to MAX
MAX = 3000

#initialize prime sieve using numpy
p = ones(2*MAX+1,dtype = bool)
p[4::2] = p[0] = p[1] = 0
for i in xrange(3,int(sqrt(2*MAX+1))+1,2):
    p[i+i::i] = 0


def getPrimeGraph(N):
    '''Build a graph G with n vertices {1,...,n}
    where undirected edges (a,b) indicate 
    that a+b is prime. 
    Data format: neighbours in array'''
    
    G = [[] for i in xrange(N)]

    for i in xrange(1,N+1):
        for j in xrange(1,i):
            if p[i+j]:#if i+j is prime, add edge between i,j
                G[i-1].append(j-1)
                G[j-1].append(i-1)
    return G

def findHamiltonian(G,reqfirst,UPPERBOUND = 100):
    '''find Hamiltonian path
    randomized algorithm taken from 
    http://stackoverflow.com/questions/1987183/randomized-algorithm-for-finding-hamiltonian-path-in-a-directed-graph'''
    
    n = len(G)
    
    path = [[] for i in xrange(n)]
    cur = reqfirst
    c = 0
    while [] in path:
        UV = [g for g in G[cur] if not path[g]]
        if UV:
            vnxt = choice(UV)
            path[cur].append(vnxt)
            path[vnxt].append(cur)
            cur = vnxt
        else:
            vnxt = choice(G[cur])
            edge = choice(path[vnxt])
            
            path[vnxt].remove(edge)
            path[edge].remove(vnxt)
            
            path[cur].append(vnxt)
            path[vnxt].append(cur)
            
            for i in xrange(n-1,-1,-1):
                if len(path[i])==1:
                    cur = i
                    break
        c+=1
        if c>UPPERBOUND*n:#cut after too many iterations
            raise RuntimeError
    
    #reconstruct number sequence from path (paranoid version)
    PATH = [cur+1]
    oldcur = None
    for i in xrange(n-1):
        if path[cur]==[]:
            raise RuntimeError
        cur,oldcur = path[cur][0],cur
        if oldcur not in path[cur]:
            raise RuntimeError
        path[cur].remove(oldcur)
        PATH.append(cur+1)
    
    #check whether consecutive numbers sum to a prime
    for i in xrange(n-1):
        assert p[PATH[i]+PATH[i+1]]
    return PATH

def getPath(n,reqfirst = 0):
    '''rearrange the sequence (1,...,n) in a way that two consecutive 
    numbers sum to a prime'''
    G = getPrimeGraph(n)
    while True:
        try:
            a = findHamiltonian(deepcopy(G),reqfirst-1)[::-1]
            if reqfirst and a[0]==reqfirst:
                break
        except RuntimeError:
            pass
            #we all know the implementation is hacky, don't we.
    return a

for n in xrange(3,1001):
    a = getPath(n,n)
    print "for n = %d a possible sequence starting with n is"%n
    print a
