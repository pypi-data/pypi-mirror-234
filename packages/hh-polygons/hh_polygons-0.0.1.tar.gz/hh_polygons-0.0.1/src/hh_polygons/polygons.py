from fractions        import Fraction

from functools        import lru_cache
from functools        import reduce
from functools        import wraps

from itertools        import accumulate
from itertools        import chain
from itertools        import combinations
from itertools        import combinations_with_replacement
from itertools        import permutations
from itertools        import product
from itertools        import repeat
from itertools        import starmap
from itertools        import takewhile

from joblib           import Memory

from logging          import DEBUG
from logging          import basicConfig
import logging

from math             import gcd
from math             import isclose
from math             import lcm
from math             import log
from numpy import sin
from numpy import cos
from numpy import pi

from operator         import __and__
from operator         import __mul__
from operator         import __or__
from operator         import __sub__

#from peval            import inline
#from peval            import partial_apply
from peval            import pure

from shapely.geometry import Polygon
from sympy            import divisors
from sys              import stdout

from time             import time

from typing           import Callable
from typing           import Optional
from typing           import TypeVar

#import numba as nb
import numpy as np

##
#
##

X = TypeVar('X')
Y = TypeVar('Y')

##
#
##

basicConfig(stream=stdout, level=DEBUG)

def trace(f:Callable[[Y],X])->Callable[[Y],X]:
    @wraps(f)
    def wrap_func(*args, **kwargs)->Y:
        logging.debug(f'enter {f.__name__!r}')
        t0 = time()
        y  = f(*args, **kwargs)
        t1 = time()
        dt = t1 - t0
        logging.debug(f'leave {f.__name__!r} {dt!r}')
        return y
    return wrap_func

##
#
##

# TODO PG-backend
cachedir = 'cache'
mem      = Memory(cachedir, verbose=0)

def cache(f:Callable[[Y],X])->Callable[[Y],X]:
    g = mem.cache(f)

    @wraps(f)
    def wrap_func(*args, **kwargs)->Y: return g(*args, **kwargs)
    return wrap_func

##
#
##

# https://www.tutorialguruji.com/python/cartesian-product-of-arbitrary-dimensional-coordinates-in-arbitrary-dimensional-arrays/
#@inline
@pure
#def cartesian_product(x, y):
def cartesian_product(x->list[list[int]], y->list[list[int]])->list[list[list[list[int]]]]:
    if x.ndim < 2: x = np.atleast_2d(x).T
    if y.ndim < 2: y = np.atleast_2d(y).T

    sx, sy = x.shape, y.shape
    sz = sy[:-1] + sx[:-1] + (sy[-1] + sx[-1],)
    z = np.empty(sz, np.result_type(x, y))

    # Broadcasted assignment
    z[...,:sx[-1]] = x
    z[...,sx[-1]:] = y.reshape(sy[:-1] + (x.ndim-1)*(1,) + (sy[-1],))

    return z

#@inline
@pure
def polygon_helper_kernel(beats:int, nvertex:int, offset:int, f:Callable[[int,int,int],list[list[int]]])->list[list[int]]:
    base = np.array((offset,), dtype=int).reshape(1,1)
    if nvertex == 1: return base

    offs = np.arange(offset+1, beats-(nvertex-1)+1)

    ret1 = map(f, offs) # TODO vectorize
    ret2 = np.concatenate(tuple(ret1)) #ret2 = chain.from_iterable(ret1)

    ret3 = cartesian_product(base, ret2)
    ret4 = ret3.reshape(-1, ret3.shape[-1])
    return ret4
@cache
@pure
def polygon_helper_impl(g:Callable[[Callable,int,int,int],list[list[int]]], beats:int, nvertex:int, offset:int)->list[list[int]]:
    f = lambda off: g(g, beats, nvertex-1, off)
    return polygon_helper_kernel(beats, nvertex, offset, f)
@trace
@pure
def polygon_helper(beats:int, nvertex:int)->list[list[int]]: return polygon_helper_impl(polygon_helper_impl, beats, nvertex, 0)

##
#
##

#@inline
@pure
def centroid(vertexes:list[tuple[float,float]])->list[float]:
    p1 = Polygon(vertexes) # Polygon
    p2 = p1.centroid       # Point
    p3 = p2.coords         # CoordinateSequence
    p4 = np.array(p3).ravel()
    return p4
@pure
def is_balanced(p:list[tuple[float,float]])->bool:
    c = centroid(p) + 1              # offset origin to (1,1,...)
    o = np.ones(c.size, dtype=float) # because near-zero comparisons are weirder
    return np.allclose(c, o)         # than normal floating-point equality tests
@cache
@pure
def polygon(r:list[float])->list[tuple[float,float]]:
    x   = cos(r)
    y   = sin(r)
    return np.array((x, y), dtype=float).T #return zip(x, y) # tuples were here

@pure
def is_balanced2(num:list[int], den:int)->bool:
    b = 2 * pi * num / den
    c = polygon(b)
    return is_balanced(c)
is_balanced2_vec = np.vectorize(is_balanced2, excluded=['den'], signature='(n),()->()')

#@trace
@pure
def balanced_polygons(beats:int, nvertex:int)->list[list[int]]:
    p = polygon_helper(beats, nvertex)
    r = np.where(is_balanced2_vec(p, beats))
    return p[r]


