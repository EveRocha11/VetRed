import pyodbc
import logging
from .config import ConfigGuayaquil, ConfigQuito

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, conn_str: str, db_name: str, autocommit: bool = False):
        self.db_name = db_name
        try:
            self.conn = pyodbc.connect(conn_str, autocommit=autocommit)
            # Evita nested transactions en vistas distribuidas
            self.conn.cursor().execute("SET XACT_ABORT ON;")
            logger.info(f"✅ Conexión exitosa a {db_name}")
        except Exception as e:
            logger.error(f"❌ Error conectando a {db_name}: {e}")
            raise

    def cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        return self.conn.commit()
    
    def rollback(self):
        return self.conn.rollback()

    def close(self):
        self.conn.close()

    def test_connection(self):
        """Probar la conexión y obtener información del servidor"""
        try:
            cursor = self.cursor()
            cursor.execute("SELECT @@SERVERNAME as Servidor, DB_NAME() as BaseDatos")
            result = cursor.fetchone()
            cursor.close()
            return {"servidor": result[0], "base_datos": result[1]}
        except Exception as e:
            logger.error(f"Error probando conexión a {self.db_name}: {e}")
            return None

# Función para intentar conectar con manejo de errores
def create_database_connection(config_class, db_name):
    """Crear conexión con manejo de errores"""
    try:
        return Database(config_class.conn_str(), db_name)
    except Exception as e:
        logger.warning(f"No se pudo conectar a {db_name}: {e}")
        return None

# Instancias globales
logger.info("Inicializando conexiones de base de datos...")

# Conexión principal a Guayaquil (siempre debe funcionar)
db_guayaquil = create_database_connection(ConfigGuayaquil, "VetRedGuayaquil")

# Conexión opcional a Quito (puede fallar si no está disponible)
db_quito = create_database_connection(ConfigQuito, "VetRedQuito")

# Verificar conexiones
if db_guayaquil:
    guayaquil_info = db_guayaquil.test_connection()
    if guayaquil_info:
        logger.info(f"Guayaquil conectado: {guayaquil_info['servidor']}/{guayaquil_info['base_datos']}")

if db_quito:
    quito_info = db_quito.test_connection()
    if quito_info:
        logger.info(f"Quito conectado: {quito_info['servidor']}/{quito_info['base_datos']}")
else:
    logger.warning("Conexión a Quito no disponible - usando solo Guayaquil")
