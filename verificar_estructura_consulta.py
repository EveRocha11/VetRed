import pyodbc
from app.config import ConfigQuito

def verificar_estructura_consulta():
    """Verificar la estructura exacta de la tabla Consulta_Quito"""
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Ver la estructura completa de la tabla
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Consulta_Quito'
            ORDER BY ORDINAL_POSITION
        """)
        
        print("Estructura de Consulta_Quito:")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]} - {col[1]} - {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        # Ver una consulta específica para entender la relación
        cursor.execute("SELECT TOP 3 * FROM Consulta_Quito")
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        
        print(f"\nColumnas: {cols}")
        print("Datos de ejemplo:")
        for row in rows:
            print(f"  {row}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estructura_consulta()
