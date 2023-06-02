import time
import subprocess # on importe la bibliothèque qui permet de créer des processus
from os import getcwd # on importe la fonction getcwd de la bibliothèque os pour obtenir le chemin du dossier dans lequel est le script

def ping(duree, port, host):
    """Fonction qui initie le ping sur le port TCP voulu

    Args:
        duree (int): durée de l'opération
        port (int): port TCP sur lequel exécuter un ping
        host (string): hôte sur lequel effectuer un ping

    Returns:
        list: liste des temps de réponse (en ms) pendant la période désirée
    """

    timer = time.time() + duree # timer = heure actuelle + durée (en secondes)
    data = [] # liste vide dans laquelle on stockera nos temps de réponse
    while timer > time.time(): # tant que heure actuelle < timer
        # on exécute dans la console la commande pour faire un ping tcp
        ping = subprocess.run(f'python {getcwd()}/tcpping.py {host} {port} 1', shell=True, capture_output=True)
        print(f'{getcwd()}/tcpping.py {host} {port} 1')
        try:
            output = ping.stdout # on récupère la sortie dans la console
            response_time = output.decode().split("time=")[1].split(" ")[0] # on récupère uniquement la partie qui nous intéresse (temps de réponse en ms)
            data.append(response_time) # on ajoute le temps de réponse dans la liste
            time.sleep(1) # on fait une pause d'une seconde
        except IndexError as error:
            # si erreur de connexion, on renvoi erreur et on arrête le script
            data = f"Erreur de connexion à l'adresse {host}:{port}"
            break
    return data

# def ping(duree, port, host):
#     count = 0
#     maxCount = duree # timer = heure actuelle + durée (en secondes)
#     data = []
#     while count < maxCount: # tant que heure actuelle < timer
#         ping = subprocess.run(f'{getcwd()}/tcpping.py {host} {port} 1', shell=True, capture_output=True)
#         try:
#             response_time = ping.stdout.decode().split("time=")[1].split(" ")[0]
#             # print(f'Response time: {response_time} ms')
#             data.append(response_time)
#             time.sleep(1)
#         except IndexError:
#             data = f"Erreur de connexion à l'adresse {host}:{port}"
#             break
#         count += 1
#     return data