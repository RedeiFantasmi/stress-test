import pymysql as db
import pymysql.cursors

class DbDAO():
    def __init__(self):
        """Initialisation des informations de connexion

        """
        
        self.user = 'michele'
        self.pwd = 'loup'
        self.host = 'projet-slam.freeboxos.fr'
        self.database = 'projet'
        self.port = 3306
    
    def connect(self):
        """Connexion à la base de données

        Returns:
            pymysql.connections.Connection: connexion à la BDD
        """
        
        return db.connect(host=self.host, user=self.user, password=self.pwd, database=self.database, port=self.port)
    
    def sendData(self, data):
        """Envoi des données en base

        Args:
            data (dict): liste des mesures par port
        """
        
        conn = self.connect()
        cur = conn.cursor()
        test_id = self.createTest(cur, data["scenario_id"]) # création du test
        
        for i in range(1, 4):
            port_id = data[f"p{i}"]["id"]
            mesures = data[f"p{i}"]["mesures"]
            for j in range(len(mesures)):
                query = f"INSERT INTO logs (test_id, num_ping, ping, port_id) VALUES ({test_id}, {j + 1}, {mesures[j]}, {port_id})"
                cur.execute(query)
        conn.commit()
        conn.close()

    def createTest(self, cursor, scenario_id):
        """Crée un nouveau test dans la BDD

        Args:
            cursor (pymysql.cursor): curseur d'accès à la BDD
            scenario_id (int): id du paramétrage choisi

        Returns:
            int: id du test créé
        """
        
        query = f"INSERT INTO test (scenario_id) VALUES ({scenario_id})" # requête d'insertion des données
        cursor.execute(query) # exécution de la requête
        return cursor.lastrowid # renvoi de l'id


    def selectQuery(self, query, all, dict):
        """Exécute une requête de type select

        Args:
            query (string): requête à exécuter
            all (bool): récupérer toutes les lignes ou une seule ?
            dict (bool): récupérer les données sous forme de tableau associatif ?

        Returns:
            array: liste des valeurs récupérées
        """
        
        conn = self.connect()
        if (dict):
            cur = conn.cursor(pymysql.cursors.DictCursor) # curseur pour récupérer un tableau associatif
        else:
            cur = conn.cursor() # curseur normal
        cur.execute(query) # exécution de la requête
        if (all):
            rows = cur.fetchall() # récupération de toutes les lignes
        else:
            rows = cur.fetchone() # récupération d'une seule ligne
        conn.close()
        return rows

    def fetchConfigs(self):
        """Récupère la liste des paramétrages

        Returns:
            array: liste des paramétrages
        """
        
        query = "SELECT scenario.id, scenario.name, port1.port_number AS p1, port2.port_number AS p2, port3.port_number AS p3 FROM scenario INNER JOIN port AS port1 ON scenario.p1_id = port1.id INNER JOIN port AS port2 ON scenario.p2_id = port2.id INNER JOIN port AS port3 ON scenario.p3_id = port3.id"
        return self.selectQuery(query, True, True)
    
    def fetchConfigData(self, id):
        """Récupère les données d'un paramétrage

        Args:
            id (int): id du paramétrage voulu

        Returns:
            dict: dictionnaire des données du paramétrage
        """
        
        query = f"SELECT scenario.*, port1.port_number AS p1, port2.port_number AS p2, port3.port_number AS p3 FROM scenario INNER JOIN port AS port1 ON scenario.p1_id = port1.id INNER JOIN port AS port2 ON scenario.p2_id = port2.id INNER JOIN port AS port3 ON scenario.p3_id = port3.id WHERE scenario.id = {id}"
        return self.selectQuery(query, False, True)
    
    def fetchIdsFromPorts(self, ports):
        """Récupère le numéro de port à partir de son libellé

        Args:
            ports (array): liste des ports

        Returns:
            tuple: tuple des id correspondants aux ports
        """
        
        query = f"SELECT id FROM port WHERE port_number IN ({ports[0]}, {ports[1]}, {ports[2]})"
        return self.selectQuery(query, True, False)
