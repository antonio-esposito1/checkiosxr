"""
L'obbiettivo di questo programma è raccogliere le informazioni da un cisco IOSXR e NXOS per verificare il ripristino dei servizi dopo la procedura di upgrade.

il programma richiede di passare un argomento pre o post per:
  - se si sceglier pre allora vengono raccolti i dati e salvati in un file precheck.json.
  - se si sceglie post allora vengono raccolti i dati e salvati in un file postcheck.json e viene poi attivata un procedura per confrontare i due file precheck.jsoon e 
    postcheck.jsono

Le informazioni vengono raccolte dal device usando netconf quindi usiamo ncclient. il codice per fare la richiesta netconf al device è racchiuso nel module myprivatelibrary nella funzione
netconfrequest che prende in ingresso due parametri:
 - Una stringa contenete il filtro xml da applicare alla richista 
 - device a cui applicare la richiesta. Nota che device è un oggetto che viene creato con ncclient

Nota che i filtri xml da applicare alla richiesta sono salvati nella cartella templatexml per XR e templatexml-nxos per NX, e vengono letti in sequenza grazie alla libreria os, L'ordine con cui vengono letti questi file 
è alfabetico


le seguenti informazioni sulle intrfacce e sui protocolli, abbiamo cercato di mantenere una corrispondenza tra le richieste netconf che facciamo al device e i comandi utlizzati 
sul device per visualizzare le stesse informazioni, questo perchè le persone del nostro gruppo sono sicuramente più abituate a ragionare in termini di comandi cli piuttoso che modelli
di YANG. 

Le seguenti informazioni verranno raccolte per XR
- show isis neighbors
- show bgp vpnv4 unicast summary
- show bgp vpnv6 unicast summary
- show bundle bunde-eth 

Le seguenti informazioni verranno raccolte per NX
- show int description


"""

import xmltodict
import json
import os
from argparse import ArgumentParser
import getpass
import lxml.etree as et
#import requests

#from ncclient import manager

from myprivatelibrary import netconfrequest
from device import Device, IOSXR, VPE, NXOS

import shelve




"""
Questa funzione prende in ingresso due parametri:
 - Una stringa contenete il filtro xml da applicare alla richista
 - device a cui applicare la richiesta. Nota che device è un oggetto che viene creato con ncclient

"""


