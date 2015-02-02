import socketserver

class dynDnsServer(socketserver.ThreadingTCPServer):
  allow_reuse_address = True
  api = None
  currentIp = None
  def setLogger(self, logger):
    self.logger = logger

  def setApi(self, api):
    self.api = api
    self.currentIp = api.getRecordData(api.getRecordName())

  def getApi(self):
    return self.api