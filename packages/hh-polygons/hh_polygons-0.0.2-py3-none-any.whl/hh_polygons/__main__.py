from psycopg2           import connect, Error as PGError

from teamhack_db.conf   import config

from            .server import start_server
from            .sql    import create_table

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  try:
    create_table(conn)
    conn.commit()
  except PGError as e:
    print(f"Error: {e}")
    conn.rollback()
    raise e

  start_server(conn)

