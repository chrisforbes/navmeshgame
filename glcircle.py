from OpenGL.GL import *
from math import sin, cos

class GLCircle():
    def __init__(self, radius):
        self.displaylist = glGenLists(1)
        glNewList(self.displaylist, GL_COMPILE)
        glBegin(GL_LINE_STRIP)
        for angle in xrange(360):
            glVertex2f(sin(angle) * radius, cos(angle) * radius)
        glEnd()
        glEndList()

    def draw(self, pos, color):
        glTranslatef(pos[0], pos[1], 0)
        glColor(*color)
        glCallList(self.displaylist)
        glLoadIdentity()
        
class GLSolidCircle(GLCircle):
    def __init__(self, radius):
        self.displaylist = glGenLists(1)
        glNewList(self.displaylist, GL_COMPILE)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for angle in xrange(72):
            glVertex2f(sin(angle * 5) * radius, cos(angle * 5) * radius)
        glEnd()
        glEndList()

