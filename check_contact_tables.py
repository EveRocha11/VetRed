"""
Verificar qué tablas de contacto existen en cada base de datos
"""
from app.database_router import db_router

def check_contact_tables():
    """Verificar tablas de contacto en ambas bases"""
    
    print("🔍 VERIFICANDO TABLAS DE CONTACTO")
    print("=" * 50)
    
    # 1. Verificar en Guayaquil
    print("\n📋 En VetRedGuayaquil:")
    try:
        guayaquil_db = db_router.get_auth_db()  # Base de Guayaquil
        cursor = guayaquil_db.cursor()
        
        # Buscar tablas relacionadas con Cliente o Contacto
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            AND (TABLE_NAME LIKE '%Cliente%' OR TABLE_NAME LIKE '%Contacto%')
            ORDER BY TABLE_NAME
        """)
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"   - {table_name}")
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"     ({count} registros)")
            except:
                print(f"     (error contando)")
        
        cursor.close()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar en Quito
    print("\n📋 En VetRedQuito:")
    try:
        quito_db = db_router.get_cliente_contacto_db()  # Debería ser Quito
        cursor = quito_db.cursor()
        
        # Buscar tablas relacionadas con Cliente o Contacto
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            AND (TABLE_NAME LIKE '%Cliente%' OR TABLE_NAME LIKE '%Contacto%')
            ORDER BY TABLE_NAME
        """)
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"   - {table_name}")
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"     ({count} registros)")
            except:
                print(f"     (error contando)")
        
        cursor.close()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    check_contact_tables()
