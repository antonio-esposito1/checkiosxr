
# SCRIPT DI DEFINIZIONE DI:
# - ISTANZE DIZIONARI DI CLASSE Output_Dict: PER I DIZIONARI COMPLETI PRE e POST
# - ISTANZE DIZIONARI DI CLASSE dict_doppio (Dict_Changed) e dict_singolo (Dict_Changed): PER I DIZIONARI
#   DEEPDIFF DEI SINGOLI COMANDI
# - FUNZIONI DI CREAZIONE DELLE ISTANZE CITATE e DI SALVATAGGIO SU FILE

from confronto_definizioni import Output_Dict, dict_doppio, dict_singolo, export_dict_
import json
import yaml

# PATH dei file di pre/post e confronto
#file_pre = /path_di_pclick/file_di_precheck.json
file_pre = 'precheck.json'
#file_post =  /path_di_pclick/file_di_postcheck.json
file_post = 'postcheck.json'
confronto_json = 'file_json_di_confronto.txt'
confronto_yaml = 'file_yaml_di_confronto.txt'

def carica_dict():
# carico i dizionari json pre e post a partire dai file di output
    with open(file_pre, "r") as pre:
        pre = json.load(pre)
    with open(file_post,"r") as post:
        post = json.load(post)
    return pre, post


def genera_istanze(pre, post):
    # istanze della classe Output_Dict che saranno a loro volta parametri delle classi Two_part_Command_Diff / Single_part_Command_Diff:
    _pre = Output_Dict(pre)
    _post = Output_Dict(post)

    # istanze delle sotto classi dict_singolo(Dict_Changed) e dict_doppio(Dict_Changed)
    # con cui creo i dizionari delle differenze DeepDiff
    isis = dict_doppio(_pre.isisname, _pre.isisneigh, _post.isisname, _post.isisneigh, '\n\n- ISIS -\n')
    bgp4 = dict_doppio(_pre.bgp4afname, _pre.bgp4neigh, _post.bgp4afname, _post.bgp4neigh, '\n\n- BGP4 -\n')
    bgp6 = dict_doppio(_pre.bgp6afname, _pre.bgp6neigh, _post.bgp6afname, _post.bgp6neigh, '\n\n- BGP6 -\n')
    bundle = dict_singolo (_pre.bundle, _post.bundle, '\n\n- Bundle-Ethernet -\n')
    interfaces = dict_singolo(_pre.interfaces, _post.interfaces, '\n\n- Interfaces -\n')
    platform = dict_singolo(_pre.platform, _post.platform, '\n\n- Platform -\n')
    lacp = dict_singolo(_pre.lacp, _post.lacp, '\n\n- Lacp -\n')
    bgpvrf = dict_singolo(_pre.bgpvrf, _post.bgpvrf, '\n\n- BGP VRFs -\n')
    return isis, bgp4, bgp6, bundle,interfaces, platform, lacp, bgpvrf


def salva (lista_dizionari):
    # uso le funzioni di creazione dei dizionari a partire dai dati di confronto generati da DeepDiff
    # per generare i dizionari finali da stampare in json e da convertire in YAML
    rimossi = "\n----\nElementi rimossi, non presenti nel file POST:\n---------------------------------------------"
    cambiati = "\n----\nElementi con differenze tra file PRE e file POST:\n-------------------------------------------------"
    nessuno = "- Nessun elemento -\n\n"

    # ELEMENTI RIMOSSI
    # inizializzo i file
    with open(confronto_json, "w") as confronto_JSON:
        confronto_JSON.write(rimossi)
    with open(confronto_yaml, "w") as confronto_YAML:
        confronto_YAML.write(rimossi)

    for dizionario in lista_dizionari:
        if dizionario.DD.get('dictionary_item_removed'):
            tmp_removed = export_dict_(dizionario.DD['dictionary_item_removed'])
            # JSON
            removed = json.dumps(tmp_removed, indent=4)+'\n\n'
            # YAML
            removed_yaml = str(yaml.dump((tmp_removed), sort_keys=False))

            with open(confronto_json, "a") as confronto_JSON:
                confronto_JSON.write(dizionario.nome+removed)
            with open(confronto_yaml, "a") as confronto_YAML:
                confronto_YAML.write(dizionario.nome+removed_yaml) 
        else:
            with open(confronto_json, "a") as confronto_JSON:
                confronto_JSON.write(dizionario.nome+nessuno)
            with open(confronto_yaml, "a") as confronto_YAML:
                confronto_YAML.write(dizionario.nome+nessuno) 


    # ELEMENTI CAMBIATI
    with open(confronto_json, "a") as confronto_JSON:
        confronto_JSON.write(cambiati)
    with open(confronto_yaml, "a") as confronto_YAML:
        confronto_YAML.write(cambiati)
    
    for dizionario in lista_dizionari:
        if dizionario.DD.get('values_changed'):
            tmp_changed = export_dict_(dizionario.DD['values_changed'])
            # JSON
            changed = json.dumps(tmp_changed, indent=4)+'\n\n'
            # YAML
            changed_yaml = str(yaml.dump((tmp_changed), sort_keys=False))

            with open(confronto_json, "a") as confronto_JSON:
                confronto_JSON.write(dizionario.nome+changed)
            with open(confronto_yaml, "a") as confronto_YAML:
                confronto_YAML.write(dizionario.nome+changed_yaml) 
        else:
            with open(confronto_json, "a") as confronto_JSON:
                confronto_JSON.write(dizionario.nome+nessuno)
            with open(confronto_yaml, "a") as confronto_YAML:
                confronto_YAML.write(dizionario.nome+nessuno)           
            
               
# esecuzione dello script, serve come definizione di funzione da importare nel file di Antonio
def procedi ():
    pre, post = carica_dict()
    isis, bgp4, bgp6, bundle, interfaces, platform, lacp, bgpvrf = genera_istanze(pre, post)
    dict_list = [isis, bgp4, bgp6, bundle, interfaces, platform, lacp, bgpvrf]
    salva (dict_list)


