from random import randint,choice,random
from math import log
import time

MOVES = [(0,-1),(0,1),(-1,0),(1,0)]
KEYS = {(-1,0):"{LEFT}",(1,0):"{RIGHT}",(0,-1):"{UP}",(0,1):"{DOWN}"}

class AbstractBoard:
    def __init__(self,n=4):
        self.B = [[None for i in xrange(n)] for j in xrange(n)]
        self.n = n
    
    def emptyBoard(self):
        #return list of empty entries
        return [(a,b) for a in xrange(self.n) for b in xrange(self.n) if self.B[a][b] is None]
    
    def populateRandom(self,m=1):
        #put 2 or 4 at random and return whether board is full
        B = self.emptyBoard()
        if B==[]:
            return False
        for i in xrange(m):
            a,b = choice(B)
            self.B[a][b] = 4 if randint(1,10)==1 else 2
            B.remove((a,b))
        return True
    
    def enumerateBoard(self):
        for a in xrange(self.n):
            for b in xrange(self.n):
                yield self.B[a][b]
    
    def shift(self,(d0,d1),verb = False):
        count = 0
        moved = False
        
        if d0==0:
            A_ = range(4)[::-d1]
            for b in xrange(4):
                merge = False
                if d1==1:
                    ind = 4
                else:
                    ind = -1
                
                for a in A_:
                    if self.B[a][b] is None:
                        continue
                    if merge and self.B[a][b]==self.B[ind][b]:
                        self.B[ind][b]*=2
                        count+=self.B[ind][b]
                        self.B[a][b] = None
                        merge = False
                        moved = True
                    else:
                        ind-=d1
                        if ind!=a:
                            self.B[ind][b] = self.B[a][b]
                            self.B[a][b] = None
                            moved = True
                        merge = True
        else:
            B_ = range(4)[::-d0]
            for a in xrange(4):
                merge = False
                if d0==1:
                    ind = 4
                else:
                    ind = -1
                for b in B_:
                    if self.B[a][b] is None:
                        continue
                    if merge and self.B[a][b]==self.B[a][ind]:
                        self.B[a][ind]*=2
                        count+=self.B[a][ind]
                        self.B[a][b] = None
                        merge = False
                        moved = True
                    else:
                        ind-=d0
                        if ind!=b:
                            self.B[a][ind] = self.B[a][b]
                            self.B[a][b] = None
                            moved = True
                        merge = True
        return moved,count

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
            hasmoved,scp = A.shift(m)
            score+=scp
            if hasmoved:
                break
            MOVE_RED.remove(m)
            if not MOVE_RED:
                for m in MOVES:
                    assert not A.shift(m)[0]
                return A,moves,score
        A.populateRandom(1)
        moves+=1

if __name__=="__main__":
    import matplotlib.pyplot as plt
    MOVSTAT = []
    NUMSTAT = []
    SCRSTAT = []
    N = 100
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

