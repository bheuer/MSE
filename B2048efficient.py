#greedy bounded-depth 2048-AI with forced bias towards large merge
#bheuer, 19.03.2014

from math import log,sqrt
from random import randint,choice
import ImageGrab
import win32com.client
import time

try:
    import psyco
    psyco.full()
except ImportError:
    pass

#GLOBALS
COLORMAP = {(204, 192, 179):None, (238, 228, 218):2, (237, 224, 200):4, (223, 212, 201):4,(242, 177, 121):8,(245, 149, 99):16,(246, 124, 95):32,(246, 94, 59):64,(237, 207, 114):128,(204, 191, 178):128,(237, 204, 97):256,(237, 200, 80):512,(237, 197, 63):1024,(237, 194, 46):2048}
GRIDCOLOR = (187, 173, 160)
MOVES = [(0,-1),(0,1),(-1,0),(1,0)]
KEYS = {(-1,0):"{LEFT}",(1,0):"{RIGHT}",(0,-1):"{UP}",(0,1):"{DOWN}"}
shell = win32com.client.Dispatch("WScript.Shell")

#Dimensions of cell:
#106,15;121

class AbstractBoard:
    def __init__(self,n=4):
        self.B = [[None for i in xrange(n)] for j in xrange(n)]
        self.n = n
        self.c = 0
        self.moves = 0
        self.pos = (0,0)
        self.isGame = True
        
    def getRandomEmpty(self):
        while True:
            a,b = randint(0,self.n-1),randint(0,self.n-1)
            if self.B[a][b] is None:
                return a,b
        
    def set(self,a,b,k):
        self.c+=1
        self.B[a][b] = k
    
    def populate(self,m=2):
        for i in xrange(m):
            a,b = self.getRandomEmpty()
            self.set(a,b,2)
    
    def enumerateMargin(self):
        for a in xrange(self.n):
            for b in xrange(self.n):
                if self.B[a][b] is None:
                    yield a,b
    
    def shift(self,(d0,d1)):
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
        
        return moved,count
    
    def margin(self):
        return [i for i in self.enumerateMargin()]
                    
    def move(self,m,AUTO = True):
        
        if AUTO:
            shell.SendKeys(KEYS[m])
            time.sleep(0.2)
            
            c = 0
            while not self.updateBoard(ensure = True):
                c+=1
                if c==10:
                    print "################################################################"
                    print "#                                                              #"
                    print "#  please focus 2048-window, keyboard does not work otherwise  #"
                    print "#                                                              #"
                    print "################################################################"
                shell.SendKeys(KEYS[m])
                time.sleep(0.2)
        else:
            s,c = self.shift(m)
            if not s:
                self.isGame = False
                return
            a,b = choice(self.margin())
            if randint(1,8)!=1:
                self.set(a,b,2)
            else:
                self.set(a,b,4)
        self.moves+=1
        
        
    def deepcopy(self):
        selfcopy = AbstractBoard()
        selfcopy.B = [b[:] for b in self.B]
        selfcopy.n = self.n
        selfcopy.c = self.c
        return selfcopy
    
    def BredthSearchOptimize(self,depth = 4):
        bestEvC = float("infinity")
        bestm = [(1,0)]
        for m in MOVES:
            B = self.deepcopy()
            moved,count = B.shift(m)
            if not moved:
                continue
            if depth>1:
                c_ = 0
                cumEvC = 0.0
                for a,b in B.enumerateMargin():
                    
                    B_ = B.deepcopy()
                    B_.set(a,b,2)
                    cumEvC = max(cumEvC,B_.BredthSearchOptimize(depth-1)[0])-log(1+count,2)*0.5
                    if cumEvC>bestEvC:
                        continue
                    c_=1
                    '''if randint(1,8)==1:
                        B_ = B.deepcopy()
                        B_.set(a,b,4)
                        cumEvC += B_.BredthSearchOptimize(depth-1)[0]
                        c_=1'''
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

