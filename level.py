"""
A level; mostly mesh manipulation
"""

from pygame.draw import polygon, line
from cPickle import dump, load
from vecutils import *

EDGEFOLLOW_BUFFER = 16

class Level:
    def __init__( self ):
        self.verts = [ ]
        self.polys = [ ]
        self.load_file('level.dat')

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
        print('Saved %s' % filename)

    def load_file(self, filename):
        f = open(filename, 'rb')
        self.verts, self.polys = load(f)
        f.close()
        self.dirty = True
        print('Loaded %s' % filename)

    def get_firing_position_near( self, x, y ):
        for q,p in self._external_edges:
            px, py = self.verts[p]
            qx, qy = self.verts[q]
            dx, dy = normalize( (qy - py, px - qx) )
            z = -( dx * px + dy * py )
            dz = dot( (x,y), (dx,dy) ) + z

            if dz < 20 and dz > 0:
                d = length( (qx - px, qy - py) )
                t = dot( ((x - px)/d, (y - py)/d), (-dy, dx) )
                if t >= 0 and t <= 1:
                    k = EDGEFOLLOW_BUFFER / d
                    if t < k: t = k
                    if t > 1 - k: t = 1 - k
                    return { 'pos': (px + t * (qx - px) + 15 * dx,
                                     py + t * (qy - py) + 15 * dy),
                             't':   t,
                             'd':   d,
                             'z':   z,
                             'tangent': (-dy,dx),
                             'norm': (dx, dy) }

        return None
