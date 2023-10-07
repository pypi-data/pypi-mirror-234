from psycopg2           import connect
from teamhack_db.conf   import config
from            .server import start_server
#from             server import start_server
from             .sql   import create_tables
#from              sql   import create_tables

if __name__ == '__main__':
  conns        = dict()
  for db in ('dns', 'msf', 'sdn'): # TODO how to read all sections
    conns[db]  = connect(**config(section=db))

  create_tables(conns['dns'], conns['sdn'])

  start_server(**conns)

