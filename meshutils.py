"""
Monkeypatch in a bunch of mesh manipulation functions.
Kept here to keep the core Level class simple. 
"""

from level import Level

TOLERANCE = 4

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
    if v == self.polys[0]:
        return True
    elif v in self.polys[p]:
        return False            # already in the poly, but not the start vert
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

Level.vertex_at = vertex_at
Level.new_vertex = new_vertex
Level.del_vertex = del_vertex
Level.new_poly = new_poly
Level.add_to_poly = add_to_poly
Level.del_poly = del_poly
