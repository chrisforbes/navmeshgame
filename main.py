#!/usr/bin/env python2

import pygame
from pygame.locals import (QUIT, KEYDOWN,
    MOUSEBUTTONDOWN, MOUSEMOTION, K_e, K_TAB)
from pygame.font import Font
from pygame.draw import circle

from level import Level
from dude import Dude

background_color = 80, 80, 80
poly = None

def do_edit_action( level, event ):
    global poly
    (x,y) = event.pos
    print event.button

    if event.button == 1:
        v = level.vertex_at( x, y ) or level.new_vertex( x, y )
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
        [   Dude( 250, 250, 1 ), Dude( 275, 250, 1 ),
            Dude( 250, 275, 1 ), Dude( 275, 275, 1 ) ],
        [   Dude( 500, 250, 0 ), Dude( 525, 250, 0 ),
            Dude( 500, 275, 0 ), Dude( 525, 275, 0 ) ]
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
            for dude in group:
                sel_level = 0
                if selectedGroup == index:
                    sel_level = 2
                dude.draw( screen, 0.3, sel_level )

        if edit_mode:
            v = level.vertex_at( mx, my )
            if v != None:
                circle( screen, (0,0,255), level.verts[v], 4, 0 )

        pygame.display.flip()

if __name__ == '__main__':
    main()
