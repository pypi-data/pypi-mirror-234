from tempfile import NamedTemporaryFile
from flask import Flask, jsonify, request
from json  import dumps, loads
from subprocess import run, PIPE, check_output
from os import unlink

from .polygons import balanced_shapes_rotations

def dejsonifynp(j):
  l = loads(j)
  return np.array(l)

def   jsonifynp(a):
  l = a.tolist()
  return dumps(l)

def create_app():
  app = Flask(__name__)

  @app.route('/cartesian_product', methods=['POST'])
  def cartesian_product_rest():
    data = request.get_json(force=True)
    x    = dejsonifynp(data['A'])
    y    = dejsonifynp(data['B'])
    xy   = cartesian_product(x, y)
    return   jsonifynp(xy)

  @app.route('/centroid', methods=['POST'])
  def centroid_rest():
    data = request.get_json(force=True)
    p    = loads(data)
    c    = centroid(p)
    return   jsonifynp(c)

  @app.route('/isbalanced', methods=['POST'])
  def isbalanced_rest():
    data = request.get_json(force=True)
    p    = loads(data)
    b    = is_balanced(p)
    return   jsonify  (b)

  @app.route('/polygons', methods=['POST'])
  def polygon_rest():
    data = request.get_json(force=True)
    R    = loads(data)
    p    = polygon(R)
    return   jsonifynp(p)

  @app.route('/isbalanced2', methods=['POST'])
  def isbalanced2_rest():
    data = request.get_json(force=True)
    p    = loads(data['polygon'])
    d    = data['denominator']
    b    = is_balanced2(p, d)
    return   jsonify  (b)

  @app.route('/balanced_polygons', methods=['GET'])
  def balanced_polygons_rest():
    b    = request.args.get('nvertex',     request.args.get('pulses'))
    v    = request.args.get('denominator', request.args.get('beats'))
    P    = balanced_polygons(b, v)
    return   jsonifynp(P)

  @app.route('/set_difference', methods=['POST'])
  def set_difference_rest():
    data = request.get_json(force=True)
    x    = dejsonifynp(data['A'])
    y    = dejsonifynp(data['B'])
    xy   = set_difference(x, y)
    return   jsonifynp(xy)

  @app.route('/rotations', methods=['POST'])
  def rotations_rest():
    data = request.get_json(force=True)
    p    = dejsonifynp(data['polygon'])
    b    = data['denominator']
    diff = data.get('diff', None)
    P    = rotations(p, b, diff)
    return   jsonifynp(P)

  @app.route('/polygon_rotations', methods=['POST'])
  def polygon_rotations_rest():
    data = request.get_json(force=True)
    P    = dejsonifynp(data['polygons'])
    b    = data['denominator']
    d    = data.get('diff', None)
    R    = polygon_rotations(P, b, d)
    return   jsonifynp(R)

  @app.route('/balanced_line', methods=['GET'])
  def balanced_line_rest():
    b    = request.args.get('denominator')
    L    = balanced_line(beats)
    return   jsonifynp(L)

  @app.route('/balanced_shapes', methods=['GET'])
  def balanced_shapes_rest():
    b1   = request.args.get('min')
    b2   = request.args.get('max')
    P    = balanced_shapes(b1, b2)
    return   jsonify  (P)

  @app.route('/balanced_shapes_rotations', methods=['GET'])
  def balanced_shapes_rotations_rest():
    b1   = request.args.get('min')
    b2   = request.args.get('max')
    d    = request.args.get('diff', None)
    P    = balanced_shapes_rotations(b1, b2, d)
    return   jsonify  (P)

  @app.route('/normalize_polygon', methods=['POST'])
  def normalize_polygon_rest():
    data = request.get_json(force=True)
    b    = data['denominator']
    p    = loads(data['polygon'])
    n    = normalize_polygon(b, p)
    return   jsonify  (n)

  @app.route('/congruency', methods=['POST'])
  def congruency_rest():
    data = request.get_json(force=True)
    p    = loads(data['polygon'])
    b    = data['denominator']
    c    = congruency(p, b)
    return   jsonify  (c)

  @app.route('/polygon_congruencies', methods=['POST'])
  def polygon_congruencies_rest():
    data = request.get_json(force=True)
    p    = loads(data['polygon'])
    b    = data['denominator']
    c    = polygon_congruencies(p, b)
    return   jsonifynp(c)

  @app.route('/metadata', methods=['GET'])
  def metadata_rest():
    b    = request.args.get('denominator')
    m    = metadata(b)
    return   jsonify  (m)

  return app

def start_server(host="0.0.0.0", port=55432, *args, **kwargs):
  app = create_app(**kwargs)
  app.run(debug=True, host=host, port=port, *args)

# https://www.easydevguide.com/posts/curl_upload_flask

