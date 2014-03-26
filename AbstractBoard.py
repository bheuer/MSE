from math import log,sqrt
from random import randint,choice

#GLOBALS

MOVES = [(0,-1),(0,1),(-1,0),(1,0)]
KEYS = {(-1,0):"{LEFT}",(1,0):"{RIGHT}",(0,-1):"{UP}",(0,1):"{DOWN}"}

class AbstractBoard:
    def __init__(self,n=4):
        self.B = [[None for i in xrange(n)] for j in xrange(n)]
        self.n = n
        self.c = 0
        self.moves = 0
        self.pos = (0,0)
        self.isGame = True
        self.maxobserved = 2
        self.missionmerge = 4
        self.bounty = 0
        
    def set(self,a,b,k):
        self.c+=1
        self.B[a][b] = k
        self.maxobserved = max(self.maxobserved,k)
    
    def emptyBoard(self):
        return [(a,b) for a in xrange(self.n) for b in xrange(self.n) if self.B[a][b] is None]
    
    def populateRandom(self,m=1):
        #put 2 or 4 at random and return whether board is full
        B = self.emptyBoard()
        for i in xrange(m):
            a,b = choice(B)
            if randint(1,10)==1:
                self.set(a,b,4)
            else:
                self.set(a,b,2)
            B.remove((a,b))
        return (B!=[])
    
    def enumerateMargin(self):
        for a in xrange(self.n):
            for b in xrange(self.n):
                if self.B[a][b] is None:
                    yield a,b
    
    def enumerateBoard(self):
        for a in xrange(self.n):
            for b in xrange(self.n):
                yield self.B[a][b]
    
    def updateMission(self):
        m = m_ = self.maxobserved
        
        while True:
            c = sum(1 if b==m else 0 for b in self.enumerateBoard())
            if c>1 or m==2:break
            m/=2
        m*=2
        
        self.missionmerge = m
        self.bounty = log(m_,2)*log(m,2)*0.1-1
    
    def shift(self,(d0,d1),verb = False):
        count = 0
        moved = False
        mission = False
        
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
                        if self.B[ind][b]==self.missionmerge:
                            mission = True
                        self.B[a][b] = None
                        self.c-=1
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
                        if self.B[a][ind]==self.missionmerge:
                            mission = True
                        self.B[a][b] = None
                        self.c-=1
                        merge = False
                        moved = True
                    else:
                        ind-=d0
                        if ind!=b:
                            self.B[a][ind] = self.B[a][b]
                            self.B[a][b] = None
                            moved = True
                        merge = True
        if mission:
            self.updateMission()
            if verb:
                print "###################"
                print "new Mission is merge of", self.missionmerge
                print "bounty is",self.bounty
                print "###################"
        return moved,count,mission
    
    def margin(self):
        return [i for i in self.enumerateMargin()]
        
    def deepcopy(self):
        selfcopy = AbstractBoard()
        selfcopy.B = [b[:] for b in self.B]
        selfcopy.n = self.n
        selfcopy.c = self.c
        return selfcopy
    
    def BredthSearchOptimizeMean(self,depth = 4,new = False):
        bestEvC = 100# punish gambling!
        bestm = []
        for m in MOVES:
            B = self.deepcopy()
            moved,count,mis = B.shift(m)
            if not moved:
                continue
            if depth>1:
                c_ = 0
                cumEvC = 0.0
                for a,b in B.enumerateMargin():
                    
                    B_ = B.deepcopy()
                    B_.set(a,b,2)
                    cumEvC += 7*B_.BredthSearchOptimizeMean(depth-1)[0]
                    
                    B_ = B.deepcopy()
                    B_.set(a,b,4)
                    cumEvC += B_.BredthSearchOptimizeMean(depth-1)[0]
                    c_+=1
                        
                if c_ == 0:
                    EvC = 100
                else:
                    EvC = cumEvC/(8.0*c_)-(log(1+count,2))*0.5
                    
            else:
                EvC = B.c
                EvC-=log(count+1,2)*0.5
            if mis:
                EvC-=self.bounty
            
            if bestEvC>=EvC:
                if bestEvC==EvC:
                    bestm.append(m)
                else:
                    bestEvC = EvC
                    bestm = [m]
        if not bestm:
            return bestEvC,None
        return bestEvC,choice(bestm)
    
    def BredthSearchOptimizeMax(self,depth = 4):
        bestEvC = float("infinity")
        bestm = []
        for m in MOVES:
            B = self.deepcopy()
            moved,count,mis = B.shift(m)
            if not moved:
                continue
            if depth>1:
                c_ = 0
                cumEvC = 0.0
                for a,b in B.enumerateMargin():
                    
                    B_ = B.deepcopy()
                    B_.set(a,b,2)
                    cumEvC = max((cumEvC,B_.BredthSearchOptimizeMax(depth-1)[0])-log(1+count,2)*0.5)
                    if cumEvC>bestEvC:
                        continue
                        
                if c_ == 0:
                    EvC = float("infinity")
                else:
                    EvC = cumEvC
            else:
                EvC = B.c
                EvC-=log(count+1,2)*0.5
            if bestEvC>=EvC:
                if bestEvC==EvC:
                    bestm.append(m)
                else:
                    bestEvC = EvC
                    bestm = [m]
        if not bestm:
            isGame = False
            return bestEvC,None
        return bestEvC,choice(bestm)
    
    def printBoard(self):
        print "board with ",self.c,"entries"
        maxs = max(len(str(self.B[a][b])) if self.B[a][b] else 1 for a in xrange(4) for b in xrange(4))
        blank = " "*maxs
        print "_"*((maxs+3)*self.n)
        for a in xrange(4):
            for b in xrange(4):
                print "|",
                if self.B[a][b] is None:
                    print blank,
                else:
                    s = str(self.B[a][b])
                    s+=" "*(maxs-len(s))
                    print s,
            print "|"
        print "_"*((maxs+3)*self.n)
