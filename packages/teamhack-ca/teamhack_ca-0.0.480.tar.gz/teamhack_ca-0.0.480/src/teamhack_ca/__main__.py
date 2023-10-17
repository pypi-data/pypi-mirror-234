#from psycopg2         import connect
#from teamhack_db.conf import config
#from teamhack_db.sql  import create_table
from .server          import start_server

if __name__ == '__main__':
  #params = config()
  #conn   = connect(**params)

  #create_table(conn)
  #conn.commit()
  #start_server(conn)
  start_server()

