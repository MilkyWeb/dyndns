#!/usr/bin/env python3
from client import *
from server import *
import sys, os, configparser, logging

def printUsage():
  sys.exit('Usage: %s server|client' % sys.argv[0])

scriptPath = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=scriptPath+'/dyndns.log', level=logging.DEBUG)

config = configparser.ConfigParser()
config.read(scriptPath + '/dyndns.conf')
serverConfig = config['server']

if (len(sys.argv)!=2):
  printUsage()

elif (sys.argv[1] == 'client'):
  logger = logging.getLogger('client')

  clientConfig = config['client']
  client = dynDnsClient()
  client.setLogger(logger)
  client.setAddress(serverConfig['address'])
  client.setPort(serverConfig['port'])
  client.setInterval(clientConfig['request_interval'])
  client.run()

elif (sys.argv[1] == 'server'):
  logger = logging.getLogger('server')

  api = apiDigitalOcean()
  api.setDomain(serverConfig['domain'])
  api.setRecordName(serverConfig['record_name'])
  api.setToken(serverConfig['token'])

  logger.info('Listening on port ' + serverConfig['port'])
  server = dynDnsServer((serverConfig['address'], int(serverConfig['port'])), dynDnsServerHandler)
  server.setApi(api)
  server.setLogger(logger)
  server.serve_forever()

else:
  printUsage()