#!/usr/bin/env python2

import pygame
from pygame.locals import QUIT, KEYDOWN, K_e
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

    level = Level( screen )
    dude = Dude( screen, 300, 300, 0 )

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_e:
                    edit_mode = not edit_mode

        screen.fill( background_color )
        if edit_mode:
            screen.blit(text, text.get_rect())

        # draw
        level.draw()
        dude.draw( 0.3, True )

        pygame.display.flip()

if __name__ == '__main__':
    main()
