
# SCRIPT DI DEFINIZIONE DI:
# - CLASSE Output_Dict: DIZIONARIO I CUI ATTRIBUTI SONO I DIZIONARI DI OUTPUT DEI SINGOLI COMANDI
# - CLASSE Dict_Changed: CONTIENE IL METODO change_dict CHE VIENE EREDITATO DALLE CLASSI FIGLIE
# - CLASSI dict_doppio (Dict_Changed) e dict_singolo (Dict_Changed): DIZIONARI I CUI ATTRIBUTI SONO I DIZIONARI
#   MODIFICATI COME MI SERVE, IL DIZIONARIO DEEPDIFF ED IL NOME DEL COMANDO DI RIFERIMENTO
# - FUNZIONE export_dict_ PER GENERARE UN DIZIONARIO CLASSICO A PARTIRE DA QUELLO DELLE DIFFERENZE DEEPDIFF

from deepdiff import DeepDiff
import re

# CLASSI #
##########
# creo la classe i cui attributi sono i dizionari parziali di output, sia per il file PRE che per quello POST
class Output_Dict:
    def __init__(self, dizionario):
        self.isisname = dizionario.get('showisisnei').get('data').get('isis').get('instances').get('instance').get('instance-name')
        self.isisneigh = dizionario.get('showisisnei').get('data').get('isis').get('instances').get('instance').get('neighbors').get('neighbor')
        self.bgp4neigh = dizionario.get('showbgpvpv4unicastsummary').get('data').get('bgp').get('instances').get('instance').get('instance-active').get('default-vrf').get('afs').get('af').get('neighbor-af-table').get('neighbor')
        self.bgp4afname = dizionario.get('showbgpvpv4unicastsummary').get('data').get('bgp').get('instances').get('instance').get('instance-active').get('default-vrf').get('afs').get('af').get('af-name')
        self.bgp6neigh = dizionario.get('showbgpvpv6unicastsummary').get('data').get('bgp').get('instances').get('instance').get('instance-active').get('default-vrf').get('afs').get('af').get('neighbor-af-table').get('neighbor')
        self.bgp6afname = dizionario.get('showbgpvpv6unicastsummary').get('data').get('bgp').get('instances').get('instance').get('instance-active').get('default-vrf').get('afs').get('af').get('af-name')
        self.bundle = dizionario.get('showbundlebundleethernet').get('data').get('bundles').get('bundles').get('bundle')
        self.interfaces = dizionario.get('showinterfacestatus').get('data').get('interfaces').get('interface')
        self.platform = dizionario.get('showplatform').get('data').get('platform').get('racks').get('rack').get('slots').get('slot')
        self.lacp = dizionario.get('showlacp').get('data').get('lacp').get('interfaces').get('interface')
        self.bgpvrf = dizionario.get('showbgpvrfunicastsummary').get('data').get('bgp').get('instances').get('instance').get('instance-active').get('vrfs').get('vrf')


# Classe madre dove definisco la funzione di modifca/trasofrmazione dizionario parziale di output su cui voglio operare
# per ogni neighbor ISIS estraggo il system-id, neighbor BGP estraggo l'IP address, per ogni BE o Interface
# estraggo l'identificativo e lo faccio diventare la chiave per il dizionario che contiene il resto delle 
# informazioni del dizionario.
# Inoltre controllo se esiste uno o più elementi nel dizionario: (se uno solo allora db è dizionario, più di uno db è lista)
class Dict_Changed:
    def change_dict (self, database):
        dict_tmp = {}
        if isinstance(database, dict): #
            if 'bundle-interface' in database.keys():
                bundle = database['bundle-interface']
                database.pop('bundle-interface')
                dict_tmp[bundle] = database
            elif 'name' in database.keys(): # usato sia per interfacce che per lacp
                interface = database['name']
                database.pop('name')
                dict_tmp[interface] = database
            elif 'slot-name' in database.keys():
                slot = database['slot-name']
                database.pop('slot-name')
                slot = 'Slot_'+slot
                dict_tmp[slot] = database
            elif 'system-id' in database.keys(): 
                system_id = database['system-id']
                database.pop('system-id')
                dict_tmp[system_id] = database
            elif 'neighbor-address' in database.keys():
                indirizzoip = database['neighbor-address']
                database.pop('neighbor-address')
                dict_tmp[indirizzoip] = database
            elif 'afs' in database.keys():  #BGP VRFs
                indirizzoip = database.get('afs').get('af').get('af-name').get('neighbor-af-table').get('neighbor').get('neighbor-address')
                database['afs']['af']['neighbor-af-table']['neighbor'].pop('neighbor-address')
                vrf = database['vrf-name']
                dict_tmp[vrf] = {indirizzoip:instance['afs']['af']['neighbor-af-table']['neighbor']}    

        else: 
            for instance in database:
                if 'bundle-interface' in instance.keys():
                    bundle = instance['bundle-interface']
                    instance.pop('bundle-interface')
                    dict_tmp[bundle] = instance
                elif 'name' in instance.keys(): # usato sia per interfacce che per lacp
                        interface = instance['name']
                        instance.pop('name')
                        dict_tmp[interface] = instance
                elif 'slot-name' in instance.keys():
                    slot = instance['slot-name']
                    instance.pop('slot-name')
                    slot = 'Slot_'+slot 
                    dict_tmp[slot] = instance
                elif 'system-id' in instance.keys(): 
                    system_id = instance['system-id']
                    instance.pop('system-id')
                    dict_tmp[system_id] = instance
                elif 'neighbor-address' in instance.keys():
                    indirizzoip = instance['neighbor-address']
                    instance.pop('neighbor-address')
                    dict_tmp[indirizzoip] = instance
                elif 'afs' in instance.keys(): #BGP VRFs
                    indirizzoip = instance.get('afs').get('af').get('neighbor-af-table').get('neighbor').get('neighbor-address')
                    instance['afs']['af']['neighbor-af-table']['neighbor'].pop('neighbor-address')
                    vrf = instance['vrf-name']
                    dict_tmp[vrf] = {indirizzoip:instance['afs']['af']['neighbor-af-table']['neighbor']}
        return dict_tmp 


