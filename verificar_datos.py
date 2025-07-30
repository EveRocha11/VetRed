import pyodbc
from app.config import ConfigQuito
from datetime import date

def verificar_datos():
    """Verificar qué datos tenemos en las tablas"""
    
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        print("=== VERIFICACIÓN DE DATOS ===\n")
        
        # Verificar empleados
        print("🔍 EMPLEADOS:")
        cursor.execute("SELECT idEmpleado, nombre, idClinica FROM Empleado ORDER BY idEmpleado")
        empleados = cursor.fetchall()
        if empleados:
            for emp in empleados:
                print(f"  - ID {emp[0]}: {emp[1]} (Clínica {emp[2]})")
        else:
            print("  No hay empleados en la base de datos")
        
        print(f"\nTotal empleados: {len(empleados)}\n")
        
        # Verificar consultas
        print("🔍 CONSULTAS:")
        hoy = date.today()
        cursor.execute("""
            SELECT idConsulta, fecha, hora, motivo, estado, idEmpleado, idMascota 
            FROM Consulta 
            WHERE fecha = ?
            ORDER BY idEmpleado, hora
        """, (hoy,))
        consultas = cursor.fetchall()
        
        if consultas:
            print(f"Consultas para hoy ({hoy}):")
            for consulta in consultas:
                print(f"  - Consulta {consulta[0]}: {consulta[2]} - {consulta[3]} (Empleado: {consulta[5]}, Estado: {consulta[4]})")
        else:
            print(f"  No hay consultas para hoy ({hoy})")
            
            # Verificar si hay consultas en otras fechas
            cursor.execute("SELECT COUNT(*), MIN(fecha), MAX(fecha) FROM Consulta")
            result = cursor.fetchone()
            if result[0] > 0:
                print(f"  Hay {result[0]} consultas en total (desde {result[1]} hasta {result[2]})")
            else:
                print("  No hay consultas en la base de datos")
        
        print(f"\nTotal consultas para hoy: {len(consultas)}\n")
        
        # Verificar clientes info
        print("🔍 CLIENTES INFO:")
        cursor.execute("SELECT COUNT(*), MIN(idCliente), MAX(idCliente) FROM Cliente_Info")
        result = cursor.fetchone()
        print(f"  Total clientes: {result[0]} (IDs del {result[1]} al {result[2]})")
        
        # Mostrar algunos clientes
        cursor.execute("SELECT TOP 5 idCliente, nombre, correo FROM Cliente_Info")
        clientes = cursor.fetchall()
        if clientes:
            print("  Algunos clientes:")
            for cliente in clientes:
                print(f"    - {cliente[0]}: {cliente[1]} ({cliente[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")

if __name__ == "__main__":
    verificar_datos()
