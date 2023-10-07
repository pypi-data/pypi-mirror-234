from psycopg2 import connect
from .sql     import create_table
from .cli     import start_cli
from .conf    import config

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  create_table(conn)
  conn.commit()
  start_cli(conn)

