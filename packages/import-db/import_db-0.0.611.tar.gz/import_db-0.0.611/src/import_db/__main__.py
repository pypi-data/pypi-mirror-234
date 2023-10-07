from os                 import environ
from            .server import start_server

if __name__ == '__main__':
  password  = environ['MSFRPC_PASSWORD']
  username  = environ['MSFRPC_USERNAME']
  #password  = environ.get('MSFRPC_PASSWORD')
  #username  = environ.get('MSFRPC_USERNAME')
  upstreamh = environ.get('MSFRPC_HOSTNAME')
  start_server(password, username, upstreamh=upstreamh)

