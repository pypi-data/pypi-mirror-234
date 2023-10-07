#from psycopg2 import connect

def execute(conn, sql, *args):
  with conn.cursor() as curs: curs.execute(sql, *args)

def select(conn, sql, *args):
  with conn.cursor() as curs:
    curs.execute(sql, *args)
    return curs.fetchall()

def drop_type_record(conn): return execute(conn, """DROP TYPE IF EXISTS record_type""") # TODO delete this
def drop_table(conn):
  execute(conn, """DROP TABLE IF EXISTS hosts""")
  drop_type_record(conn)

#def create_type_record(conn): execute("""CREATE TYPE record_type AS ENUM ('A', 'AAAA', 'MX', 'NS')""")
def create_table(conn):
  #create_type_record(conn)
  return execute(conn,  """
    CREATE TABLE IF NOT EXISTS hosts (
      id       SERIAL        PRIMARY KEY,
      hostname VARCHAR(255)  NOT NULL,
      record   INT           NOT NULL,
      ip       INET          NOT NULL,
      UNIQUE(hostname, record)
    )
  """)

def insert(conn, hostname, record, ip):
  sql = """INSERT INTO hosts (hostname, record, ip) VALUES (%s, %s, %s)"""
  return execute(conn, sql, (hostname, record, ip,))

def select_all                (conn):                   return select(conn, """SELECT hostname, record, ip FROM hosts""")
def select_ip                 (conn, ip):               return select(conn, """SELECT * FROM hosts WHERE ip = %s""", (ip,))
def select_hostname           (conn, hostname):         return select(conn, """SELECT * FROM hosts WHERE hostname = %s""", (hostname,))
def select_hostname_recordtype(conn, hostname, record): return select(conn, """SELECT * FROM hosts WHERE hostname = %s AND record = %s""", (hostname, record))
        #return curs.fetchone()

def drop_row_id                 (conn, row_id):           return execute(conn, """DELETE FROM hosts WHERE id = %s""", (row_id,))
def drop_row_hostname           (conn, hostname):         return execute(conn, """DELETE FROM hosts WHERE hostname = %s""", (hostname,))
def drop_row_hostname_recordtype(conn, hostname, record): return execute(conn, """DELETE FROM hosts WHERE hostname = %s AND record = %s""", (hostname,))
def drop_row_ip                 (conn, ip):               return execute(conn, """DELETE FROM hosts WHERE ip = %s""", (ip,))

