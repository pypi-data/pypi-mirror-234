from flask import jsonify
from json  import dumps, loads
import numpy as np

from .polygons import balanced_shapes_rotations

def dejsonifynp(j):
  l = loads(j)
  return np.array(l)

def   jsonifynp(a):
  l = a.tolist()
  return dumps(l)

