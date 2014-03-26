from AbstractBoard import AbstractBoard,MOVES
from random import choice 
import time

try:
    import psyco
    psyco.full()
except ImportError:
    pass


def randomGame(n):
    A = AbstractBoard(4)
    A.populateRandom(2)
    isGame = True
    moves = 0
    score = 0
    while isGame:
        hasmoved = False
        while not hasmoved:
            m = choice(MOVES)
            hasmoved,scp,_ = A.shift(m)
            score+=scp
        isGame = A.populateRandom(1)
        moves+=1
    return A,moves,score

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

if __name__=="__main__":
    time.clock()
    MOVMAX = 0
    NUMMAX = 0
    SCRMAX = 0
    for i in xrange(100):    
        A,moves,score = randomGame(4)
        MOVMAX = max(moves,MOVMAX)
        NUMMAX = max(NUMMAX,max(i for i in A.enumerateBoard()))
        SCRMAX = max(SCRMAX,score)
    print MOVMAX
    print NUMMAX
    print SCRMAX
    print time.clock()
