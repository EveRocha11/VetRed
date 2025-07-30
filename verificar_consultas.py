import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil
from datetime import date

def verificar_consultas():
    """Verificar qué consultas específicas existen para los empleados"""
    
    print("=== CONSULTANDO CONSULTAS EN QUITO ===")
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Ver estructura de Consulta_Quito
        cursor.execute("SELECT TOP 10 * FROM Consulta_Quito")
        rows = cursor.fetchall()
        if rows:
            cols = [desc[0] for desc in cursor.description]
            print(f"Columnas de Consulta_Quito: {', '.join(cols)}")
            print("Primeras consultas:")
            for row in rows:
                print(f"  {row}")
        else:
            print("No hay consultas en Consulta_Quito")
        
        # Ver empleados disponibles
        print("\nEmpleados en Quito:")
        cursor.execute("SELECT idEmpleado, nombre FROM Empleado_Quito")
        empleados = cursor.fetchall()
        for emp in empleados:
            print(f"  ID {emp[0]}: {emp[1]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n=== CONSULTANDO CONSULTAS EN GUAYAQUIL ===")
    try:
        conn = pyodbc.connect(ConfigGuayaquil.conn_str())
        cursor = conn.cursor()
        
        # Ver estructura de Consulta_Guayaquil
        cursor.execute("SELECT TOP 10 * FROM Consulta_Guayaquil")
        rows = cursor.fetchall()
        if rows:
            cols = [desc[0] for desc in cursor.description]
            print(f"Columnas de Consulta_Guayaquil: {', '.join(cols)}")
            print("Primeras consultas:")
            for row in rows:
                print(f"  {row}")
        else:
            print("No hay consultas en Consulta_Guayaquil")
        
        # Ver empleados disponibles
        print("\nEmpleados en Guayaquil:")
        cursor.execute("SELECT idEmpleado, nombre FROM Empleado_Guayaquil")
        empleados = cursor.fetchall()
        for emp in empleados:
            print(f"  ID {emp[0]}: {emp[1]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_consultas()
