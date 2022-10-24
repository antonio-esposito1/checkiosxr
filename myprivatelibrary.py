import xmltodict
import json
import os

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