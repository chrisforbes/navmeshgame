from pygame.draw import polygon, line
from cPickle import dump, load

TOLERANCE = 4   #px

class Level:
    def __init__( self ):
        self.verts = [ (200,200), (400,200), (400,400), 
                       (200,400), (600,200), (600,400) ]
        self.polys = [ [ 0, 1, 2, 3 ], [ 1, 4, 5, 2 ] ]

        # 0 = walkable, 1 = shootable
        self.colors = [ (0, 0, 0), (40, 40, 40), (60, 60, 60) ]
        self.dirty = True

    def draw( self, screen, debug ):
        if self.dirty:
            self.update()
        for p in self._fill_polys:
            polygon( screen, self.colors[0], p )
        if debug:
            for v1,v2 in self._internal_edges:
                line( screen, self.colors[1], self.verts[v1], self.verts[v2] )
        for v1,v2 in self._external_edges:
            line( screen, self.colors[2], self.verts[v1], self.verts[v2], 3 )

    def update( self ):
        self.dirty = False
        self._fill_polys = [[self.verts[x] for x in p] for p in self.polys if len(p) > 2]     
        
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

    def del_vertex( self, v ):
        u = len(self.verts) - 1
        rep = lambda x: v if x == u else x
        self.polys = [[rep(x) for x in p if x != v] for p in self.polys]
        self.verts[v] = self.verts[-1]
        del self.verts[-1]

        # collect polys which have become degenerate
        self.polys = [p for p in self.polys if len(p) > 2]
        self.dirty = True

    def new_poly( self, v ):
        self.polys.append( [v] )
        self.dirty = True
        return len(self.polys) - 1

    def add_to_poly( self, p, v ):
        if v in self.polys[p]:
            return True
        else:
            self.polys[p].append(v)
            self.dirty = True
            return False

    def del_poly( self, p ):
        self.polys[p] = self.polys[-1]
        del self.polys[-1]
        self.dirty = True

        # collect unreferenced verts
        vrefs = {}
        for p in self.polys:
            for v in p:
                vrefs[v] = vrefs.get(v, 0) + 1
        unused_verts = [ i for i,v in enumerate(self.verts)
            if vrefs.get(i,0) == 0 ][:]
        unused_verts.reverse()
        for uv in unused_verts:
            self.del_vertex( uv )

    def get_firing_position_near( self, x, y ):
        return 300, 300
