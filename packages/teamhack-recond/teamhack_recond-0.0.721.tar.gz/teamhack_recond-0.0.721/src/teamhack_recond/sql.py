from teamhack_db.sql  import create_table, insert, execute, select
from teamhack_db.util import get_name, get_record_type
from            .util import diff
#from             util import diff

def create_table_sdn  (conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS subdomains  (
    id        SERIAL        PRIMARY KEY,
    subdomain VARCHAR(255)  NOT NULL,
    host      INET          NOT NULL,
    UNIQUE(subdomain, host)
  )
""")

# TODO port ?
def create_table_vh   (conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS vhosts      (
    id        SERIAL        PRIMARY KEY,
    vhost     VARCHAR(255)  NOT NULL,
    host      INET          NOT NULL,
    UNIQUE(vhost, host)
  )
""")

# TODO port ?
def create_table_fp   (conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS subdirs     (
    id        SERIAL        PRIMARY KEY,
    vhostid   INT           NOT NULL REFERENCES vhosts(id),
    path      VARCHAR(255)  NOT NULL,
    UNIQUE(vhostid, path)
  )
""")

def create_table_srv  (conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS services    (
    id        SERIAL        PRIMARY KEY,
    subdnid   INT           NOT NULL REFERENCES subdomains(id),
    port      INT2          NOT NULL,
    UNIQUE(subdnid, port)
  )
""")

def create_table_creds(conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS credentials (
    id        SERIAL        PRIMARY KEY,
    serviceid INT           NOT NULL REFERENCES services(id),
    username  VARCHAR(255),
    password  VARCHAR(255),
    UNIQUE(serviceid, username)
  )
""")

def create_table_flags(conn): return execute(conn, """
  CREATE TABLE IF NOT EXISTS flags       (
    id        SERIAL        PRIMARY KEY,
    host      INET          NOT NULL,
    flag      VARCHAR(255)  NOT NULL,
    path      VARCHAR(255)  NOT NULL,
    isroot    BOOLEAN       NOT NULL,
    UNIQUE(host, path),
    UNIQUE(host, isroot)
  )
""")

def drop_table_sdn  (conn): return execute(conn, """DROP TABLE IF EXISTS subdomains""")
def drop_table_vh   (conn): return execute(conn, """DROP TABLE IF EXISTS vhosts""")
def drop_table_fp   (conn): return execute(conn, """DROP TABLE IF EXISTS subdirs""")
def drop_table_srv  (conn): return execute(conn, """DROP TABLE IF EXISTS services""")
def drop_table_creds(conn): return execute(conn, """DROP TABLE IF EXISTS credentials""")
def drop_table_flags(conn): return execute(conn, """DROP TABLE IF EXISTS flags""")

def drop_tables(conn):
  drop_table_flags(conn)
  drop_table_creds(conn)
  drop_table_srv  (conn)
  drop_table_fp   (conn)
  drop_table_vh   (conn)
  drop_table_sdn  (conn)

def create_tables(dns, sdn):
  drop_tables(sdn) # TODO delete

  create_table(dns)
  dns.commit()
  create_table_sdn  (sdn)
  create_table_vh   (sdn)
  create_table_fp   (sdn)
  create_table_srv  (sdn)
  create_table_creds(sdn)
  create_table_flags(sdn)
  sdn.commit()

def select_dns  (conn):    return select(conn, """
  SELECT ip
  FROM hosts
""")
#def select_msf(conn, q): return select(conn, """
#  SELECT address           FROM hosts
#  WHERE address IN %s
#""", (tuple(q),))
def select_msf (conn, q):
  print("select_msf(q=%s)" % (q,))
  return select(conn, """
  SELECT address
  FROM hosts
  WHERE address IN %s
""", (tuple(q),))
def select_sdn (conn, q): return select(conn, """
  SELECT subdomain, host
  FROM subdomains
  WHERE host    IN %s
""", (tuple(q),))
def select_vh  (conn, q): return select(conn, """
  SELECT vhost,     host
  FROM vhosts
  WHERE host    IN %s
""", (tuple(q),))
def select_fp  (conn, q): return select(conn, """
  SELECT vhost,     host, path
  FROM subdirs
  JOIN vhosts ON vhostid = vhosts.id
  WHERE host   IN %s
""", (tuple(q),))
def select_srv (conn, q): return select(conn, """
  SELECT vhost,     host, port
  FROM services
  JOIN vhosts ON vhostid = vhosts.id
  WHERE host   IN %s
""", (tuple(q),))
def select_cred(conn, q): return select(conn, """
  SELECT subdomain, host, port, username, password
  FROM credentials
  JOIN services   ON serviceid =   services.id
  JOIN subdomains ON   subdnid = subdomains.id
  WHERE host   IN %s
""", (tuple(q),))
def select_flag(conn, q): return select(conn, """
  SELECT            host, path, flag, isroot
  FROM flags
  WHERE host   IN %s
""", (tuple(q),))

def get_queue(inbound, get_outbound, db):
  outbound = get_outbound(db,       inbound)
  print(f'outbound: {outbound}')
  ret      = diff        (inbound, outbound)
  #print(f'A diff: {diff( inbound, outbound)}')
  #print(f'B diff: {diff(outbound,  inbound)}')
  print(f'ret: {ret}')
  return ret

def     portscan_queue(inbound, msf): return get_queue(inbound, select_msf,  msf)
def    subdomain_queue(inbound, sdn): return get_queue(inbound, select_sdn,  sdn)
def        vhost_queue(inbound, sdn): return get_queue(inbound, select_vh,   sdn)
def subdirectory_queue(inbound, sdn): return get_queue(inbound, select_fp,   sdn)
def   credential_queue(inbound, sdn): return get_queue(inbound, select_cred, sdn)
def         flag_queue(inbound, sdn): return get_queue(inbound, select_flag, sdn)

