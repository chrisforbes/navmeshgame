from math import sin, cos
from pygame.draw import circle, line
from glcircle import GLCircle
from OpenGL.GL import *

dude_types = [ 
    [ (0.62, 0.0, 0.0), (0.42, 0.23, 0.23), (0.54, 0.15, 0.15) ],
    [ (0.0, 0.62, 0.0), (0.23, 0.35, 0.23), (0.15, 0.43, 0.15) ],
]

class Dude:
    def __init__( self, x, y, t, angle=0.0 ):
        self.pos = x,y
        self.t = t
        self.angle = angle
        self.dude_circle = GLCircle(10)
        self.line_list = glGenLists(1)
        self.path = []
        self.possible_path = []    

    def draw( self, screen, sel_level):
        self.dude_circle.draw(self.pos, dude_types[self.t][sel_level])
        glNewList(self.line_list, GL_COMPILE)
        glBegin(GL_LINES)
        glColor(*dude_types[self.t][sel_level])
        glVertex2f(*self.pos)
        glVertex2f(self.pos[0] + 15 * cos(self.angle), self.pos[1] + 15 * sin(self.angle))
        glEnd()
        glEndList()
        glCallList(self.line_list)

    def set_possible_orders( self, path ):
        self.possible_path = path

    def issue_orders( self ):
        if self.possible_path:
            self.path = self.possible_path
            # todo: state machine transitions
