#!/usr/bin/env python2

import pygame
from pygame.locals import QUIT
from pygame.draw import circle, line, polygon
from math import sin, cos

background_color = 80, 80, 80
dude_color = 160, 0, 0
highlight_color = 140, 80, 80
walkable_color = 0, 0, 0
screen = None

level_verts = [ (200,200), (400,200), (400,400), (200,400) ]
level_polys = [ [ 0, 1, 2, 3 ] ]

def draw_level():
    for poly in level_polys:
        actual_verts = [ level_verts[x] for x in poly ]
        polygon( screen, walkable_color, actual_verts )

def draw_dude(x, y, angle, selected):
    pointer = (x + 15 * cos(angle), y + 15 * sin(angle))

    if selected:
        circle( screen, highlight_color, (x, y), 10, 3 )
        line( screen, highlight_color, (x, y), pointer, 3 )

    circle( screen, dude_color, (x, y), 10, 1 )
    line( screen, dude_color, (x, y), pointer, 1 )

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((800, 600))
    x = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.fill( background_color )

        # animate
        x = x + 1
        if x > 100: x = 0

        # draw
        draw_level()
        draw_dude( 300 + x, 300, 0.3, True )

        pygame.display.flip()

if __name__ == '__main__':
    main()
