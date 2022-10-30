#Questo file contiene tutte le classi che utilizzo nel mio progetto

from ncclient import manager

class Device:
  def __init__(self, name, username='EspositoA1', password='admin'):
    self.name = name
    self.username = username
    self.password = password

  def connectnetconf(self):
    return manager.connect(host=self.name, port=830, username=self.username, password=self.password, hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)

class IOSXR(Device):
  def setisisinstancename(self, isisinstancename):
    self.isisinstancename = isisinstancename
    
#voglio garantire che un attributo isisinstancename sia sempre settati nelle istanze di questa classe.    
class VPE(IOSXR):
  def __init__(self, isisinstancename):
    self.isisinstancename = isisinstancename
    
class NXOS(Device):
  def __init__(self, name, username, password ):
    Device.__init__(self,name,username,password)
  
  def connectnxapi(self, cmd):
    self.cmd = cmd
    print(self.name)
    print(cmd)
    print(self.cmd)
    print(self.username)
    print(self.password)
    client_cert_auth=True
    client_cert='/home/EspositoA1/CERT_DEMO2/mivce501.crt'
    client_private_key='/home/EspositoA1/CERT_DEMO2/mivce501.key'
    ca_cert='/home/EspositoA1/CERT_DEMO2/mivce501-chain.pem'
    url='http://' + self.name + '/ins'
    print(url)
    myheaders={'content-type':'application/json-rpc'}

    payload=[
     {
       "jsonrpc": "2.0",
       "method": "cli",
       "params": {
       "cmd": cmd,
       "version": 1
        },
     "id": 1
     }
    ]

    if client_cert_auth is False:
        response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(self.name,self.password)).json()
    else:
        url='https://' + self.name + '/ins'
        response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(self.name,self.password),cert=(client_cert,client_private_key),verify=ca_cert).json()
    return response
    