##
#
##

@pure
def set_difference(a1:list[list[int]], a2:list[list[int]])->list[list[int]]:
    a1_rows = a1.view([('', a1.dtype)] * a1.shape[1])
    a2_rows = a2.view([('', a2.dtype)] * a2.shape[1])
    a3      = np.setdiff1d(a1_rows, a2_rows)
    a3      = a3.view(a1.dtype)
    a3      = a3.reshape(-1, a1.shape[1])
    return a3

@trace
#@inline
@pure
def rotations(p:list[int], beats:int, diff=True)->list[list[int]]:
    n = np.arange(1,beats).reshape(beats-1,1)

    s = (beats-1, len(p),)
    q = np.broadcast_to(p, s)
    q = (q + n) % beats

    q = np.sort(q, axis=1)

    if diff: q = set_difference(q, p.reshape(1,-1))
    else:    q = np.unique(q, axis=0)
    return q
rotations_vec = np.vectorize(rotations, excluded=['beats', 'diff'], signature='(n),(),()->(m,n)')

@trace
#@inline
@pure
def polygon_rotations(p:list[list[int]], beats:int, diff=True)->list[list[int]]:
    r = rotations_vec(p, beats, diff)
    r = r.reshape(-1, r.shape[-1])
    if diff: r = set_difference(r, p)
    else:    r = np.unique(r, axis=0)
    return r

##
#
##

@trace
#@inline
@pure
def balanced_line(beats:int)->list[list[int]]:
    if beats % 2 != 0: return ()
    l = (0, beats // 2)
    l = np.array(l, dtype=int)
    l = l.reshape(1,-1)
    return (l,)

#@inline
@pure
def empty(e): return e.size != 0

@trace
#@inline
@pure
def balanced_shapes(beats1:int, beats2:int)->list[list[int]]:
    #n = range(3, beats2+1)
    n = range(beats1, beats2+1)
    #f = partial_apply(balanced_polygons, beats)
    f = lambda nvertex: balanced_polygons(beats2, nvertex)
    p = map(f, n)
    #if filterempty:
    p = filter(empty, p)
    l = balanced_line(beats2)
    p = chain(l, p)

    p = tuple(p)
    print('p: ', p)

    return p

@trace
#@inline
@pure
def balanced_shapes_rotations(beats1:int, beats2:int, diff=False)->list[list[int]]:
    p = balanced_shapes(beats1, beats2)
    #g = partial_apply(polygon_rotations, beats=beats, diff=diff)
    g = lambda p: polygon_rotations(p, beats2, diff)
    p = map(g, p)

    p = tuple(p)
    print('p: ', p)

    return p

@trace
#@inline
@pure
def balanced_shapes_api(beats:int)->list[list[int]]:
    p = balanced_polygons(beats, beats)
    #if filterempty:
    #p = filter(empty, p)
    l = balanced_line(beats)
    p = chain(l, p)

    p = tuple(p)
    print('p: ', p)

    return p
@trace
#@inline
@pure
def balanced_shapes_rotations_api(beats:int, diff=False)->list[list[int]]:
    p = balanced_shapes_api(beats)
    #g = partial_apply(polygon_rotations, beats=beats, diff=diff)
    g = lambda p: polygon_rotations(p, beats, diff)
    p = map(g, p)

    p = tuple(p)
    print('p: ', p)

    return p
##
#
##

#@inline
@pure
def normalize_polygon(beats:int, p:list[int])->list[int]: return beats - p

@cache
#@inline
@pure
def congruency(p:list[int], beats:int)->int:
    q = normalize_polygon(beats, p)
    g = gcd(*q)
    assert beats % g == 0
    assert g != 0
    return beats // g
congruency_vec = np.vectorize(congruency, excluded=['beats'], signature='(n),()->()')

@trace
#@inline
@pure
def polygon_congruencies(p:list[list[int]], beats:int)->list[int]: return congruency_vec(p, beats)

##
#
##

@trace
def metadata(beats:int)->list[tuple[list[int], int]]:
    n = range(3, beats+1) # TODO lines
    f = partial_apply(balanced_polygons, beats)
    n = map(f, n)
    f = lambda e: e.size != 0
    n = filter(f, n)
    # TODO filter empty layers
    n = tuple(n)
    print('n: ', n)

    g = partial_apply(polygon_rotations, beats=beats)
    p = map(g, n)
    p = filter(f, p)
    p = tuple(p)
    print('p: ', p, '\n')

    h = partial_apply(polygon_congruencies, beats=beats)
    c = map(h, p)
    c = tuple(c)
    print('c1: ', c, '\n')

    zp = zip(p, c)

    c = map(h, n)
    c = tuple(c)
    print('c2: ', c, '\n')

    zn = zip(n, c)
    z  = zip(zp, zn)
    return z


##
#
##

@trace
def main():
    #n = 30
    n = 10
    #p = metadata(n)
    p = balanced_shapes_rotations(3, n)
    for k in p: print(k)
    print()
    #p = balanced_shapes_rotations(n, n)
    #for k in range(3, n+1):
    #  p = balanced_shapes_rotations_api(k)
    #  print()
    #  for k in p: print(k)
    #  print()

if __name__ == '__main__': exit(main())