class AutomaticBoard(AbstractBoard):
    def __init__(self,*args,**kwargs):
        AbstractBoard.__init__(self,*args)
        if "profile" in kwargs:
            self.profile = kwargs["profile"]
        else:
            self.profile = "effective"
        self.Depth = []
        for c in xrange(17):
            if self.profile=="fast":
                if c>15:
                    d = 5
                elif c>12:
                    d = 4
                elif c>6:
                    d = 3
                else:
                    d = 2
            elif self.profile=="unreasonable":
                if c>10:
                    d = 3
                else:
                    d = 2
            elif self.profile=="effective":
                if c>12:
                    d = 5
                elif c>8:
                    d = 4
                elif c>5:
                    d = 3
                else:
                    d = 2
            else:
                if c>11:
                    d = 5
                elif c>7:
                    d = 4
                elif c>4:
                    d = 3
                else:
                    d = 2
            self.Depth.append(d)
    
    def findGrid(self):
        image = ImageGrab.grab()
        _,_,a,b = image.getbbox()
        for x in xrange(0,a,7):
            for y in xrange(0,b,7):
                if image.getpixel((x,y))==GRIDCOLOR:
                    
                    for a1 in xrange(4):
                        for b1 in xrange(4):
                            if x+121*a1+60>=a or y+121*b1+17>=b:
                                break
                            if image.getpixel((x+121*a1+60,y+121*b1+17)) not in COLORMAP:
                                break
                        else:continue
                        break
                    else:
                        return x,y
    
    def updateBoard(self,confirm = False,ensure = False):
        
        nc0 = sum(1 if (not self.B[a][b] is None) else 0 for a in xrange(self.n) for b in xrange(self.n))
        change = False
        c=0
        
        while True:
            image = ImageGrab.grab()
            for x in xrange(4):
                for y in xrange(4):
                    pix = image.getpixel((self.pos[0]+60+x*121, self.pos[1]+20+y*121))
                    if pix not in COLORMAP:
                        break
                else:continue
                break
            else:break
            c+=1
            if c==10:
                self.updatePosition()
                c = 0
        
        for x in xrange(4):
            for y in xrange(4):
                pix = image.getpixel((self.pos[0]+60+x*121, self.pos[1]+20+y*121))
                if pix not in COLORMAP:
                    print pix
                b = COLORMAP[pix]
                if b!=self.B[y][x]:
                    if confirm:
                        return False
                    if ensure:
                        change = True
                    self.set(y,x,b)
                    
        if not change and ensure:
            return False
        nc = sum(1 if (not self.B[a][b] is None) else 0 for a in xrange(self.n) for b in xrange(self.n))
        if nc==0:
            self.updateBoard()
            return True
        
        self.c = nc
        return True
    
    def updatePosition(self):
        print "update position..."
        a = None
        c= 0
        while not a:
            c+=1
            a = self.findGrid()
            if c==50:
                print "################################################################"
                print "#                                                              #"
                print "# please open the 2048-window and make the whole grid visible" #"
                print "#                                                              #"
                print "################################################################"
        self.pos = a
        print self.pos
        print "updated position"
    
    def AutoMove(self):
        self.updateBoard()
        d = self.Depth[self.c]
        print "minimize Energy with depth ",d
        EvC,m = self.BredthSearchOptimize(d)
        print "Apply Move",KEYS[m][1:-1]
        if not self.updateBoard(confirm=True):
            print("wait, confirm...")
            
            self.printBoard()
            return
        self.move(m,AUTO=True)
        self.printBoard()
        print "current Energy is:", EvC
        print "in Move          :", self.moves
        if EvC==float("infinity"):
            print "sorry, there is nothing I can do for you anymore"
            self.isGame = False
    
    def solve(self,AUTO = True):
        if AUTO:
            self.updatePosition()
            self.updateBoard()
            self.printBoard()
        else:
            self.populate()
        print("initialized Game")
        
        while self.isGame:
            self.AutoMove()

if __name__ == "__main__":
    #choose profile: "unreasonable", "fast", "effective", "thorough"
    B = AutomaticBoard(4,profile = "fast")
    B.solve(AUTO = True)