# creo le sotto classi di tipo Dict_Changed i cui attributi sono la trasformazione/preparazione del dizionario su cui voglio operare
# e la differenza trovata da DeepDeiff
class dict_doppio (Dict_Changed):
    def __init__(self, pre1, pre2, post1, post2, nome):
        self.pre = {pre1:self.change_dict(pre2)}
        self.post = {post1:self.change_dict(post2)}
        self.DD = DeepDiff(self.pre, self.post, verbose_level=2)
        self.nome = nome
    
class dict_singolo (Dict_Changed):
    def __init__(self, pre, post, nome):
        self.pre = self.change_dict(pre)
        self.post = self.change_dict(post)
        self.DD = DeepDiff(self.pre, self.post, verbose_level=2)
        self.nome = nome
    


# CREAZIONE DICT FINALI DELLE DIFFERENZE TROVATE DA DEEPDIFF #####
##################################################################

# a partire dal dizionario generato da DeepDiff creo un nuovo dizionario
# tramite le chiavi inserite nei path del dizionario DeepDiff
# ESEMPIO: 
# da questa unica chiave "root['vpnv4-unicast']['10.176.2.20']['connection-state']"
# viene creato il dizionario nestato: {"vpnv4-unicast": {"10.176.2.20": {"connection-state": {value}}}}

def export_dict_(database):
        tree = {} # db delle variazioni
        for key in database:      
            value = database[key] # valori cambiati per tipologia, o chiave, generata da DeepDiff
            if 'new_value' in value.keys():
                value['nuovo valore in POST --->'] = value.get('new_value')
                value['vecchio valore in PRE <--'] = value.get('old_value')
                value.pop('new_value')
                value.pop('old_value')
            sub = "\['(.*?)'\]" #pattern di ricerca chiavi
            subs = [] # lista delle chiavi trovate
            subs = re.findall(sub, key) #lista delle chiavi trovate
            tree_db = value # per ogni valore cambiato creo il dizionario tree_db parziale a partire dalle chiavi generate da DeepDiff
            for chiave in reversed(subs):   # per ogni chiave del dizionario DeepDiff creo un nuovo dizionario nested temporaneo
                tree_db = {chiave: tree_db}
            tree = dict(merge(tree_db, tree)) #creo il db tree delle variazioni facendo merge con il tree_db parziale
        return tree


# funzione ustata da export_dict
# controllo se le chiavi di due dict indentati corrispondono, altrimenti le unisco
def merge (dict1, dict2): # i parametri sono il dizionario delle variazioni temporaneo e quello totale che all'inizio è vuoto
    for chiave in set(dict1.keys()).union(dict2.keys()): # le chiavi dei due dizionari si fondono in un set dove ogni chiave è unica
        # se la chiave è presente in entrambi i dizionari allora controllo i loro valori
        if chiave in dict1 and chiave in dict2:
            # se il valore di ogni chiave dei due dizionari è un dizionario allora continuo ad iterare
            if isinstance(dict1[chiave], dict) and isinstance(dict2[chiave], dict): 
                yield (chiave, dict(merge(dict1[chiave], dict2[chiave])))
            # quando la chiave è presente solo in un dizionario allora ne prendo il valore
        elif chiave in dict1:
            yield (chiave, dict1[chiave])
        else:
            yield (chiave, dict2[chiave])
      





