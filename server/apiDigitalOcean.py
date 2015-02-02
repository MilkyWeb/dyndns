import requests, json

class apiDigitalOcean:
  doUrl = 'https://api.digitalocean.com/v2/domains/'
  domain = ''
  recordName = ''
  urls = {
    'getRecords':'/records',
    'updateRecord':'/records/%s'
  }
  cache = {
    'getRecords':None,
    'getRecord':None
  }
  headers = {'Authorization': ''}

  def setDomain(self, domain):
    self.domain = domain

  def setRecordName(self, recordName):
    self.recordName = recordName

  def getRecordName(self):
    return self.recordName

  def setToken(self, token):
    self.headers['Authorization'] = token

  def getUrl(self, method):
    return self.doUrl + self.domain + self.urls[method]

  def getRecords(self):
    if (self.cache['getRecords'] is None):
      self.cache['getRecords'] = requests.get(self.getUrl('getRecords'), data={}, headers=self.headers)
    return self.cache['getRecords'];

  def getRecord(self, recordName):
    if ((self.cache['getRecord']) is not None and (recordName in self.cache['getRecord'])):
      return self.cache['getRecord'][recordName]
    else:
      records = self.getRecords()
      for record in records.json()['domain_records']:
        if record['name'] == recordName:
          if (self.cache['getRecord'] is None):
            self.cache['getRecord'] = {}
          self.cache['getRecord'][recordName] = record
          return record

  def getRecordData(self, recordName):
    return self.getRecord(recordName)['data']

  def updateRecord(self, recordName, data):
    record = self.getRecord(recordName)
    newData = {'name':record['name'], 'data':data}
    url = self.getUrl('updateRecord') % record['id']
    r = requests.put(url, data=newData, headers=self.headers)
