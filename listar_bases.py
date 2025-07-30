"""
Script para listar las bases de datos disponibles
"""
import pyodbc
from app.config import Config

def list_databases():
    """Listar todas las bases de datos disponibles"""
    try:
        # Conectar a la base de datos master para listar todas las DB
        conn_str = (
            f"DRIVER={Config.DRIVER};"
            f"SERVER={Config.SERVER};"
            f"DATABASE=master;"  # Usar master para listar DBs
            f"UID={Config.UID};PWD={Config.PWD}"
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        print("🔍 Listando bases de datos disponibles...")
        cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")  # Excluir system DBs
        
        databases = cursor.fetchall()
        
        print("📋 Bases de datos encontradas:")
        for db in databases:
            print(f"  - {db[0]}")
        
        cursor.close()
        conn.close()
        
        # Ahora probar específicamente con VetRedGuayaquil
        print(f"\n🔍 Verificando contenido de VetRedGuayaquil...")
        
        guayaquil_conn_str = (
            f"DRIVER={Config.DRIVER};"
            f"SERVER={Config.SERVER};"
            f"DATABASE=VetRedGuayaquil;"
            f"UID={Config.UID};PWD={Config.PWD}"
        )
        
        conn = pyodbc.connect(guayaquil_conn_str)
        cursor = conn.cursor()
        
        # Listar tablas en VetRedGuayaquil
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        print("📋 Tablas en VetRedGuayaquil:")
        for table in tables:
            print(f"  - {table[0]}")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_databases()
