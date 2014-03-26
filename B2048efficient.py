#greedy bounded-depth 2048-AI with forced bias towards large merge
#bheuer, 19.03.2014

from AbstractBoard import *
import ImageGrab
import win32com.client
import win32con
import win32api
import time

try:
    import psyco
    psyco.full()
except ImportError:
    pass


#GLOBALS
COLORMAP = {(204, 192, 179):None, (238, 228, 218):2, (237, 224, 200):4, (223, 212, 201):4,(242, 177, 121):8,(245, 149, 99):16,(246, 124, 95):32,(246, 94, 59):64,(237, 207, 114):128,(204, 191, 178):128,(237, 204, 97):256,(237, 200, 80):512,(237, 197, 63):1024,(237, 194, 46):2048}
NEWCOLOR = (143, 122, 102)
GRIDCOLOR = (187, 173, 160)
DEPTHS = {}
DEPTHS["unreasonable"]  = [2]*17
DEPTHS["fast"]          = [2]*7+[3]*5+[4]*5
DEPTHS["effective"]     = [2]*6+[3]*3+[4]*4+[5]*4
DEPTHS["thorough"]      = [3]*4+[4]*9+[5]*4
#Dimensions of cell:
#106,15;121


shell = win32com.client.Dispatch("WScript.Shell")

class AutomaticBoard(AbstractBoard):
    def __init__(self,*args,**kwargs):
        AbstractBoard.__init__(self,*args)
        if "profile" in kwargs:
            self.profile = kwargs["profile"]
        else:
            self.profile = "flexible"
        if self.profile=="flexible":  
            self.Depth = DEPTHS["unreasonable"]
        else:
            self.Depth = DEPTHS[self.profile]
        self.Observed = []
        print "##############################"
        print "# Welcome to Ben's 2048 AI :)#"
        print "# Just open the 2048, make   #"
        print "#sure that the whole grid is #"
        print "#visible and watch the AI.   #"
        print "##############################"
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
        EvC,m = self.BredthSearchOptimizeMean(d)
        if m is None:
            return
        print "Apply Move",KEYS[m][1:-1]
        if not self.updateBoard(confirm=True):
            print("wait, confirm...")
            
            self.printBoard()
            return
        self.move(m,AUTO=True)
        self.printBoard()
        print "depth are ",self.Depth
        print "current Energy is:", EvC
        print "in Move          :", self.moves
        if EvC==float("infinity"):
            print "sorry, there is nothing I can do for you anymore"
            
    def firstObserve(self,b):
        print "first observation of",b
        self.Observed.append(b)
        if self.profile == "flexible" and b>=512:
            self.Depth = DEPTHS[{512:"fast",1024:"effective",2048:"thorough"}[b]]
    
    def move(self,m,AUTO = True):
        
        if AUTO:
            shell.SendKeys(KEYS[m])
            time.sleep(0.3)
            _,_,mis = self.shift(m,verb = True)
            c = 0
            while not self.updateBoard(ensure = True):
                c+=1
                if c==1:
                    print "################################################################"
                    print "#                                                              #"
                    print "#  please focus 2048-window, keyboard does not work otherwise  #"
                    print "#                                                              #"
                    print "################################################################"
                shell.SendKeys(KEYS[m])
                time.sleep(0.2)
        else:
            s,c,mis = self.shift(m)
            if not s:
                self.isGame = False
                return
            a,b = choice(self.margin())
            if randint(1,8)!=1:
                self.set(a,b,2)
            else:
                self.set(a,b,4)
        self.moves+=1
        if mis:
            self.updateMission()
    
    def solve(self,AUTO = True):
        if AUTO:
            self.updatePosition()
            self.updateBoard()
            self.updateMission()
            self.printBoard()
        else:
            self.populate()
        print("initialized Game")
        
        while self.isGame:
            self.AutoMove()

if __name__ == "__main__":
    #choose profile: "unreasonable", "fast", "effective", "thorough", "flexible"
    B = AutomaticBoard(4,profile = "fast")
    B.solve(AUTO = True)
    #A = AbstractBoard(4)
    
