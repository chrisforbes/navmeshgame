from pygame.draw import polygon

walkable_color = 0, 0, 0

class Level:

    def __init__( self, screen ):
        self.screen = screen
        self.verts = [ (200,200), (400,200), (400,400), (200,400) ]
        self.polys = [ [ 0, 1, 2, 3 ] ]

    def draw( self ):
        for poly in self.polys:
            actual_verts = [ self.verts[x] for x in poly ]
            polygon( self.screen, walkable_color, actual_verts )

