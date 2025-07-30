import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil
from datetime import date

def debug_consulta_api():
    """Debug directo de la consulta para empleados"""
    
    hoy = date.today()
    print(f"Fecha de hoy: {hoy}")
    
    # Test directo en la base de datos
    print("\n🔍 PROBANDO CONSULTA DIRECTA EN BASE DE DATOS...")
    
    try:
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        # Para empleado Carlos Pérez (ID: 1)
        empleado_id = 1
        print(f"\n👨‍⚕️ Verificando empleado {empleado_id}...")
        
        # 1. Verificar si el empleado existe
        cursor.execute("SELECT idEmpleado, nombre FROM Empleado_Quito WHERE idEmpleado = ?", (empleado_id,))
        empleado = cursor.fetchone()
        if empleado:
            print(f"  ✅ Empleado encontrado: {empleado[1]} (ID: {empleado[0]})")
        else:
            print(f"  ❌ Empleado no encontrado")
        
        # 2. Verificar consultas para hoy
        query = """
            SELECT 
                c.idConsulta,
                c.fecha,
                c.hora,
                c.motivo,
                c.estado,
                c.observaciones,
                c.idEmpleado,
                c.idMascota,
                m.nombre as mascota_nombre,
                m.especie as mascota_tipo
            FROM Consulta_Quito c
            LEFT JOIN Mascota m ON m.idMascota = c.idMascota
            WHERE c.idEmpleado = ? AND c.fecha = ?
            ORDER BY c.hora
        """
        
        cursor.execute(query, (empleado_id, hoy))
        consultas = cursor.fetchall()
        
        print(f"  📋 Query ejecutada con parámetros: idEmpleado={empleado_id}, fecha={hoy}")
        print(f"  📊 Consultas encontradas: {len(consultas)}")
        
        for i, consulta in enumerate(consultas, 1):
            print(f"    {i}. ID:{consulta[0]} {consulta[1]} {consulta[2]} - {consulta[3]} ({consulta[4]})")
            print(f"       Mascota: {consulta[8] or 'Sin nombre'} ({consulta[9] or 'Sin tipo'})")
        
        cursor.close()
        conn_quito.close()
        
    except Exception as e:
        print(f"❌ Error en consulta directa: {e}")
    
    # Test de la función get_empleado_sede
    print(f"\n🏢 PROBANDO FUNCIÓN get_empleado_sede...")
    
    try:
        from app.repositories.empleado import EmpleadoRepository
        empleado_repo = EmpleadoRepository()
        
        for emp_id in [1, 2, 3, 4, 6]:
            sede = empleado_repo.get_empleado_sede(emp_id)
            print(f"  Empleado {emp_id}: {sede}")
            
    except Exception as e:
        print(f"❌ Error en get_empleado_sede: {e}")
    
    # Test de la función get_by_empleado_fecha
    print(f"\n📋 PROBANDO FUNCIÓN get_by_empleado_fecha...")
    
    try:
        from app.repositories.consulta import ConsultaRepository
        consulta_repo = ConsultaRepository()
        
        for emp_id in [1, 2, 3, 4, 6]:
            print(f"\n  Empleado {emp_id}:")
            consultas = consulta_repo.get_by_empleado_fecha(emp_id, hoy)
            print(f"    Consultas encontradas: {len(consultas)}")
            
            for i, consulta in enumerate(consultas[:3], 1):  # Solo mostrar las primeras 3
                print(f"      {i}. {consulta.get('hora')} - {consulta.get('motivo')}")
            
    except Exception as e:
        print(f"❌ Error en get_by_empleado_fecha: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_consulta_api()
