import pyodbc
from app.config import ConfigQuito
from datetime import date, time

def crear_consultas_hoy():
    """Crear consultas específicamente para hoy"""
    
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        hoy = date.today()
        print(f"Creando consultas para: {hoy}")
        
        # Verificar si ya existen consultas para hoy
        cursor.execute("SELECT COUNT(*) FROM Consulta WHERE fecha = ?", (hoy,))
        consultas_existentes = cursor.fetchone()[0]
        
        if consultas_existentes > 0:
            print(f"Ya existen {consultas_existentes} consultas para hoy. Eliminándolas primero...")
            cursor.execute("DELETE FROM Consulta WHERE fecha = ?", (hoy,))
        
        # Encontrar el próximo ID disponible
        cursor.execute("SELECT ISNULL(MAX(idConsulta), 0) + 1 FROM Consulta")
        next_id = cursor.fetchone()[0]
        
        print(f"Próximo ID de consulta: {next_id}")
        
        # Crear consultas para empleados específicos
        consultas_hoy = [
            # Consultas para empleado ID 1 (Carlos Pérez)
            (next_id, hoy, time(9, 0), 'Revisión general', 'Completado', 'Paciente en buen estado', 1, 1, 1),
            (next_id + 1, hoy, time(10, 30), 'Vacunación', 'Completado', 'Vacunas aplicadas correctamente', 1, 1, 2),
            (next_id + 2, hoy, time(11, 45), 'Control de rutina', 'Pendiente', None, 1, 1, 3),
            (next_id + 3, hoy, time(14, 0), 'Consulta por dolor', 'Pendiente', None, 1, 1, 4),
            (next_id + 4, hoy, time(15, 30), 'Cirugía menor', 'Pendiente', None, 1, 1, 5),
            
            # Consultas para empleado ID 2 (Ana Gómez)
            (next_id + 5, hoy, time(9, 30), 'Examen de laboratorio', 'Pendiente', None, 1, 2, 1),
            (next_id + 6, hoy, time(11, 0), 'Consulta dermatológica', 'Pendiente', None, 1, 2, 2),
            (next_id + 7, hoy, time(16, 0), 'Revisión post-operatoria', 'Pendiente', None, 1, 2, 3),
            
            # Consultas para empleado ID 3 (Juan López) - Clínica 2
            (next_id + 8, hoy, time(8, 30), 'Consulta de emergencia', 'Completado', 'Atendido correctamente', 2, 3, 1),
            (next_id + 9, hoy, time(13, 30), 'Control de peso', 'Pendiente', None, 2, 3, 2),
        ]
        
        for consulta in consultas_hoy:
            cursor.execute("""
                INSERT INTO Consulta (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, consulta)
            print(f"  ✅ Consulta {consulta[0]} creada: {consulta[2]} - {consulta[3]} (Empleado {consulta[7]})")
        
        conn.commit()
        print(f"\n✅ Se crearon {len(consultas_hoy)} consultas para hoy ({hoy})")
        
        # Verificar las consultas creadas
        cursor.execute("""
            SELECT c.idConsulta, c.hora, c.motivo, c.estado, c.idEmpleado, e.nombre
            FROM Consulta c
            LEFT JOIN Empleado e ON c.idEmpleado = e.idEmpleado
            WHERE c.fecha = ?
            ORDER BY c.idEmpleado, c.hora
        """, (hoy,))
        
        consultas_verificacion = cursor.fetchall()
        print(f"\n🔍 VERIFICACIÓN - Consultas para {hoy}:")
        for consulta in consultas_verificacion:
            print(f"  - ID {consulta[0]}: {consulta[1]} - {consulta[2]} (Empleado {consulta[4]}: {consulta[5]}) [{consulta[3]}]")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creando consultas: {e}")

if __name__ == "__main__":
    crear_consultas_hoy()
