import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil

def verificar_vistas_existentes():
    """Verificar qué vistas existen en las bases de datos"""
    
    print("🔍 VERIFICANDO VISTAS EXISTENTES...")
    
    try:
        # VERIFICAR VISTAS EN QUITO
        print("\n📊 Verificando vistas en base de datos de Quito...")
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        # Listar todas las vistas
        cursor.execute("""
            SELECT TABLE_NAME, TABLE_TYPE 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'VIEW'
            ORDER BY TABLE_NAME
        """)
        vistas_quito = cursor.fetchall()
        
        print("  Vistas disponibles en Quito:")
        for vista in vistas_quito:
            print(f"    - {vista[0]}")
        
        # Verificar estructura de vista Consulta si existe
        try:
            cursor.execute("SELECT TOP 1 * FROM dbo.Consulta")
            columns = [desc[0] for desc in cursor.description]
            print(f"\n  📋 Columnas de vista dbo.Consulta en Quito: {columns}")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM dbo.Consulta")
            count = cursor.fetchone()[0]
            print(f"  📊 Total registros en vista Consulta: {count}")
            
            # Ver algunos registros de hoy
            cursor.execute("SELECT COUNT(*) FROM dbo.Consulta WHERE fecha = '2025-07-30'")
            count_hoy = cursor.fetchone()[0]
            print(f"  📅 Registros para hoy (2025-07-30): {count_hoy}")
            
        except Exception as e:
            print(f"  ❌ Error accediendo a vista Consulta en Quito: {e}")
        
        # Verificar vista Empleado si existe
        try:
            cursor.execute("SELECT TOP 1 * FROM dbo.Empleado")
            columns_emp = [desc[0] for desc in cursor.description]
            print(f"\n  👥 Columnas de vista dbo.Empleado en Quito: {columns_emp}")
            
            cursor.execute("SELECT COUNT(*) FROM dbo.Empleado")
            count_emp = cursor.fetchone()[0]
            print(f"  📊 Total empleados en vista: {count_emp}")
            
        except Exception as e:
            print(f"  ❌ Error accediendo a vista Empleado en Quito: {e}")
        
        cursor.close()
        conn_quito.close()
        
        # VERIFICAR VISTAS EN GUAYAQUIL
        print("\n📊 Verificando vistas en base de datos de Guayaquil...")
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            # Listar todas las vistas
            cursor.execute("""
                SELECT TABLE_NAME, TABLE_TYPE 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'VIEW'
                ORDER BY TABLE_NAME
            """)
            vistas_guayaquil = cursor.fetchall()
            
            print("  Vistas disponibles en Guayaquil:")
            for vista in vistas_guayaquil:
                print(f"    - {vista[0]}")
            
            # Verificar estructura de vista Consulta si existe
            try:
                cursor.execute("SELECT TOP 1 * FROM dbo.Consulta")
                columns = [desc[0] for desc in cursor.description]
                print(f"\n  📋 Columnas de vista dbo.Consulta en Guayaquil: {columns}")
                
                # Contar registros
                cursor.execute("SELECT COUNT(*) FROM dbo.Consulta")
                count = cursor.fetchone()[0]
                print(f"  📊 Total registros en vista Consulta: {count}")
                
                # Ver algunos registros de hoy
                cursor.execute("SELECT COUNT(*) FROM dbo.Consulta WHERE fecha = '2025-07-30'")
                count_hoy = cursor.fetchone()[0]
                print(f"  📅 Registros para hoy (2025-07-30): {count_hoy}")
                
            except Exception as e:
                print(f"  ❌ Error accediendo a vista Consulta en Guayaquil: {e}")
            
            # Verificar vista Empleado si existe
            try:
                cursor.execute("SELECT TOP 1 * FROM dbo.Empleado")
                columns_emp = [desc[0] for desc in cursor.description]
                print(f"\n  👥 Columnas de vista dbo.Empleado en Guayaquil: {columns_emp}")
                
                cursor.execute("SELECT COUNT(*) FROM dbo.Empleado")
                count_emp = cursor.fetchone()[0]
                print(f"  📊 Total empleados en vista: {count_emp}")
                
            except Exception as e:
                print(f"  ❌ Error accediendo a vista Empleado en Guayaquil: {e}")
            
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"  ❌ Error conectando a Guayaquil: {e}")
        
        print("\n✅ Verificación de vistas completada")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    verificar_vistas_existentes()
