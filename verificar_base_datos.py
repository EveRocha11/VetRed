import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil

def verificar_base_datos():
    """Verificar qué tablas y datos existen en la base de datos"""
    
    print("=== VERIFICANDO BASE DE DATOS QUITO ===")
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tablas = cursor.fetchall()
        print("Tablas disponibles en VetRedQuito:")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        # Verificar datos en tablas específicas
        tablas_importantes = ['Empleado', 'Consulta', 'Cliente_Info', 'Mascota', 'Cliente']
        
        for tabla in tablas_importantes:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"\n{tabla}: {count} registros")
                
                if count > 0 and count < 20:  # Solo mostrar algunos registros
                    cursor.execute(f"SELECT TOP 5 * FROM {tabla}")
                    rows = cursor.fetchall()
                    cols = [desc[0] for desc in cursor.description]
                    print(f"  Columnas: {', '.join(cols)}")
                    print("  Primeros registros:")
                    for row in rows:
                        print(f"    {row}")
                        
            except Exception as e:
                print(f"{tabla}: No existe o error - {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a Quito: {e}")
    
    print("\n=== VERIFICANDO BASE DE DATOS GUAYAQUIL ===")
    try:
        conn = pyodbc.connect(ConfigGuayaquil.conn_str())
        cursor = conn.cursor()
        
        # Listar todas las tablas
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tablas = cursor.fetchall()
        print("Tablas disponibles en VetRedGuayaquil:")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        # Verificar datos en tablas específicas
        for tabla in tablas_importantes:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"\n{tabla}: {count} registros")
                
                if count > 0 and count < 20:
                    cursor.execute(f"SELECT TOP 5 * FROM {tabla}")
                    rows = cursor.fetchall()
                    cols = [desc[0] for desc in cursor.description]
                    print(f"  Columnas: {', '.join(cols)}")
                    print("  Primeros registros:")
                    for row in rows:
                        print(f"    {row}")
                        
            except Exception as e:
                print(f"{tabla}: No existe o error - {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a Guayaquil: {e}")

if __name__ == "__main__":
    verificar_base_datos()
