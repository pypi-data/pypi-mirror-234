#from flask            import Flask, jsonify, request
#from flask_restful   import Resource, Api
#from importlib       import import_module
#from importlib.util  import find_spec, LazyLoader, module_from_spec, spec_from_file_location
#from inspect         import getmembers, getmodulename, isclass
#from sys             import modules, path
#from tempfile        import NamedTemporaryFile
from ratelimit        import limits, sleep_and_retry
from requests         import post
from teamhack_db.sql  import insert
from teamhack_db.util import get_name, get_record_type
from            .sql  import *
#from             sql  import *
from            .util import diff
#from            util import diff

def portscan(queue):
  print(f'portscan({queue})')
  nmap      = 'http://0.0.0.0:55432/upload'
  response  = post(nmap,      files={'file': queue})
  if response.status_code != 200: return response.text, response.status_code

  import_db = 'http://0.0.0.0:65432/upload'
  response  = post(import_db, files={'file': response.text})
  return response.text, response.status_code

def subdomains(queue):
  #print(f'subdomains({queue})')
  pass
def vhosts(queue):
  #print(f'vhosts({queue})')
  pass
def subdirectories(queue):
  #print(f'subdirectories({queue})')
  pass
def credentials(queue):
  #print(f'credentials({queue})')
  pass
def flags(queue):
  #print(f'flags({queue})')
  pass

@sleep_and_retry
@limits(calls=3, period=180)
def loop(dns=None, msf=None, sdn=None, *args, **kwargs):
  inbound  = select_dns(dns)
  print(f'inbound: {inbound}')
  inbound  = [k[0] for k in inbound]
  print(f'inbound: {inbound}')

  psq      =     portscan_queue(inbound, msf) # msfcli   db_nmap psq
  print(f'psq: {psq}')
  text, code = portscan(psq) # batch process
  print(f'text: {text}')
  if code != 200: raise Exception(f'code: {code}')

  #svq      =      service_queue(inbound, sdn) # TODO should be populated by db_nmap ?

  sdq      =    subdomain_queue(inbound, sdn) # gobuster dns     sdq
  print(f'sdq: {sdq}')
  #sdq      =    subdomain_queue(psq, sdn) # gobuster dns     sdq
  subdomains(sdq) # sequential process

  vhq      =        vhost_queue(inbound, sdn) # gobuster vhost   shq
  #vhq      =        vhost_queue(sdq, sdn) # gobuster vhost   shq
  vhosts(vhq) # sequential process

  fpq      = subdirectory_queue(inbound, sdn) # gobuster dir     fpq
  #fpq      = subdirectory_queue(vhq, sdn) # gobuster dir     fpq
  subdirectories(fpq) # sequential process

  crq      =   credential_queue(inbound, sdn) # hydra
  credentials(crq) # sequential process

  fgq      =         flag_queue(inbound, sdn) # ssh linpeas, pspy
  flags(fgq)

  # TODO
  # - services found
  #   - scrape web for CVE re: service versions
  #   - 80, 443
  #     - begin vhost        scan
  #     - begin subdirectory scan
  #     - recursively download website
  #       - static analysis
  #       - bulk_extractor => generate wordlists
  #       - cewl
  #       - cupp
  #   - sqlmap
  #   - hydra/ncrack/medusa
  #   - db_autopwn
  pass



#def create_app(conn):
#  app = Flask(__name__)
#  #api = Api(app)
#
#  def dispatch(data, hostname_recordtype_cb, hostname_cb, ip_cb):
#    if 'host' in data and 'type' in data:
#      host = data['host']
#      host = get_name(host)
#      rt   = data['type']
#      rt   = get_record_type(rt)
#      ret  = hostname_recordtype_cb(conn, host, rt)
#      return ret
#    if 'host' in data and 'type' not in data:
#      host = data['host']
#      host = get_name(host)
#      ret  = hostname_cb(conn, host)
#      return ret
#    if 'inet' in data:
#      addr = data['inet']
#      ret  = ip_cb(conn, addr)
#      return ret
#    return '', 404
#
#  @app.route('/create', methods=['POST'])
#  def add():
#    data = request.get_json(force=True)
#    if 'host' not in data: return '', 404
#    host = data['host']
#    host = get_name(host)
#    if 'type' not in data: return '', 404
#    rt   = data['type']
#    rt   = get_record_type(rt)
#    if 'inet' not in data: return '', 404
#    addr = data['inet']
#    insert(conn, host, rt, addr)
#    return '', 204
#
#  @app.route('/retrieve', methods=['POST'])
#  def retrieve():
#    data = request.get_json(force=True)
#    return dispatch(data, select_hostname_recordtype, select_hostname, select_ip)
#
#  @app.route('/update', methods=['POST'])
#  def update():
#    # TODO
#    return '', 404
#
#  @app.route('/delete', methods=['POST'])
#  def delete():
#    data = request.get_json(force=True)
#    return dispatch(data, drop_row_hostname_recordtype, drop_row_hostname, drop_row_ip)
#
#  return app

def start_server(host="0.0.0.0", port=6000, dns=None, msf=None, sdn=None, *args, **kwargs):
  #psd = portscan_daemon()
  #while(True): loop(dns, msf, sdn, psd, **kwargs)
  while(True): loop(dns, msf, sdn, **kwargs)
  #app = create_app(dns=dns, msf=msf, **kwargs)
  #app.run(debug=True, host=host, port=port, *args)

