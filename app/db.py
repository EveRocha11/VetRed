import pyodbc
from .config import Config

class Database:
    def __init__(self, conn_str: str, autocommit: bool = True):
        self.conn = pyodbc.connect(conn_str, autocommit=autocommit)
        # Evita nested transactions en vistas distribuidas
        self.conn.cursor().execute("SET XACT_ABORT ON;")

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

# Instancias globales (ajusta SERVER/DATABASE según necesites)
db_guayaquil = Database(Config.conn_str())
# Si quieres también Quito, haz otro Config con SERVER='Geovanny', DATABASE='VetRedQuito'
