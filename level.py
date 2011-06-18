from pygame.draw import polygon, line
from cPickle import dump, load

TOLERANCE = 4   #px

def make_replacer( a, b ):
    def f(x): return b if a == x else x
    return f

class Level:
    def __init__( self ):
        self.verts = [ (200,200), (400,200), (400,400), 
                       (200,400), (600,200), (600,400) ]
        self.polys = [ [ 0, 1, 2, 3 ], [ 1, 4, 5, 2 ] ]

        # 0 = walkable, 1 = shootable
        self.colors = [ (0, 0, 0), (40, 40, 40), (60, 60, 60) ]
        self.dirty = True

    def draw( self, screen ):
        if self.dirty:
            self.update()
        for p in self._fill_polys:
            polygon( screen, self.colors[0], p )
        for v1,v2 in self._internal_edges:
            line( screen, self.colors[1], self.verts[v1], self.verts[v2] )
        for v1,v2 in self._external_edges:
            line( screen, self.colors[2], self.verts[v1], self.verts[v2], 3 )

    def update( self ):
        self.dirty = False
        self._fill_polys = [[self.verts[x] for x in p] for p in self.polys]     
        
        edges = {}
        for p in self.polys:
            last = p[-1]
            for v in p:
                rk = (v,last)
                k = (last,v)
                if rk in edges:
                    edges[rk] = edges[rk] + 1
                else:
                    edges[k] = 1
                last = v

        self._internal_edges = [ e for e,count in edges.items() if count==2 ]
        self._external_edges = [ e for e,count in edges.items() if count==1 ]

    def save_file(self, filename):
        f = open(filename, 'wb')
        dump((self.verts, self.polys), f)
        f.close()

    def load_file(self, filename):
        f = open(filename, 'rb')
        self.verts, self.polys = load(f)
        f.close()

    def vertex_at( self, x, y ):
        for i,p in enumerate(self.verts):
            _x,_y = p
            if abs( x - _x ) <= TOLERANCE and abs( y - _y ) <= TOLERANCE:
                return i
        return None

    def new_vertex( self, x, y ):
        self.verts.append( (x,y) )
        self.dirty = True
        return len(self.verts) - 1

    def del_vertex( self, x, y ):
        v = self.vertex_at( x, y )
        if v == None:
            return
      
        u = len(self.verts) - 1 
        rep = replacer( u, v ) 
        self.polys = [[rep(x) for x in p if x != v] for p in self.polys]
        self.polys = [p for p in self.polys if len(p) > 2]
        del self.verts[-1]
        self.dirty = True

    def new_poly( self, v ):
        self.polys.append( [v] )
        self.dirty = True
        return len(self.polys) - 1

    def add_to_poly( self, p, v ):
        self.polys[p].append(v)
        self.dirty = True
