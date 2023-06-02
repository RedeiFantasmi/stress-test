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
        conn = self.connect()
        cur = conn.cursor()
        test_id = self.createTest(cur, data["scenario_id"])
        print(test_id)
        
        for i in range(1, 4):
            port_id = data[f"p{i}"]["id"]
            mesures = data[f"p{i}"]["mesures"]
            for j in range(len(mesures)):
                query = f"INSERT INTO logs (test_id, num_ping, ping, port_id) VALUES ({test_id}, {j}, {mesures[j]}, {port_id})"
                cur.execute(query)
        conn.commit()
        conn.close()

    def createTest(self, cursor, scenario_id):
        query = f"INSERT INTO test (scenario_id) VALUES ({scenario_id})"
        cursor.execute(query)
        return cursor.lastrowid


    def selectQuery(self, query, all, dict):
        conn = self.connect()
        if (dict):
            cur = conn.cursor(pymysql.cursors.DictCursor)
        else:
            cur = conn.cursor()
        cur.execute(query)
        if (all):
            rows = cur.fetchall()
        else:
            rows = cur.fetchone()
        conn.close
        return rows

    def fetchConfigs(self):
        query = "SELECT scenario.id, scenario.name, port1.port_number AS p1, port2.port_number AS p2, port3.port_number AS p3 FROM scenario INNER JOIN port AS port1 ON scenario.p1_id = port1.id INNER JOIN port AS port2 ON scenario.p2_id = port2.id INNER JOIN port AS port3 ON scenario.p3_id = port3.id"
        return self.selectQuery(query, True, True)
    
    def fetchConfigData(self, id):
        query = f"SELECT scenario.*, port1.port_number AS p1, port2.port_number AS p2, port3.port_number AS p3 FROM scenario INNER JOIN port AS port1 ON scenario.p1_id = port1.id INNER JOIN port AS port2 ON scenario.p2_id = port2.id INNER JOIN port AS port3 ON scenario.p3_id = port3.id WHERE scenario.id = {id}"
        return self.selectQuery(query, False, True)
    
    def fetchIdsFromPorts(self, ports):
        query = f"SELECT id FROM port WHERE port_number IN ({ports[0]}, {ports[1]}, {ports[2]})"
        return self.selectQuery(query, True, False)