"""
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
    
"""


   
if __name__ == '__main__':
  
  devicename = 'v-mivpe015'
  username = 'EspositoA1'
  userpassword = 'admin'

  switchname = 'v-mivce501'
    
    
    #devicename = input('devicename: ')
    #username = input('login: ')
    #userpassword = getpass.getpass()
    
    #Nel caso voglio specificarfe la username e la pwd 
    #dev = Device(devicename, username, userpassword)
    
    #Nel caso voglio usare la username e la pwd di defailt
  dev = Device(devicename)
  print(dev)
  """
  print(dev.__class__)
  print(dev.__class__.__name__)
  print(dev.__class__.__base__)
  print(dev.__dict__)
  """
  nx = NXOS(switchname, username, userpassword)
  print(nx)
  """
  print(nx.__class__)
  print(nx.__class__.__name__)
  print(nx.__class__.__base__)
  print(nx.__dict__)
  """
  #Questa non funziona ancora ho problemi con il proxy che mi blocca la richiesta https inoltre non sono sicurissimo sulla procedura di generazione dei certificati SSL
  #showipinterfacebrief = nx.connectnxapi('show interface mgmt 0')['result']['body']
  
  
  parser = ArgumentParser(description='Usage:')
  
  # Script argument for pre e post
  
  parser.add_argument('-t', '--preorpost', type=str, required=True)
  
  args = parser.parse_args()
  
  """
  # script arguments for manager
      parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
      parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
      parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
      parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
      args = parser.parse_args()
  """
  
  
  # Attiva questo pezzo di codice quando vai in produzione
  """
  deviceip = input('deviceip: ')
  switchuser = input('login: ')
  switchpassword = getpass.getpass()
  
  device = manager.connect(host=deviceip, port=830, username=switchuser, password=switchpassword, hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)
  """
  
  # Disattiva questa linea di codice quando vai in produzione
  #device = manager.connect(host='v-mivce501', port=830, username='EspositoA1', password='admin', hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)
  
  device = dev.connectnetconf()
  
  #print (dev.hardwareversion())
  
  """
  La prima cosa che devo fare è cercare di capire con quale tipo di device stiamo lavorando, poichè non ho ancora trovato un modello di yang che mi tirasse fuori questa informazione
  dovrò usare due modelli di yang diversi. Per nx-os userò cisco-nx-os-device copyRight
  """
  
  """
  Faccio una get netconf verso il device con il filtro copyRight che mi restituisce diverse info tra cui il tipo di piattaforma su cui si sta lavorando. Ho verificato che se uso eusto 
  filtro per una macchina NX-OS mi ritornano le info richieste mentre se mando la stessa get ad una macchina XR non ho errore ma le info riportate sono vuote.
  Con questi presupposti mi basterà verificare se nella stringa di ritorno esiste la sottostringa NX-OS, in caso affermativo sono in presenza di una macchina NX-OS, in caso contrario sono
  in presenza di qualcos'altro, probabilemte XR. Non ho verificato se questo filtro lavora anche IOS-XE.
  """
  
  """
  Note che il modello di yang cisco-nx-os-device contiene tutte le informazioni che ci occorrono, ospf, interface, etc per cui useremo sempre lo stesso modello di yang per tutte le get"
  """
  
  copyRight = '''
                <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
                   <showversion-items>
                      <copyRight/>
                   </showversion-items>
                </System>
              '''
  systemtype = device.get(('subtree', copyRight)).data_xml
  
  if 'NX-OS' in systemtype:
    path = 'templatexml-nxos'
  else:
    path = 'templatexml'
     
  
  
  #namespace = {"plat-chas-invmgr-ng-oper": "http://cisco.com/ns/yang/Cisco-IOS-XR-plat-chas-invmgr-ng-oper"}
  #namespace = 'http://cisco.com/ns/yang/Cisco-IOS-XR-plat-chas-invmgr-ng-oper'
  namespace = 'http://cisco.com/ns/yang/Cisco-IOS-XR-platform-oper'
  #select = '/Cisco-IOS-XR-platform-oper:platform/racks/rack/slots/slot/state/card-type'
  select = '/Cisco-IOS-XR-platform-oper:platform/racks/rack['rack-name']'
  #select = '/platform-oper:platform/platform-oper:racks/platform-oper:rack/platform-oper:slots/platform-oper:slot/platform-oper:state/platform-oper:card-type'
  #select = '/plat-chas-invmgr-ng-oper:platform/plat-chas-invmgr-ng-oper:racks/plat-chas-invmgr-ng-oper:rack/plat-chas-invmgr-ng-oper:slots/plat-chas-invmgr-ng-oper:slot[0]/plat-chas-invmgr-ng-oper:state/plat-chas-invmgr-ng-oper:card-type'
  #select = "/plat-chas-invmgr-ng-oper:platform/plat-chas-invmgr-ng-oper:racks/plat-chas-invmgr-ng-oper:rack/plat-chas-invmgr-ng-oper:slots/plat-chas-invmgr-ng-oper:slot"
  #select = "/plat-chas-invmgr-ng-oper:platform"
  #select = "/platform"
  
  reply = device.get(filter=("xpath", (namespace, select)))
  #reply = device.get('xpath', '/Cisco-IOS-XR-plat-chas-invmgr-ng-oper:platform/racks/rack/slots/slot1/state/card-type')#.data_xml
  #reply = device.get('xpath', 'plat-chas-invmgr-ng-oper:platform/plat-chas-invmgr-ng-oper:racks/plat-chas-invmgr-ng-oper:rack/plat-chas-invmgr-ng-oper:slots/plat-chas-invmgr-ng-oper:slot/plat-chas-invmgr-ng-oper:state/plat-chas-invmgr-ng-oper:card-type').data_xml
  #reply = device.get('xpath', 'plat-chas-invmgr-ng-oper:platform/plat-chas-invmgr-ng-oper:racks/plat-chas-invmgr-ng-oper:rack/plat-chas-invmgr-ng-oper:slots/plat-chas-invmgr-ng-oper:slot')#.data_xml
  
  
  #definisco un dizionario che, alla fine,  conterrà tutte le info relativa alla piattaforma.
  
  D = dict()
  
  #Questo ciclo for è il cuore del programma, mi crea un dizionario D con tutti i dati estratti dal device.
  
  for filename in os.listdir(path):
      if filename.endswith('.xml'):
              with open(os.path.join(path, filename), 'r') as g:
                  D[filename[:-4]] = netconfrequest(g.read(), device)
  
  
     
  mivpe015 = IOSXR(devicename, username, userpassword)
  mivpe015.setisisinstancename(D['showisisnei']['data']['isis']['instances']['instance']['instance-name'])
  print(mivpe015.isisinstancename)
  
  iosxr = VPE(D['showisisnei']['data']['isis']['instances']['instance']['instance-name'])
  print(iosxr.isisinstancename)
  
  
  #definisco una classe test che contiene un dizionario e un metodo per visualizzre il dizionario.
  #Questa classe prende come parametro il dizionartio D
  class TEST():
    def __init__(self, dict_test):
      self.dict_test = dict_test
    def visualizza_intero_dizionario(self,dict_test):
      print(self.dict_test)
    def visualizza_dizinario_isis(self,dict_test):
      print(self.dict_test['showisisnei'])
    def stato_del_protocollo_isis(self, dict_test):
      dizionrio_con_lo_stato_di_isis = {}
      dizionrio_con_lo_stato_di_isis['instance-name'] = dict_test['showisisnei']['data']['isis']['instances']['instance']['instance-name']
      dizionrio_con_lo_stato_di_isis['neighbor'] = dict_test['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']
      print(dizionrio_con_lo_stato_di_isis)
      
  vpe_test = TEST(D)
  #vpe_test.visualizza_intero_dizionario(D)
  #vpe_test.visualizza_dizinario_isis(D)
  vpe_test.stato_del_protocollo_isis(D)
  
  db = shelve.open('devicedb')
  for obj in (dev,nx):
    db[obj.name] = obj
  db.close()
  
  db = shelve.open('devicedb')
  print(len(db))
  print(list(db.keys()))
  
  for key in db:
    print(key, '=>', db[key])
    
  for key in sorted(db):
    print(key, '=>', db[key])
    
  
  
  #Stampo il dizionario su file .json
  
  if args.preorpost == 'pre':
      json.dump(D, fp = open('precheck.json', 'w'), indent = 4)
  elif args.preorpost == 'post':
      json.dump(D, fp = open('postcheck.json', 'w'), indent = 4)
  
      Precheck = json.load(open('precheck.json'))
      Postcheck = json.load(open('postcheck.json'))
      
      #print(os.system('diff precheck.json postcheck.json'))
  
      ListaKeysPrecheck = list(Postcheck.keys())
      ListaKeysPostcheck = list(Postcheck.keys())
  
      #print(type(ListaKeysPrecheck))
      #print(ListaKeysPrecheck)
  
      #print(type(ListaKeysPostcheck))
      #print(ListaKeysPostcheck)
  
      #print(Postcheck.keys())
      #print(Postcheck.keys())
      
      def scendidentroildizionario(dizion):
        ListaDelleChiavi = list(dizion.keys())
        for i in ListaDelleChiavi:
          if type(dizion[i]) is dict:
            scendidentroildizionario(dizion[i])
        return i
        
      #Confronta due dizionari e ritorna una lista con l'elenco delle chiavi degli elementi che differiscono
      def listadellechiaviko(d1,d2):
        ListaDelleChiavi = list(d1.keys())
        ListaDelleChiaviKO = []
        for i in ListaDelleChiavi:
          if d1[i] == d2[i]:
            pass
          else:
            ListaDelleChiaviKO.append(i)
        return ListaDelleChiaviKO
          
      #devi distinguere 4 diverse casistiche
      #Caso 1 ho un solo elemento nel precheck e 0 in postcheck ad esempio nel caso isis ho un sole neighbor nel Pre e zero nel Pro
      #Caso 2 ho due elementi nel precheck e uno nel postchek ad esempio nel caso isis ho due neighbor nel Pre e uno nel Pro
      #Caso 3 ho N elementi in precheck e M in post check  ad esempio nel caso di sisi avevo N neighbor nel Pre e M nel Post
      #Caso 4 ho N elementi nel pre e 0 nel post ad esempio nel casi di isis avevo N neigbor ma sono caduti tutti non viene gestito per il momento  
      def Confronta_Dizionari(d1,d2):
        if type(d1) is dict: #sono nel caso 1
          print('check ', l)
        else: #sono nel caso 2 o nel caso 3
          if type(d2) is dict: #sono nel caso 2
            for l in d1:
              if l != d2:
                print('check ', l)
          else: #sono nel caso 3
            for l in d1:
              if l not in d2:
                print('check ', l)
                
      
      #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Questa funzione non viene usata  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      #devi distinguere diverse casistiche
      #Caso 1 ho un solo neighbor isis in precheck e 0 in postcheck
      #Caso 2 ho due neighbor isis in precheck e uno in postchek
      #Caso 3 ho ne neighbor isis in precheck e m in post check, questo è il caso 
      def showisisnei(d1, d2):
        if type(Precheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']) is dict: #sono nel caso 1
          print('check ', l)
        else: #sono nel caso 2 o nel caso 3
          if type(Postcheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']) is dict: #sono nel caso 2
            for l in Precheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']:
              if l != Postcheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']:
                print('check ', l)
          else: #sono nel caso 3
            for l in Precheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']:
              if l not in Postcheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor']:
                print('check ', l)
            
        
      """  
      def confrontadizionari(d1,d2):
        ListaDelleChiavi = list(d1.keys())
        for i in ListaDelleChiavi:
          if type(d1[i]) is dict:
            confrontadizionari(d1[i],d2[i])
          else:
            if (type(d1[i]) is str) and (type(d2[i]) is str):
              pass
            elif (type(d1[i]) is list) and (type(d2[i] is str)):
              pass
            else:
              if (type(d1[i]) is list) and (type(d2[i] is list)):
                print('sono due list')
                for l in d1[i]:
                  if l not in d2[i]:
                    print('check', l)
      """
                    
      """
      def visitadizionari(dizionario1, dizionario2):
        ListaDelleChiavi = list(dizionario1.keys())
        for d in ListaDelleChiavi:
          if type(dizionario1[d]) is dict:
            visitadizionari(dizionario1[d],dizionario2[d])
          elif type(dizionario1[d]) is str:
            print(dizionario1[d])
          else:
            print('non ci sono')
            for l in dizionario1[d]:
              if l not in dizionario2[d]:
                print('check', l)
      """
      
  
      if Precheck == Postcheck:
        print('i due file json sono identici')
      else:
        
        print('Questo è l\'elenco delle chiavi degli elementi che differiscono:', end = '\n')
        print(listadellechiaviko(Precheck,Postcheck))
        
      if Precheck['showisisnei'] == Postcheck['showisisnei']:
        print('ISIS OK')
      else:
        print('ISIS KO')
        Confronta_Dizionari(Precheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor'],Postcheck['showisisnei']['data']['isis']['instances']['instance']['neighbors']['neighbor'])
        
      if Precheck['showinterfacestatus'] == Postcheck['showinterfacestatus']:
        print('INTERFACE OK')
      else:
        print('INTERFACE KO')
        #attenzione se non ci sono neighbor isis il programma va in errore per cui stiamo valutando di eliminare questo check
        Confronta_Dizionari(Precheck['showinterfacestatus']['data']['interfaces']['interface'], Postcheck['showinterfacestatus']['data']['interfaces']['interface'])
      
      if Precheck['showbgpvpv4unicastsummary'] == Postcheck['showbgpvpv4unicastsummary']:
        print('BGP VPNV4 OK')
      else:
        print('BGP VPNV4 KO')
        Confronta_Dizionari(Precheck['showbgpvpv4unicastsummary']['data']['bgp']['instances']['instance']['instance-active']['default-vrf']['afs']['af']['neighbor-af-table']['neighbor'],Postcheck['showbgpvpv4unicastsummary']['data']['bgp']['instances']['instance']['instance-active']['default-vrf']['afs']['af']['neighbor-af-table']['neighbor'])
      
      if Precheck['showbgpvpv6unicastsummary'] == Postcheck['showbgpvpv6unicastsummary']:
        print('BGP VPNV6 OK')
      else:
        print('BGP VPNV6 KO')
        Confronta_Dizionari(Precheck['showbgpvpv6unicastsummary']['data']['bgp']['instances']['instance']['instance-active']['default-vrf']['afs']['af']['neighbor-af-table']['neighbor'],Postcheck['showbgpvpv6unicastsummary']['data']['bgp']['instances']['instance']['instance-active']['default-vrf']['afs']['af']['neighbor-af-table']['neighbor'])
      
      if Precheck['showbundlebundleethernet'] == Postcheck['showbundlebundleethernet']:
        print('Bundle OK')
      else:
        print('Bundle KO')
        Confronta_Dizionari(Precheck['showbundlebundleethernet']['data']['bundles']['bundles']['bundle'], Postcheck['showbundlebundleethernet']['data']['bundles']['bundles']['bundle'])
      
      if Precheck['showplatform'] == Postcheck['showplatform']:
        print('MODULE OK')
      else:
        print('MODULE KO')
        Confronta_Dizionari(Precheck['showplatform']['data']['platform']['racks']['rack']['slots']['slot'],Postcheck['showplatform']['data']['platform']['racks']['rack']['slots']['slot'])
        
      if Precheck['showlacp'] == Postcheck['showlacp']:
        print('LACP OK')
      else:
        print('LACP KO')
        Confronta_Dizionari(Precheck['showlacp']['data']['lacp']['interfaces']['interface'], Postcheck['showlacp']['data']['lacp']['interfaces']['interface'])
      
  else:
      print('Devi scegliere pre o post')
  