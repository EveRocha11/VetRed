"""
Script para verificar la conexión a la base de datos de Quito
"""
from app.db import db_quito, db_guayaquil
from app.repositories.cliente_contacto import ClienteContactoRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_quito_connection():
    """Probar conexión a Quito y listar Cliente_Contacto"""
    try:
        logger.info("🔍 Probando conexión a VetRedQuito...")
        
        # Probar conexión directa
        cursor = db_quito.cursor()
        cursor.execute("SELECT @@SERVERNAME as Servidor, DB_NAME() as BaseDatos")
        result = cursor.fetchone()
        cursor.close()
        
        logger.info(f"✅ Conectado a: Servidor={result[0]}, Base de Datos={result[1]}")
        
        # Verificar si existe la tabla Cliente_Contacto
        cursor = db_quito.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Cliente_Contacto'
        """)
        table_exists = cursor.fetchone()[0]
        cursor.close()
        
        if table_exists:
            logger.info("✅ Tabla Cliente_Contacto existe en VetRedQuito")
            
            # Usar el repositorio para obtener datos
            repo = ClienteContactoRepository()
            clientes = repo.list()
            
            logger.info(f"📋 Encontrados {len(clientes)} registros en Cliente_Contacto:")
            for cliente in clientes[:5]:  # Mostrar los primeros 5
                logger.info(f"  - ID: {cliente.idCliente}, Email: {cliente.correo}, Dir: {cliente.direccion}")
                
        else:
            logger.error("❌ Tabla Cliente_Contacto NO existe en VetRedQuito")
            
    except Exception as e:
        logger.error(f"❌ Error conectando a Quito: {e}")
        logger.info("🔄 Intentando conectar a Guayaquil como respaldo...")
        
        try:
            cursor = db_guayaquil.cursor()
            cursor.execute("SELECT @@SERVERNAME as Servidor, DB_NAME() as BaseDatos")
            result = cursor.fetchone()
            cursor.close()
            logger.info(f"✅ Conectado a Guayaquil: Servidor={result[0]}, Base de Datos={result[1]}")
            
        except Exception as e2:
            logger.error(f"❌ Error también en Guayaquil: {e2}")

def test_cliente_info_guayaquil():
    """Verificar Cliente_Info en Guayaquil"""
    try:
        logger.info("\n🔍 Verificando Cliente_Info en Guayaquil...")
        
        cursor = db_guayaquil.cursor()
        cursor.execute("SELECT COUNT(*) FROM Cliente_Info")
        count = cursor.fetchone()[0]
        cursor.close()
        
        logger.info(f"✅ Cliente_Info en Guayaquil tiene {count} registros")
        
    except Exception as e:
        logger.error(f"❌ Error con Cliente_Info en Guayaquil: {e}")

if __name__ == "__main__":
    test_quito_connection()
    test_cliente_info_guayaquil()
    
    print("\n🎯 Resumen de configuración:")
    print("  - Cliente_Contacto: Base de datos Quito (servidor Geovanny)")
    print("  - Cliente_Info: Base de datos Guayaquil (servidor DESKTOP-N4G4IF1)")
    print("  - Login/Registro: usa Cliente_Info en Guayaquil")
    print("  - Gestión de contactos: usa Cliente_Contacto en Quito")
