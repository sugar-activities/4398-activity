# tra.py
import g,random,utils,pygame

squares=[] # 10x10= 8x8 surrounded by border to assist legal checking
piles=[0,0,0,0,0,0,0,0,0,0] # eg piles[2]= number of tiles left in pile 2

class Square:
    def __init__(self,ind,r,c,x,y):
        self.ind=ind; self.r=r; self.c=c; self.x=x; self.y=y
        self.value=0 # 0...9
        self.piece=0 #0...9
        self.cxy=utils.top_left_to_centre(g.tile_imgs[1],(x,y))

class Board:
    def __init__(self):
        d=g.sy(.32)
        y=g.y0+d; ind=0
        for r in range(10):
            x=g.x0+d
            for c in range(10):
                sq=Square(ind,r,c,x,y)
                squares.append(sq)
                ind+=1
                if c>0: x+=g.dx
            if r>0: y+=g.dy

    def setup(self):
        for sq in squares: sq.piece=0; sq.value=0
        self.deal()
        for i in range(1,10): piles[i]=8
        self.carry=0; self.first=True; g.score=0; g.glow_ms=None; g.red_ms=None
        self.clashes=[]

    def deal(self): # total 110-130
        n=0; total=0
        for sq in squares: sq.value=0
        for i in range(10000):
            rnd=random.randint(1,98); sq=squares[rnd]
            if sq.value==0:
                if sq.r>0 and sq.r<9 and sq.c>0 and sq.c<9:
                    v=random.randint(1,9)
                    if n==23: # last tile
                        if total<101 or total>121:
                            n=0; total=0 # start again
                            for sq1 in squares: sq1.value=0
                        else:
                            for j in range(1000):
                                t=total+v
                                if t>109 and t<131: break
                                v=random.randint(1,9)
                    sq.value=v; n+=1; total+=v
                    if n==24: break
        #print total,###
                    
    def reset(self):
        for sq in squares: sq.piece=0
        for i in range(1,10): piles[i]=8
        self.carry=0; self.first=True; g.score=0; g.glow_ms=None; g.red_ms=None

    def draw(self):
        g.screen.blit(g.grid,(g.x0,g.y0))
        for sq in squares:
            if sq.piece>0:
                g.screen.blit(g.tile_imgs[sq.piece],(sq.x,sq.y))
            elif sq.value>0:
                g.screen.blit(g.tile_imgs_pale[sq.value],(sq.x,sq.y))
        y=g.y1
        for r in range(1,10):
            x=g.x1
            for c in range(1,piles[r]+1):
                g.screen.blit(g.tile_imgs[r],(x,y))
                x+=g.dx1
            y+=g.dy1
        if self.carry>0:
            mx,my=pygame.mouse.get_pos()
            utils.centre_blit(g.screen,g.shadow,(mx,my))
            utils.centre_blit(g.screen,g.tile_imgs[self.carry],(mx,my))
            if g.red_ms<>None:
                utils.centre_blit(g.screen,g.red,(mx,my))
                for sq in self.clashes:
                    utils.centre_blit(g.screen,g.red,sq.cxy)
        if g.glow_ms<>None:
            utils.centre_blit(g.screen,g.glow,g.glow_cxy)

    def click(self):
        if self.carry==0:
            n=self.which_pile()
            if n>0:
                piles[n]-=1; self.carry=n
        else:
            sq=self.which_square()
            if sq==None:
                piles[self.carry]+=1; self.carry=0
            else:
                if self.ok(sq,self.carry):
                    if sq.value==self.carry:
                        g.score+=sq.value
                        g.glow_ms=-1; g.glow_cxy=(sq.x+g.d/2,sq.y+g.d/2)
                    sq.piece=self.carry; self.carry=0
                else:
                    g.red_ms=-1

    def key(self,n):
        if self.carry==0:
            if piles[n]>0: piles[n]-=1; self.carry=n
        else:
            if n==self.carry:
                piles[n]+=1; self.carry=0
            else:
                if piles[n]>0:
                    piles[self.carry]+=1; piles[n]-=1; self.carry=n
            
    def ok(self,sq,v): # ok to put piece v on square sq?
        if self.first: self.first=False; return True # anywhere for 1st tile
        if sq.piece>0: return False # sq occupied
        ind=sq.ind; mates=0; self.clashes=[]
        # left mate
        vm=squares[ind-1].piece
        if vm>0:
            if (v==vm) or (v==(vm+1)) or (vm==9 and v==1): mates+=1
            else: self.clashes.append(squares[ind-1])
        # right mate
        vm=squares[ind+1].piece
        if vm>0:
            if (v==vm) or (v==(vm-1)) or (vm==1 and v==9): mates+=1
            else: self.clashes.append(squares[ind+1])
        # above mate
        vm=squares[ind-10].piece
        if vm>0:
            if (v==vm) or (v==(vm+1)) or (vm==9 and v==1): mates+=1
            else: self.clashes.append(squares[ind-10])
        # below mate
        vm=squares[ind+10].piece
        if vm>0:
            if (v==vm) or (v==(vm-1)) or (vm==1 and v==9): mates+=1
            else: self.clashes.append(squares[ind+10])
        if mates==0: return False # not linked
        if len(self.clashes)==0: return True
        return False

    def which_pile(self):
        y=g.y1
        for r in range(1,10):
            x=g.x1
            for c in range(1,piles[r]+1):
                if c==piles[r]:
                    if utils.mouse_in(x,y,x+g.d,y+g.d):
                        return r
                x+=g.dx1
            y+=g.dy1
        return 0
    
    def which_square(self):
        for sq in squares:
            if sq.r>0 and sq.r<9 and sq.c>0 and sq.c<9:
                if utils.mouse_in(sq.x,sq.y,sq.x+g.d,sq.y+g.d):
                    return sq
        return None
        

                

        
