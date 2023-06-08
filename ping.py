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
    
    count = 0 # nombre de ping
    data = [] # liste vide dans laquelle on stockera nos temps de réponse
    while count < duree: # tant que nombre de ping voulu non atteint
        # on exécute dans la console la commande pour faire un ping tcp
        ping = subprocess.run(f'python {getcwd()}/tcpping.py {host} {port} 1', shell=True, capture_output=True)
        try:
            response_time = ping.stdout.decode().split("time=")[1].split(" ")[0] # on récupère la sortie dans la console en filtrant pour ne récupérer que le temps de réponse
            print(f'Temps de réponse : {response_time} ms') # On affiche le résultat
            data.append(response_time) # on ajoute le temps de réponse dans la liste
            time.sleep(1) # on marque un temps d'arrêt d'une seconde
        except IndexError:
            # si erreur de connexion
            print(f"Erreur de connexion à l'adresse {host}:{port}") # on affiche qu'il y a eu une erreur
            data.append(-1) # on ajoute -1 comme temps de réponse
            break
        count += 1
    return data
