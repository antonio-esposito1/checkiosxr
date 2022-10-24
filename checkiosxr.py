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

from ncclient import manager

#from myprivatelibrary import netconfrequest

"""
Questa funzione prende in ingresso due parametri:
 - Una stringa contenete il filtro xml da applicare alla richista
 - device a cui applicare la richiesta. Nota che device è un oggetto che viene creato con ncclient

"""

def netconfrequest(subtree_filter, device):

    #crea una string str_nc_get_reply contenete la risposta xml del device
    str_nc_get_reply = device.get(('subtree', subtree_filter)).data_xml
    
    #Crea un file di testo check.xml contenente la stringa con la risposta xml
    with open("%s.xml" % 'check', 'w') as f:
        f.write(str_nc_get_reply)
        f.close()
    
    #Converte xml in un OrdDictionary, una speciale classe di dizionario che non permette agli elementi di cambiare ordine, Questo serve perché nei file xml l'ordine è importante.
     
    with open('check.xml') as fxml:
        return xmltodict.parse(fxml.read())

class Device:
  def __init__(self, name, username, password):
    self.name = name
    self.username = username
    self.password = password

  def connect(self):
    return manager.connect(host=self.name, port=830, username=self.username, password=self.password, hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)

devicename = 'v-mivpe015'
username = 'EspositoA1'
userpassword = 'admin'

#devicename = input('devicename: ')
#username = input('login: ')
#userpassword = getpass.getpass()

dev = Device(devicename, username, userpassword)


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

device = dev.connect()

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
   
#definisco un dizionario che, alla fine,  conterrà tutte le info relativa alla piattaforma.

D = dict()

#Questo ciclo for è il cuore del programma, mi crea un dizionario D con tutti i dati estratti dal device.

for filename in os.listdir(path):
    if filename.endswith('.xml'):
            with open(os.path.join(path, filename), 'r') as g:
                D[filename[:-4]] = netconfrequest(g.read(), device)


#Stampo il dizionario su file .json

if args.preorpost == 'pre':
    json.dump(D, fp = open('precheck.json', 'w'), indent = 4)
elif args.preorpost == 'post':
    json.dump(D, fp = open('postcheck.json', 'w'), indent = 4)

    Precheck = json.load(open('precheck.json'))
    Postcheck = json.load(open('postcheck.json'))

    ListaKeysPrecheck = list(Postcheck.keys())
    ListaKeysPostcheck = list(Postcheck.keys())

    print(type(ListaKeysPrecheck))
    print(ListaKeysPrecheck)

    print(type(ListaKeysPostcheck))
    print(ListaKeysPostcheck)

    print(Postcheck.keys())
    print(Postcheck.keys())

    def visitadizionari(dizionario1, dizionario2):
      ListaDelleChiavi = list(dizionario1.keys())
      for d in ListaDelleChiavi:
        if type(dizionario1[d]) is dict:
          visitadizionari(dizionario1[d],dizionario2[d])
        elif type(dizionario1[d]) is str:
          pass
        else:
          print('non ci sono')
          for l in dizionario1[d]:
            if l not in dizionario2[d]:
              print('check', l)



    if Precheck == Postcheck:
        print('i due file json sono identici')
    else:
      for k1 in ListaKeysPrecheck:
        if Precheck[k1] == Postcheck[k1]:
          print(k1, 'is ok')
        else:
          print(k1, 'is not ok')
          visitadizionari(Precheck[k1],Postcheck[k1])
          print('************************************************************************')
          """
          ListaKeys2Precheck = list(Postcheck[k1].keys())
          print(ListaKeys2Precheck)
          for k2 in ListaKeys2Precheck:
            if Precheck[k1][k2] is dict:

            if Precheck[k1][k2] == Postcheck[k1][k2]:
              print(k2, 'is ok')
            else:
              print(k2, 'is not ok') 
          """         
        """
        if Precheck['showisisnei'] == Postcheck['showisisnei']:
          print('ISIS OK')
        else:
            print('ISIS KO')
        if Precheck['showbgpvpv4unicastsummary'] == Postcheck['showbgpvpv4unicastsummary']:
          print('BGP VPNV4 OK')
        else:
            print('BGP VPNV4 KO')
        if Precheck['showbgpvpv6unicastsummary'] == Postcheck['showbgpvpv6unicastsummary']:
          print('BGP VPNV6 OK')
        else:
            print('BGP VPNV6 KO')
        
        if Precheck['showbundlebundleethernet'] == Postcheck['showbundlebundleethernet']:
          print('BUNDLE ETHERNET OK')
        else:
            print('BUNDLE ETHERNET KO')
        
        if Precheck['showinterfacestatus'] == Postcheck['showinterfacestatus']:
          print('INTERFACE OK')
        else:
          for l in Precheck['showinterfacestatus']['data']['interfaces']['interface']:
            if l not in Postcheck['showinterfacestatus']['data']['interfaces']['interface']:
              print('check questa interfaccia:', l)
        
        if Precheck['showplatform'] == Postcheck['showplatform']:
          print('MODULE OK')
        else:
          for l in Precheck['showplatform']['data']['platfomr']['racks']['slots']['slot']:
            if l not in Postcheck['showplatform']['data']['platfomr']['racks']['slots']['slot']:
              print('check questo modulo:', l)
        
        if Precheck['showlacp'] == Postcheck['showlacp']:
          print('LACP OK')
        else:
          for l in Precheck['showlacp']['data']['lacp']['interfaces']['interface']:
            if l not in Postcheck['showlacp']['data']['lacp']['interfaces']['interface']:
              print('check questo lacp:', l)
        """
else:
    print('Devi scegliere pre o post')
