#!/usr/bin/env python2

import pygame
from pygame.locals import QUIT
from pygame.draw import circle, line
from math import sin, cos

background_color = 80, 80, 80
dude_color = 160, 0, 0
screen = None

def draw_dude(x, y, angle):
	circle( screen, dude_color, (x, y), 10, 1 )
	line( screen, dude_color, (x, y),
		(x + 15 * cos(angle), y + 15 * sin(angle)), 1 )

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

		x = x + 1
		if x > 100: x = 0
		draw_dude( 300 + x, 300, 0.3 )

		pygame.display.flip()

if __name__ == '__main__':
	main()
