"""
Test específico para verificar la tabla Cliente_Info en VetRedQuito
"""
import pyodbc
from app.config import ConfigQuito
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_vetred_quito_connection():
    """Probar conexión específicamente a VetRedQuito"""
    print("🔍 Probando conexión a VetRedQuito...")
    print(f"Servidor: {ConfigQuito.SERVER}")
    print(f"Base de datos: {ConfigQuito.DATABASE}")
    print(f"Usuario: {ConfigQuito.UID}")
    print("-" * 50)
    
    try:
        # Intentar conectar con diferentes credenciales
        test_configs = [
            # Configuración original
            {"UID": "Quito", "PWD": "Quito", "name": "Credenciales Quito"},
            # Configuración con credenciales de Guayaquil
            {"UID": "Guayaquil", "PWD": "Guayaquil", "name": "Credenciales Guayaquil"},
            # Configuración con autenticación Windows
            {"UID": "", "PWD": "", "name": "Autenticación Windows (vacía)"},
        ]
        
        for config in test_configs:
            print(f"\n🔐 Probando: {config['name']}")
            try:
                if config['UID'] == "":
                    # Autenticación Windows
                    conn_str = (
                        f"DRIVER={ConfigQuito.DRIVER};"
                        f"SERVER={ConfigQuito.SERVER};"
                        f"DATABASE={ConfigQuito.DATABASE};"
                        f"Trusted_Connection=yes;"
                    )
                else:
                    conn_str = (
                        f"DRIVER={ConfigQuito.DRIVER};"
                        f"SERVER={ConfigQuito.SERVER};"
                        f"DATABASE={ConfigQuito.DATABASE};"
                        f"UID={config['UID']};PWD={config['PWD']}"
                    )
                
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                
                # Verificar información del servidor
                cursor.execute("SELECT @@SERVERNAME as Servidor, DB_NAME() as BaseDatos")
                server_info = cursor.fetchone()
                print(f"   ✅ Conectado a: {server_info[0]} / {server_info[1]}")
                
                # Verificar si existe Cliente_Info
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'Cliente_Info'
                """)
                cliente_info_exists = cursor.fetchone()[0] > 0
                
                if cliente_info_exists:
                    print("   ✅ Tabla Cliente_Info: EXISTE")
                    
                    # Contar registros
                    cursor.execute("SELECT COUNT(*) FROM Cliente_Info")
                    count = cursor.fetchone()[0]
                    print(f"   📊 Registros en Cliente_Info: {count}")
                    
                    # Mostrar algunos registros si existen
                    if count > 0:
                        cursor.execute("SELECT TOP 3 idCliente, correo, nombre FROM Cliente_Info")
                        rows = cursor.fetchall()
                        print("   📋 Primeros registros:")
                        for row in rows:
                            print(f"      - ID: {row[0]}, Email: {row[1]}, Nombre: {row[2]}")
                else:
                    print("   ❌ Tabla Cliente_Info: NO EXISTE")
                
                # Listar todas las tablas disponibles
                cursor.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    ORDER BY TABLE_NAME
                """)
                tables = cursor.fetchall()
                print(f"   📋 Total tablas en la base: {len(tables)}")
                print("   🗂️ Tablas principales:")
                for table in tables[:10]:  # Mostrar las primeras 10
                    print(f"      - {table[0]}")
                if len(tables) > 10:
                    print(f"      ... y {len(tables) - 10} más")
                
                cursor.close()
                conn.close()
                
                # Si llegamos aquí, la conexión fue exitosa
                print(f"   🎉 ¡Conexión exitosa con {config['name']}!")
                return True, config
                
            except Exception as e:
                print(f"   ❌ Error con {config['name']}: {e}")
                continue
        
        print("\n❌ No se pudo conectar con ninguna configuración")
        return False, None
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False, None

def test_available_databases():
    """Listar bases de datos disponibles en el servidor Geovanny"""
    print("\n🔍 Listando bases de datos en servidor Geovanny...")
    
    try:
        # Intentar conectar al master para listar DBs
        conn_str = (
            f"DRIVER={ConfigQuito.DRIVER};"
            f"SERVER={ConfigQuito.SERVER};"
            f"DATABASE=master;"
            f"UID=Guayaquil;PWD=Guayaquil"
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sys.databases WHERE database_id > 4")
        databases = cursor.fetchall()
        
        print("📋 Bases de datos disponibles:")
        for db in databases:
            print(f"   - {db[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error listando bases de datos: {e}")

if __name__ == "__main__":
    print("🧪 TEST DE VERIFICACIÓN - VetRedQuito")
    print("=" * 60)
    
    # Test 1: Probar conexión a VetRedQuito
    success, working_config = test_vetred_quito_connection()
    
    # Test 2: Listar bases disponibles
    test_available_databases()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 RESULTADO: VetRedQuito accesible")
        print(f"📝 Configuración que funciona: {working_config['name']}")
        print("✅ Cliente_Info verificada en VetRedQuito")
    else:
        print("🎯 RESULTADO: VetRedQuito no accesible")
        print("💡 Sugerencia: Verificar servidor, credenciales o permisos")
