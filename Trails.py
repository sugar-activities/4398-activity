#!/usr/bin/python
# Trails.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,tra,pygame,utils,gtk,sys,buttons

class Trails:

    def __init__(self):
        self.best=0
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py
        self.keys={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
                   pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
                   pygame.K_9:9}

    def display(self):
        g.screen.fill(utils.BLACK)
        self.board.draw()
        utils.display_number(g.score,(g.sx(22.6),g.yc),g.font2,utils.CREAM)
        utils.centre_blit(g.screen,g.star,(g.sx(27.6),g.yc))
        utils.display_number1(g.best,(g.sx(28.6),g.yc),g.font2,utils.CREAM)
        buttons.draw()

    def do_button(self,bu):
        if bu=='new': self.board.setup()
        if bu=='reset': self.board.reset()

    def do_key(self,key):
        if key==265 or key==pygame.K_o: self.do_button('new') #circle
        if key in self.keys.keys():
            n=self.keys[key]; self.board.key(n)

    def update(self):
        if g.glow_ms<>None:
            if g.glow_ms==-1: # start glow (set in tra.py)
                g.glow_ms=pygame.time.get_ticks()
            else: # check if glow finished
                d=pygame.time.get_ticks()-g.glow_ms
                if d>800: g.glow_ms=None; g.redraw=True
        if g.red_ms<>None:
            if g.red_ms==-1: # start red (set in tra.py)
                g.red_ms=pygame.time.get_ticks()
            else: # check if red finished
                d=pygame.time.get_ticks()-g.red_ms
                if d>400: g.red_ms=None; g.redraw=True
        buttons.on('reset')
        if self.board.first: buttons.off('reset')

    def run(self):
        g.init()
        g.journal=self.journal
        if not self.journal:
            utils.load(); self.best=g.best
        else:
            g.best=self.best
        buttons.Button('reset',(g.sx(15.6),g.yc),True)
        buttons.Button('new',(g.sx(18.8),g.yc),True)
        self.board=tra.Board()
        self.board.setup()
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True
        while going:
            g.mx,g.my=pygame.mouse.get_pos()
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        g.glow_ms=None; g.red_ms=None
                        bu=buttons.check()
                        if bu!='': self.do_button(bu)
                        else: self.board.click()
                elif event.type == pygame.KEYDOWN:
                    self.do_key(event.key); g.redraw=True
            if not going: break
            self.update()
            #self.board.setup(); g.redraw=True###
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            if g.score>g.best: g.best=g.score
            self.best=g.best
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=Trails()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
