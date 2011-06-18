from math import sin, cos
from pygame.draw import circle, line

dude_types = [ 
    { 'normal_color': (160, 0, 0), 'sel_color': (140, 80, 80) }
]

class Dude:
    def __init__( self, x, y, t ):
        self.x = x
        self.y = y
        self.t = t

    def draw( self, screen, angle, selected):
        p = ( self.x, self.y )
        q = ( self.x + 15 * cos(angle), self.y + 15 * sin(angle) )

        if selected:
            sel_color = dude_types[ self.t ][ 'sel_color' ]
            circle( screen, sel_color, p, 10, 3 )
            line( screen, sel_color, p, q, 3 )

        normal_color = dude_types[ self.t ][ 'normal_color' ]
        circle( screen, normal_color, p, 10, 1 )
        line( screen, normal_color, p, q, 1 )
