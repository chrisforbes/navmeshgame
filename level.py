from pygame.draw import polygon
from cPickle import dump, load

class Level:

    def __init__( self ):
        self.verts = [ (200,200), (400,200), (400,400), (200,400) ]
        self.polys = [ [ 0, 1, 2, 3 ] ]
        # 0 = walkable, 1 = shootable
        self.colors = [ (0, 0, 0), (40, 40, 40) ]
        self.dirty = True

    def draw( self, screen ):
        if self.dirty:
            self.update()
        for p in self._fill_polys:
            polygon( screen, self.colors[0], p )

    def update( self ):
        self.dirty = False
        self._fill_polys = [[self.verts[x] for x in p] for p in self.polys]

    def save_file(self, filename):
        f = open(filename, 'wb')
        dump((self.verts, self.polys), f)
        f.close()

    def load_file(self, filename):
        f = open(filename, 'rb')
        self.verts, self.polys = load(f)
        f.close()

