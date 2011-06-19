#!/usr/bin/env python2

import pygame
from pygame.locals import (QUIT, KEYDOWN,
    MOUSEBUTTONDOWN, MOUSEMOTION,
    K_e, K_TAB, K_s, K_l, K_a, K_d, K_w)
from pygame.font import Font
from pygame.draw import circle, line

from level import Level
from dude import Dude
import meshutils

background_color = 80, 80, 80
poly = None

def snap(x):
    return (x+7) & ~15

def do_edit_action( level, event ):
    global poly
    x, y = event.pos
    print event.button

    if event.button == 1:
        v = level.vertex_at( x, y ) or level.new_vertex( snap(x), snap(y) )
        if poly == None:
            poly = level.new_poly( v )
        elif level.add_to_poly( poly, v ):
            poly = None

    if event.button == 3:
        if poly != None:
            level.del_poly( poly )
            poly = None
        else:
            v = level.vertex_at( x, y )
            if v != None:
                level.del_vertex( v )

def main():
    pygame.init()
    edit_mode = False
    screen = pygame.display.set_mode((800, 600))
    font = Font(None, 24)
    text = font.render("Edit Mode", 1, (255,255,255))

    level = Level()
    groups = [
        { 'dudes': [Dude( 250, 250, 1 ), Dude( 275, 250, 1 ),
                    Dude( 250, 275, 1 ), Dude( 275, 275, 1 ) ]},
        { 'dudes': [Dude( 500, 250, 0 ), Dude( 525, 250, 0 ),
                    Dude( 500, 275, 0 ), Dude( 525, 275, 0 ) ]},
    ]

    sel_group = 0
    sel_dude = 0
    mx, my = 0, 0

    def validate_sel_dude(x,z):
        n = len( groups[ sel_group ][ 'dudes' ] )
        return x if x < n else z

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_e:
                    edit_mode = not edit_mode

                elif event.key == K_TAB:
                    sel_group = (sel_group + 1) % len(groups)
                    # don't let the dindex point to an invalid dude.
                    sel_dude = validate_sel_dude( sel_dude, 0 )

                elif edit_mode:
                    if event.key == K_s:
                        level.save_file( 'level.dat' )
                    if event.key == K_l:
                        global poly
                        poly = None
                        level.load_file('level.dat')

                elif event.key == K_w:
                    sel_dude = validate_sel_dude( 0, sel_dude )
                elif event.key == K_a:
                    sel_dude = validate_sel_dude( 1, sel_dude )
                elif event.key == K_s:
                    sel_dude = validate_sel_dude( 2, sel_dude )
                elif event.key == K_d:
                    sel_dude = validate_sel_dude( 3, sel_dude )

            if event.type == MOUSEBUTTONDOWN:
                if edit_mode:
                    do_edit_action( level, event )
            if event.type == MOUSEMOTION:
                mx, my = event.pos

        screen.fill( background_color )
        if edit_mode:
            screen.blit(text, text.get_rect())

        # draw
        level.draw( screen, edit_mode )
        for index,group in enumerate(groups):
            for dindex, dude in enumerate(group['dudes']):
                sel_level = 0
                if sel_group == index:
                    sel_level = 2 if dindex == sel_dude else 1
                dude.draw( screen, sel_level )

        if edit_mode:
            v = level.vertex_at( mx, my )
            if v != None:
                circle( screen, (0,0,255), level.verts[v], 4, 0 )
        else:
            # show movement plan
            fp = level.get_firing_position_near( mx, my )
            if fp != None:
                fx, fy = int(fp['pos'][0]), int(fp['pos'][1])
                circle( screen, (200, 150, 0), (fx, fy), 10, 1 )

                path = level.get_path( (300,300), (fx,fy) )
                draw_path( screen, path )

        pygame.display.flip()

def draw_path( screen, path ):
    q = path[0]
    for p in path[1:]:
        line( screen, (200,150,0), q, p, 1 )

if __name__ == '__main__':
    main()
