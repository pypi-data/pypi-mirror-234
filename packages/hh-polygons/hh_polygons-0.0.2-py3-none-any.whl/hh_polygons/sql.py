from functools   import wraps
import numpy as np
from psycopg2    import Error as PGError

from teamhack_db import execute, select

def execute_all(conn, sql, *args):
  with conn.cursor() as curs:
    curs.executemany(sql, *args)
    # TODO test this
    return curs.fetchone()

def create_table_polygons (conn):
  return execute(conn,  """
    CREATE TABLE IF NOT EXISTS polygons (
      id        SERIAL        PRIMARY KEY,
      n         INT           NOT NULL
    )
  """)
      #balanced  BOOL          NOT NULL,
      #euclidean BOOL          NOT NULL,
def create_table_vertices (conn):
  return execute(conn,  """
    CREATE TABLE IF NOT EXISTS vertices (
      n         INT           NOT NULL,
      x         FLOAT         NOT NULL,
      y         FLOAT         NOT NULL,
      polygon   INT           NOT NULL REFERENCES polygons(id),
      PRIMARY KEY(n, polygon),
      UNIQUE(x, y, polygon)
    )
  """)
def create_table_balanced (conn):
  return execute(conn, """
    CREATE TABLE IF NOT EXISTS balanced (
      polygon   INT           NOT NULL PRIMARY KEY REFERENCES polygons(id)
    )
  """)
def create_table_euclidean(conn):
  return execute(conn, """
    CREATE TABLE IF NOT EXISTS euclidean (
      polygon   INT           NOT NULL PRIMARY KEY REFERENCES polygons(id)
    )
  """)

def drop_table_polygons (conn): return execute(conn, """DROP TABLE IF EXISTS polygons""")
def drop_table_vertices (conn): return execute(conn, """DROP TABLE IF EXISTS vertices""")
def drop_table_balanced (conn): return execute(conn, """DROP TABLE IF EXISTS balanced""")
def drop_table_euclidean(conn): return execute(conn, """DROP TABLE IF EXISTS euclidean""")

def create_tables(conn):
  create_table_polygons (conn)
  create_table_vertices (conn)
  create_table_balanced (conn)
  create_table_euclidean(conn)

def drop_tables(conn):
  drop_table_euclidean(conn)
  drop_table_balanced (conn)
  drop_table_vertices (conn)
  drop_table_polygons (conn)

def insert_polygon(conn, denominator):
  sql = """INSERT INTO polygons (n) VALUES (%s) RETURNING id"""
  return execute(conn, (denominator,))
# TODO bulk
def insert_vertex  (conn, polygon, x, y, i)
  sql = """INSERT INTO vertices (n, x, y, polygon) VALUES (%s, %s, %s, %s)"""
  return execute(conn, (i, x, y, polygon))
def insert_vertices(conn, polygon, xyi)
  sql = """INSERT INTO vertices (n, x, y, polygon) VALUES (%s, %s, %s, %s)"""
  xyi = [(polygon, x, y, i) for x, y, i in xyi]
  return execute_all(conn, polygon, xyi)
# TODO
def insert(conn, denominator, polygon):
  balanced  = is_balanced2(polygon)
  polygonid = insert_polygon(conn, denominator, balanced)
  xy        = pass
  i         = pass
  xyi       = zip(xy, i)
  return insert_vertices(conn, polygonid, xyi)

#def select_polygons         (conn, n):           return select(conn, """SELECT id, balanced FROM polygons WHERE n = %s""",                   (n,))
#def select_balanced_polygons(conn, n, balanced): return select(conn, """SELECT id           FROM polygons WHERE n = %s AND balanced = %s""", (n, balanced))
##def select_

#def drop_row_id                 (conn, row_id):           return execute(conn, """DELETE FROM hosts WHERE id = %s""", (row_id,))
#def drop_row_hostname           (conn, hostname):         return execute(conn, """DELETE FROM hosts WHERE hostname = %s""", (hostname,))
#def drop_row_hostname_recordtype(conn, hostname, record): return execute(conn, """DELETE FROM hosts WHERE hostname = %s AND record = %s""", (hostname, record))
#def drop_row_ip                 (conn, ip):               return execute(conn, """DELETE FROM hosts WHERE ip = %s""", (ip,))

def cache_balanced_polygons(conn):
  def decorator(func):
    @wraps(func)
    def wrapper(pulses, beats):
      with conn.cursor() as cur:
        cur.execute("SELECT polygon FROM polygons WHERE n = %s", (beats,))
        res = cur.fetchone()
        if res:
          pid = res[0]
          cur.execute("SELECT x, y FROM vertices WHERE polygon = %s", (pid,))
          vex = np.array(cursor.fetchall())
        else:
          polygons = func(pulses, beats)
          try:
            cur.execute("INSERT INTO polygons(n) VALUES (%s) RETURNING id", (beats,))
            pid = cursor.fetchone()[0]
            vex = polygon2(polygons, beats)
            vex = vex.astype(float)
            vex = [(i, x, y, pid) for i, (x, y) in enumerate(vertices)]
            cur.executemany("INSERT INTO vertices (n, x, y, polygon) VALUES (%s, %s, %s, %s)", vertices)
            cur.execute("INSERT INTO balanced(n) VALUES (%s)", (pid,))
            conn.commit()
          except PGError as e:
            print(f"Error: {e}")
            conn.rollback()
            raise e
        return vex
    return wrapper
  return decorator

