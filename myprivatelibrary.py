import xmltodict
import json
import os

import requests
import json
import getpass



from ncclient import manager

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


#Questa funzione prende in ingresso un comando, si collega in rest al nexus e restituisce l'outout de lcomando in formato json
"""
deviceip = input('deviceip: ')
switchuser = input('login: ')
switchpassword = getpass.getpass()

def nxapi(cmd):
    client_cert_auth=False
    client_cert='PATH_TO_CLIENT_CERT_FILE'
    client_private_key='PATH_TO_CLIENT_PRIVATE_KEY_FILE'
    ca_cert='PATH_TO_CA_CERT_THAT_SIGNED_NXAPI_SERVER_CERT'
    url='http://' + deviceip + '/ins'
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
        response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
    else:
        url='https://' + deviceip + '/ins'
        response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword),cert=(client_cert,client_private_key),verify=ca_cert).json()
    return response

"""