#!/usr/bin/env python2

import pygame
from pygame.locals import QUIT, KEYDOWN, K_e, K_TAB
from pygame.font import Font

from level import Level
from dude import Dude

background_color = 80, 80, 80

def main():
    pygame.init()
    edit_mode = False
    screen = pygame.display.set_mode((800, 600))
    font = Font(None, 24)
    text = font.render("Edit Mode", 1, (255,255,255))

    level = Level()
    group1 = [ Dude( 250, 250, 0 ), Dude( 275, 250, 0 ), Dude( 250, 275, 0 ), Dude( 275, 275, 0 ) ]
    group2 = [ Dude( 500, 250, 0 ), Dude( 525, 250, 0 ), Dude( 500, 275, 0 ), Dude( 525, 275, 0 ) ]

    selectedGroup = group1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_e:
                    edit_mode = not edit_mode
                elif event.key == K_TAB:
                    if selectedGroup == group1:
                        selectedGroup = group2
                    else:
                        selectedGroup = group1

        screen.fill( background_color )
        if edit_mode:
            screen.blit(text, text.get_rect())

        # draw
        level.draw( screen )
        for dude in group1:
            sel_level = 0
            if selectedGroup == group1:
                sel_level = 2
            dude.draw( screen, 0.3, sel_level )
        for dude in group2:
            sel_level = 0
            if selectedGroup == group2:
                sel_level = 2
            dude.draw( screen, 0.3, sel_level ) 

        pygame.display.flip()

if __name__ == '__main__':
    main()
