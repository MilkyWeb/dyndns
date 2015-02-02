#!/usr/bin/python3
import sys
import os

def printUsage():
  sys.exit('Usage: %s server|client' % sys.argv[0])

if ((len(sys.argv)!=2) or (sys.argv[1] != 'client') and (sys.argv[1] != 'server')):
  printUsage()

print("Generating daemon script\n")
fileContents = open('dyndns.sh').read( os.path.getsize('dyndns.sh') )
fileContents = fileContents.replace('{DYNDNS_PATH}', os.getcwd())
fileContents = fileContents.replace('{VERSION}', sys.argv[1])
fileContents = fileContents.replace('{USER}', os.getlogin())

print("Writing daemon script in /etc/init.d\n")
daemonPath = '/etc/init.d/dyndns'
daemon = open(daemonPath, 'w')
daemon.write(fileContents)
daemon.close()

print('Changing permissions\n')
os.chmod(daemonPath, 0o755)

print('Installing the init script')
os.system('update-rc.d dyndns defaults')

print('done.\nYou can start the service by using:\nsudo service dyndns start')