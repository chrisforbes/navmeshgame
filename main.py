#!/usr/bin/env python2

import pygame
from pygame.locals import (QUIT, KEYDOWN,
    MOUSEBUTTONDOWN, MOUSEMOTION,
    K_e, K_TAB, K_s, K_l, K_a, K_d, K_w)
from pygame.draw import circle, line

from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D 

from level import Level
from dude import Dude
from vecutils import *
from glcircle import GLSolidCircle, GLCircle
import meshutils
import editorutils

background_color = 0.2, 0.2, 0.2, 1.0
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
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height), pygame.OPENGL|pygame.DOUBLEBUF)
    vertex_circle = GLSolidCircle(4)
    fp_circle = GLCircle(10)
    marker_circle = GLSolidCircle(3)

    glClearColor(*background_color)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, width, height, 0.0)

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
    	global poly
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_e:
                    edit_mode = not edit_mode
                    if poly != None and len(level.polys[poly]) < 3:
                    	level.del_poly(poly)
                    	poly = None

                elif event.key == K_TAB:
                    sel_group = (sel_group + 1) % len(groups)
                    # don't let the dindex point to an invalid dude.
                    sel_dude = validate_sel_dude( sel_dude, 0 )

                elif edit_mode:
                    if event.key == K_s:
                        level.save_file( 'level.dat' )
                    if event.key == K_l:
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
                elif event.button == 1:
                    for dude in groups[sel_group]['dudes']:
                        dude.issue_orders()
            if event.type == MOUSEMOTION:
                mx, my = event.pos

        if edit_mode:
            pass
            #screen.blit(text, text.get_rect())

        # draw
        level.draw( screen, edit_mode )
        for index,group in enumerate(groups):
            for dindex, dude in enumerate(group['dudes']):
                sel_level = 0
                if sel_group == index:
                    sel_level = 2 if dindex == sel_dude else 1
                dude.draw( screen, sel_level )

        if edit_mode:
        	level.draw_vertex_circle( mx, my , vertex_circle)
        	level.draw_poly_vertex( poly, marker_circle )
        	level.draw_guide_line( poly, mx, my )
            	
        else:
            # show movement plan
            # todo: get this crap out of the renderer
            fp = level.get_firing_position_near( mx, my )
            if fp != None:
                for i, dude in enumerate(groups[sel_group]['dudes']):
                    f = intvec( get_position_for( fp, i ) )
                    color = (0.78, 0.59, 0.0) if i == 0 else (0.43, 0.27, 0.0)
                    fp_circle.draw( f, color )
                    path = level.get_path( dude.pos, f )
                    dude.set_possible_orders( path )
                    draw_path( path )
            else:
                for dude in groups[sel_group]['dudes']:
                    dude.set_possible_orders( None )

        pygame.display.flip()

FORMATION_SPACING = 25
def get_position_for( fp, n ):
    fx, fy = fp['pos']
    tx, ty = fp['tangent']
    if fp['t'] > 0.5:
        tx, ty = -tx, -ty
    return (fx + FORMATION_SPACING * n * tx,
            fy + FORMATION_SPACING * n * ty)

def draw_path( path ):
    glBegin(GL_LINES)
    q = path[0]
    for p in path[1:]:
        glColor(0.78, 0.59, 0)
        glVertex2f(*q)
        glVertex2f(*p)
    glEnd()

if __name__ == '__main__':
    main()
