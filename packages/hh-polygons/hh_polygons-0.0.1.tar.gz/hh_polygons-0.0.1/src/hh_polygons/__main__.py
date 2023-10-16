from psycopg2           import connect
from            .server import start_server

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  create_table(conn)
  conn.commit()
  start_server(conn)

