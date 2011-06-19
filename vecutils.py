"""
Vector math utilities
"""

from math import sqrt

def length( p ):
    x,y = p
    return sqrt(x * x + y * y)

def normalize( p ):
    x,y = p
    d = sqrt(x * x + y * y)
    return x / d, y / d

def dot( p, q ):
    x,y = p
    u,v = q
    return x * u + y * v

def intvec( p ):
    return int(p[0]), int(p[1])
