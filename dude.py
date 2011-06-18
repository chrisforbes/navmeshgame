from math import sin, cos
from pygame.draw import circle, line

dude_types = [ 
    { 'normal_color': (160, 0, 0), 'sel_color': (140, 80, 80) }
]

class Dude:
    def __init__( self, screen, x, y, t ):
        self.screen = screen
        self.x = x
        self.y = y
        self.t = t

    def draw( self, angle, selected):
        p = ( self.x, self.y )
        q = ( self.x + 15 * cos(angle), self.y + 15 * sin(angle) )

        if selected:
            sel_color = dude_types[ self.t ][ 'sel_color' ]
            circle( self.screen, sel_color, p, 10, 3 )
            line( self.screen, sel_color, p, q, 3 )

        normal_color = dude_types[ self.t ][ 'normal_color' ]
        circle( self.screen, normal_color, p, 10, 1 )
        line( self.screen, normal_color, p, q, 1 )
