import socket
import time
import json

class dynDnsClient:
  currentRequest = 1
  def setLogger(self, logger):
    self.logger = logger

  def setAddress(self, address):
    self.address = str(address)

  def setPort(self, port):
    self.port = int(port)

  def setInterval(self, interval):
    self.interval = interval

  def run(self):
    while True:
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        s.send(bytes(str(self.currentRequest), 'UTF-8'))
        result = json.loads(s.recv(20).decode('UTF-8'))
        if (result['updated'] == True):
          self.logger.info('The IP has changed')
        self.currentRequest += 1
        s.close()
        time.sleep(float(self.interval))
      except Exception as e:
        self.logger.error("Exception while sending message: ", e)