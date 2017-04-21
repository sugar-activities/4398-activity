# g.py - globals
import pygame,utils,random

app='Trails'; ver='1.0'
ver='1.1'
# debug right click removed
# clashing squares shown
# key 1-9 for pick up
ver='1.2'
# the total of the ghost squares is always between 110 and 130 inclusive
# cannot key pickup from empty pile
ver='1.3'
# ghost square outside grid bug fixed
ver='4.0'
# new sugar cursor etc
ver='4.1'
# o key

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(50*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    
    # this activity only
    global best,tile_imgs,tile_imgs_pale,d,grid,x0,y0,dx,dy,x1,y1,dx1,dy1
    global star,yc,score,shadow,glow,glow_ms,glow_cxy,red,red_ms
    best=0
    tile_imgs=[None]; tile_imgs_pale=[None]
    for i in range(1,10):
        img=utils.load_image(str(i)+".png"); tile_imgs.append(img)
        img=utils.load_image(str(i)+".png",True,'pale'); tile_imgs_pale.append(img)
    d=img.get_width()
    grid=utils.load_image("grid.png")
    x0=sx(14); y0=sy(1); dx=sy(2.05333); dy=dx # for grid
    x1=sx(.5); y1=sy(.5); dx1=sy(1.5); dy1=sy(2.35) # for piles
    yc=sy(19.6) # centre for buttons & scores
    star=utils.load_image("star.png",True); score=0
    shadow=utils.load_image("shadow.png",True)
    glow=utils.load_image("glow.png",True); glow_ms=None; glow_cxy=None
    red=utils.load_image("red.png",True); red_ms=None
    
def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor
