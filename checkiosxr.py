"""
L'obbiettivo di questo programma è raccogliere le informazioni da un cisco IOSXR per verificare il ripristino dei servizi dopo la procedura di upgrade.

il programma richiede di passare un argomento pre o post per:
  - se si sceglier pre allora vengono raccolti i dati e salvati in un file precheck.json.
  - se si sceglie post allora vengono raccolti i dati e salvati in un file postcheck.json e viene poi attivata un procedura per confrontare i due file precheck.jsoon e 
    postcheck.jsono

Le informazioni vengono raccolte dal device usando netconf quindi usiamo ncclient. il codice per fare la richiesta netconf al devide è racchiuso nel module myprivatelibrary nella funzione
netconfrequest che prende in ingresso due parametri:
 - Una stringa contenete il filtro xml da applicare alla richista 
 - device a cui applicare la richiesta. Nota che device è un oggetto che viene creato con ncclient

Nota che i filtri xml da applicare alla richiesta sono salvati nella cartella templatexml e vengono letti in sequenza grazie alla libreria os, L'ordine con cui vengono letti questi file 
è alfabetico


le seguenti informazioni sulle intrfacce e sui protocolli, abbiamo cercato di mantenere una corrispondenza tra le richieste netconf che facciamo al device e i comandi utlizzati 
sul device per visualizzare le stesse informazioni, questo perchè le persone del nostro gruppo sono sicuramente più abituate a ragionare in termini di comandi cli piuttoso che modelli
di YANG. Le seguenti informazioni verranno raccolte
- show isis neighbors
- show bgp vpnv4 unicast summary
- show bgp vpnv6 unicast summary
- show bundle bunde-eth 

"""

import xmltodict
import json
import os
from argparse import ArgumentParser
import getpass

from ncclient import manager

from myprivatelibrary import netconfrequest

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
device = manager.connect(host='v-mivpe015', port=830, username='EspositoA1', password='admin', hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)

D = dict()

path = 'templatexml'
for filename in os.listdir(path):
    if filename.endswith('.xml'):
            with open(os.path.join(path, filename), 'r') as g:
                D[filename[:-4]] = netconfrequest(g.read(), device)



if args.preorpost == 'pre':
    json.dump(D, fp = open('precheck.json', 'w'), indent = 4)
elif args.preorpost == 'post':
    json.dump(D, fp = open('postcheck.json', 'w'), indent = 4)

    Precheck = json.load(open('precheck.json'))
    Postcheck = json.load(open('postcheck.json'))

    print(Postcheck.keys())
    print(Postcheck.keys())

    if Precheck == Postcheck:
        print('i due file json sono identici')
    else:
        if Postcheck['showisisnei'] == Postcheck['showisisnei']:
          print('ISIS OK')
        else:
            print('ISIS KO')
        if Postcheck['showbgpvpv4unicastsummary'] == Postcheck['showbgpvpv4unicastsummary']:
          print('BGP VPNV4 OK')
        else:
            print('BGP VPNV4 KO')
        if Postcheck['showbgpvpv6unicastsummary'] == Postcheck['showbgpvpv6unicastsummary']:
          print('BGP VPNV6 OK')
        else:
            print('BGP VPNV6 KO')
        if Postcheck['showbundlebundleethernet'] == Postcheck['showbundlebundleethernet']:
          print('BUNDLE ETHERNET OK')
        else:
            print('BUNDLE ETHERNET KO')
        if Precheck['showinterfacestatus'] == Postcheck['showinterfacestatus']:
          print('INTERFACE OK')
        else:
          for l in Precheck['showinterfacestatus']['data']['interfaces']['interface']:
            if l not in Postcheck['showinterfacestatus']['data']['interfaces']['interface']:
              print('check questa interfaccia:', l)
else:
    print('Devi scegliere pre o post')
