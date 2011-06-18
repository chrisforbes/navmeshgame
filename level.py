from pygame.draw import polygon

walkable_color = 0, 0, 0

level_verts = [ (200,200), (400,200), (400,400), (200,400) ]
level_polys = [ [ 0, 1, 2, 3 ] ]

class Level:
    def __init__( self, screen ):
        self.screen = screen

    def draw( self ):
        for poly in level_polys:
            actual_verts = [ level_verts[x] for x in poly ]
            polygon( self.screen, walkable_color, actual_verts )

