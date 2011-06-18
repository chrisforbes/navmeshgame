#!/usr/bin/env python2

import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_e, K_TAB
from pygame.font import Font

from level import Level
from dude import Dude

background_color = 80, 80, 80

def do_edit_action( level, event ):
    (x,y) = event.pos
    if event.button == 0:
        pass
    if event.button == 1:
        level.del_vertex( x, y )

def main():
    pygame.init()
    edit_mode = False
    screen = pygame.display.set_mode((800, 600))
    font = Font(None, 24)
    text = font.render("Edit Mode", 1, (255,255,255))

    level = Level()
    groups = [
        [   Dude( 250, 250, 0 ), Dude( 275, 250, 0 ),
            Dude( 250, 275, 0 ), Dude( 275, 275, 0 ) ],
        [   Dude( 500, 250, 0 ), Dude( 525, 250, 0 ),
            Dude( 500, 275, 0 ), Dude( 525, 275, 0 ) ]
    ]

    selectedGroup = 0

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
                do_edit_action( level, event )

        screen.fill( background_color )
        if edit_mode:
            screen.blit(text, text.get_rect())

        # draw
        level.draw( screen )
        for index,group in enumerate(groups):
            for dude in group:
                sel_level = 0
                if selectedGroup == index:
                    sel_level = 2
                dude.draw( screen, 0.3, sel_level )

        pygame.display.flip()

if __name__ == '__main__':
    main()
