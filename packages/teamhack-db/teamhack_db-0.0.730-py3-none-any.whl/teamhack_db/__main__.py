from psycopg2 import connect, Error as PGError
from .sql     import create_table
from .cli     import start_cli
from .conf    import config

if __name__ == '__main__':
  params = config()
  conn   = connect(**params)

  try:
    create_table(conn)
    conn.commit()
  except PGError as e:
    print(f"Error: {e}")
    conn.rollback()

  start_cli(conn)

