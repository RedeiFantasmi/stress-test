from sat import sat # on inclu la fonction sat du fichier sat.py
from ping import ping # on inclut la fonction ping du fichier ping.py
import threading # on inclut la bibliothèque threading (pour exécuter plusieurs script en parallèle)
from time import sleep # on inclut la fonction sleep de la bibliothèque time (pour marquer des temps d'arrêt dans le code)
import argparse # pour récupérer des paramètres dans la ligne de commande
import sys
from db_connect import DbDAO

parser = argparse.ArgumentParser() # on charge le composant pour gérer les arguments

group = parser.add_mutually_exclusive_group() # on crée un groupe qui interdit deux arguments d'être utilisés en même temps
group.add_argument('-C', '--configs', action='store_true', help='retourne la liste de paramétrages')
group.add_argument('-c', '--config', type=int, help='sélectionne un paramétrage à utiliser avec le programme')

parser.add_argument('-H', '--host', type=str, help="l'hôte qu'il faudra saturer")
# parser.add_argument('-p', '--port', type=int, nargs=3, help="les 3 ports à ping séparés par un espace")
# parser.add_argument('-d', '--duration', type=int, help="la durée en secondes du ping pour chaque port")

args = parser.parse_args() # on interprète les arguments de la ligne de commande

db_conn = DbDAO() # Classe pour se connecter à la BDD

config = {}
error = ''

if args.configs: # si on a mis -C ou --configs
    configs = db_conn.fetchConfigs() # on récupère tous les paramétrages
    for i in range(len(configs)):
        config = configs[i]
        print(f'{config["id"]} - {config["name"]} ({config["p1"]}, {config["p2"]}, {config["p3"]})') # on affiche un message de type [id de la config] - [nom de la config] (port1, port2, port3)
    sys.exit() # on quitte le programme, on veut uniquement afficher la liste de configs
elif args.config and args.host: # si on a choisi une config avec -c ou --config et renseigné un hôte
    config = db_conn.fetchConfigData(args.config) # on récupère les informations du paramétrage
    config["host"] = args.host


##### Amélioration possible, permettre de réaliser un test sans se baser sur un scénario

# elif args.host and len(args.port) == 3 and args.duration: # sinon, si on a rentré toutes les informations manuellement
#     port_ids = db_conn.fetchIdsFromPorts(args.port) # on récupère les id à partir du numéro de port
#     if len(port_ids) != 3: # si un port non-renseigné dans la BDD a été saisi, on va renvoyer une erreur
#         error = 'Les trois ports ne sont pas enregistrés dans notre base de données'

#     try:

#         config["host"] = args.host
#         config["p1"] = args.port[0]
#         config["p1_id"] = port_ids[0][0]
#         config["p2"] = args.port[1]
#         config["p2_id"] = port_ids[1][0]
#         config["p3"] = args.port[2]
#         config["p3_id"] = port_ids[2][0]
#         config["duration"] = args.duration
#     except:
#         print("Quelque chose s'est mal passé :") 
else :
    error = "Il manque des arguments (soit un host et un paramétrage soit un host, les 3 ports et une durée)"

if (error != ''):
    print(error)


# print(config)



def test(duree, port, host):
    # Début Saturation
    print(f'------------------------ Début de la saturation du port {port} ------------------------')
    # on crée un thread (le code s'exécute sur une autre partie du processeur) pour que la saturation puisse s'effectuer en parallèle du ping
    download_thread = threading.Thread(target=sat, args=(duree, port, host))
    download_thread.start()
    
    # Début mesure du ping
    res = ping(duree, port, host) # on récupère les résultats du ping dans une variable
    print(f'------------------------ Fin de la saturation du port {port} ------------------------')
    sleep(2) # on attend 2 secondes pour une meilleure lisibilité
    return res

if (error == ''):
    data = {} # dictionnaire vide
    data["scenario_id"] = args.config
    # for port in [config["p1"], config["p2"], config["p3"]]: # pour chaque port
    #     port_mesures = test(10, port, config["host"]) # on récupère dans une variable les mesures effectuées sur le port
        
    #     data[port] = port_mesures # on les mets dans le dictionnaire

    for i in range (1, 4):
        port = f"p{i}"
        port_mesures = test(config["duration"], config[port], config["host"])
        data[port] = { "id": config[f"{port}_id"], "mesures": port_mesures }
    print(data) # pour le moment on affiche. Plus tard, insertion dans la base de données
    db_conn.sendData(data)

