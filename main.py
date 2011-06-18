#!/usr/bin/env python2

import pygame
from pygame.locals import *

background_color = 80, 80, 80

def main():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		screen.fill( background_color )
		pygame.display.flip()

if __name__ == '__main__':
	main()
