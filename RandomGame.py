from AbstractBoard import AbstractBoard,MOVES
from random import choice,random
from itertools import cycle
from math import log
import time
'''
try:
    import psyco
    psyco.full()
except ImportError:
    pass
'''
MOVES = [(0,1),(1,0),(-1,0),(0,-1)]

def randomGame(n):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    while True:
        MOVE_RED = MOVES[:]
        while True:
            m = choice(MOVE_RED)
            hasmoved,scp,_ = A.shift(m)
            score+=scp
            if hasmoved:
                break
            MOVE_RED.remove(m)
            if not MOVE_RED:
                return A,moves,score
        A.populateRandom(1)
        moves+=1

def randomGreedyGame(n):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    while isGame:
        M = []
        msc = -1
        A_ = A.deepcopy()
        for m in MOVES:
            hasmoved,scp,_ = A.shift(m)
            if hasmoved:
                A_ = A.deepcopy()
                if scp>msc:
                    msc = scp
                    M = [(scp,m)]
                elif scp==msc:
                    M.append((scp,m))
        scp,m = choice(M)
        score+=scp
        A.shift(m)
        isGame = A.populateRandom(1)
        moves+=1
    return A,moves,score

def randomBiasGame(n,(p1,p2,p3,p4)):
    assert p1+p2+p3+p4==1
    
    def iterateBiasedMoves():
        while True:
            x = random()
            if x<p1:yield MOVES[0]
            if x<p1+p2:yield MOVES[1]
            if x<p1+p2+p3:yield MOVES[2]
            yield MOVES[3]
    
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    for m in iterateBiasedMoves():
        hasmoved,scp,_ = A.shift(m)
        if hasmoved:
            score+=scp
            moves+=1
            isGame = A.populateRandom(1)
            if not isGame:break
    return A,moves,score    

def randomPreferMoves(F):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    tested = set()
    while True:
        if len(tested)==len(F):
            m = choice([i for i in MOVES if i not in F])
            tested = set()
        else:
            m = choice(F)
            
        hasmoved,scp,_ = A.shift(m)
        if hasmoved:
            score+=scp
            moves+=1
            isGame = A.populateRandom(1)
            if not isGame:break
        else:
            tested.add(m)
    return A,moves,score    

def randomcyclePreferedMoves(F):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    c = 0
    for m in cycle(F):
        if c==len(F):
            m = choice([i for i in MOVES if i not in F])
        c+=1
        hasmoved,scp,_ = A.shift(m)
        if hasmoved:
            score+=scp
            moves+=1
            isGame = A.populateRandom(1)
            if not isGame:break
            c=0
    return A,moves,score  

def randomCycleGame(n):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    for m in cycle([(0,1),(-1,0),(0,-1),(1,0)]):
        hasmoved,scp,_ = A.shift(m)
        if hasmoved:
            score+=scp
            moves+=1
            isGame = A.populateRandom(1)
            if not isGame:break
    return A,moves,score
    
if __name__=="__main__":
    import matplotlib.pyplot as plt
    time.clock()
    MOVSTAT = []
    NUMSTAT = []
    SCRSTAT = []
    N = 100000
    for i in xrange(N):
        A,moves,score = randomGame(3)
        MOVSTAT.append(moves)
        NUMSTAT.append(max(i for i in A.enumerateBoard()))
        SCRSTAT.append(score)
        if i%1000==0:
            print i*1.0/N*100
    am = [NUMSTAT.count(2**i) for i in xrange(1,12)]
    amCum = [sum(am[i:]) for i in xrange(len(am))]
    for j,a in enumerate(am):
        print 2*2**j,a
    
    maxtilenum = tuple(str(2**i) for i in xrange(1,12))
    x_pos = range(len(maxtilenum))

    plt.bar(x_pos, am, align='center', alpha=0.4)
    plt.xticks(x_pos, maxtilenum)
    plt.ylabel('number of games')
    plt.title('highest tile number reached')

    plt.show()
    plt.hist(SCRSTAT,bins=(max(SCRSTAT)-min(SCRSTAT))/4,align = "left",edgecolor = 'none',histtype ="stepfilled")
    plt.xlabel("score")
    plt.ylabel("number of games")
    plt.title('game score reached')
    plt.show()
    0,0,0,1,330,5115,32836,54118,7595,5
    print time.clock()

