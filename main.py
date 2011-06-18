#!/usr/bin/env python2

import pygame
from pygame.locals import *

def main():
	pygame.init()
	pygame.display.set_mode((800,600))

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		pygame.display.flip()

if __name__ == '__main__':
	main()
