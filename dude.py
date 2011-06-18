from math import sin, cos
from pygame.draw import circle, line

dude_types = [ 
    [ (160, 0, 0), (110, 60, 60), (140, 40, 40) ],
    [ (0, 160, 0), (60, 90, 60), (40, 110, 40) ],
]

class Dude:
    def __init__( self, x, y, t, angle=0.0 ):
        self.x = x
        self.y = y
        self.t = t
        self.angle = angle

    def draw( self, screen, sel_level):
        p = ( self.x, self.y )
        q = ( self.x + 15 * cos(self.angle), self.y + 15 * sin(self.angle) )

        if sel_level > 0:
            sel_color = dude_types[ self.t ][ sel_level ]
            circle( screen, sel_color, p, 10+1, 3 )
            line( screen, sel_color, p, q, 3 )

        normal_color = dude_types[ self.t ][ 0 ]
        circle( screen, normal_color, p, 10, 1 )
        line( screen, normal_color, p, q, 1 )
