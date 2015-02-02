import socketserver
import json

class dynDnsServerHandler(socketserver.BaseRequestHandler):
  def handle(self):
    try:
      response = {}
      updated = False
      clientIp = self.client_address[0]
      dataReceived = self.request.recv(10).decode('UTF-8')
      self.server.logger.info('Request #' + dataReceived + "\n")

      if (clientIp != self.server.currentIp):
        self.server.currentIp = clientIp
        self.server.api.updateRecord(self.server.api.getRecordName(), clientIp)
        self.server.logger.info('New IP detected: ' + clientIp)
        updated = True

      self.request.sendall(bytes(json.dumps({'updated':updated}), 'UTF-8'))
    except Exception as e:
      self.server.logger.error("Exception while receiving message: ", e)