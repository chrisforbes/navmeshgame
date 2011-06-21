
from OpenGL.GL import *

from level import Level
import meshutils

def draw_vertex_circle( self, mx, my , vertex_circle):
	v = self.vertex_at( mx, my )
	if v != None:
		vertex_circle.draw( self.verts[v], (0.0, 0.0, 1.0) )
        
def draw_poly_vertex( self, poly, marker_circle):
	if poly != None:
		marker_circle.draw(self.verts[self.polys[poly][0]], (1.0, 0.0, 0.0))
		
def draw_guide_line(self, poly, mx, my):
	if poly != None:
		v = self.verts[self.polys[poly][-1]]
		glBegin(GL_LINES)
		glColor((0.9, 0.9, 0.9))
		glVertex2f( mx , my )
		glVertex2f(*v)
		glEnd()
		
Level.draw_vertex_circle = draw_vertex_circle
Level.draw_poly_vertex = draw_poly_vertex
Level.draw_guide_line = draw_guide_line