#!/usr/bin/env python2

import pygame
from pygame.locals import (QUIT, KEYDOWN,
    MOUSEBUTTONDOWN, MOUSEMOTION, K_e, K_TAB, K_s, K_l)
from pygame.font import Font
from pygame.draw import circle

from level import Level
from dude import Dude

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

    selectedGroup = 0
    mx, my = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_e:
                    edit_mode = not edit_mode
                elif event.key == K_TAB:
                    if selectedGroup == len(groups) - 1:
                        selectedGroup = 0
                    else:
                        selectedGroup = selectedGroup + 1
                elif event.key == K_s and edit_mode:
                    level.save_file('level.dat')
                elif event.key == K_l and edit_mode:
                    global poly
                    poly = None
                    level.load_file('level.dat')
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
            for dude in group['dudes']:
                sel_level = 0
                if selectedGroup == index:
                    sel_level = 2
                dude.draw( screen, 0.3, sel_level )

        if edit_mode:
            v = level.vertex_at( mx, my )
            if v != None:
                circle( screen, (0,0,255), level.verts[v], 4, 0 )
        else:
            fx, fy = level.get_firing_position_near( mx, my )
            fx, fy = int(fx), int(fy)
            circle( screen, (200, 150, 0), (fx, fy), 10, 1 )

        pygame.display.flip()

if __name__ == '__main__':
    main()
