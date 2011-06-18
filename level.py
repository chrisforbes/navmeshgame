from pygame.draw import polygon
from cPickle import dump, load

class Level:

    def __init__( self, screen ):
        self.screen = screen
        self.verts = [ (200,200), (400,200), (400,400), (200,400) ]
        self.polys = [ [ 0, 1, 2, 3 ] ]
        # 0 = walkable, 1 = shootable
        self.colors = [ (0, 0, 0), (40, 40, 40) ]

    def draw( self ):
        for poly in self.polys:
            actual_verts = [ self.verts[x] for x in poly ]
            polygon( self.screen, self.colors[0], actual_verts )

    def save_file(self, filename):
        f = open(filename, 'wb')
        dump((self.verts, self.polys), f)
        f.close()

    def load_file(self, filename):
        f = open(filename, 'rb')
        self.verts, self.polys = load(f)
        f.close()

