import pyodbc
from app.config import ConfigQuito
from datetime import date, time

def verificar_y_crear_consultas_hoy():
    """Verificar consultas para hoy y crear algunas si no existen"""
    
    hoy = date.today()  # 2025-07-29
    print(f"Fecha de hoy: {hoy}")
    
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Ver todas las consultas para el empleado Carlos Pérez (ID: 1)
        print("\n=== CONSULTAS EXISTENTES PARA EMPLEADO ID 1 (Carlos Pérez) ===")
        cursor.execute("""
            SELECT idConsulta, fecha, hora, motivo, estado, idEmpleado, idMascota
            FROM Consulta_Quito 
            WHERE idEmpleado = 1
            ORDER BY fecha, hora
        """)
        consultas = cursor.fetchall()
        
        if consultas:
            print("Consultas encontradas:")
            for consulta in consultas:
                print(f"  ID: {consulta[0]}, Fecha: {consulta[1]}, Hora: {consulta[2]}, Motivo: {consulta[3]}, Estado: {consulta[4]}")
        else:
            print("No hay consultas para el empleado ID 1")
        
        # Verificar consultas para hoy específicamente
        print(f"\n=== CONSULTAS PARA HOY ({hoy}) ===")
        cursor.execute("""
            SELECT idConsulta, fecha, hora, motivo, estado, idEmpleado, idMascota
            FROM Consulta_Quito 
            WHERE fecha = ?
            ORDER BY hora
        """, (hoy,))
        consultas_hoy = cursor.fetchall()
        
        if consultas_hoy:
            print("Consultas para hoy:")
            for consulta in consultas_hoy:
                print(f"  ID: {consulta[0]}, Empleado: {consulta[5]}, Hora: {consulta[2]}, Motivo: {consulta[3]}")
        else:
            print("No hay consultas programadas para hoy")
            
            # Crear consultas para hoy
            print("\nCreando consultas para hoy...")
            
            # Obtener el próximo ID disponible
            cursor.execute("SELECT MAX(idConsulta) FROM Consulta_Quito")
            max_id = cursor.fetchone()[0] or 0
            
            consultas_nuevas = [
                (max_id + 1, hoy, time(9, 0), 'Revisión general', 'Pendiente', None, 1, 1, 1),
                (max_id + 2, hoy, time(10, 30), 'Vacunación', 'Pendiente', None, 1, 1, 2),
                (max_id + 3, hoy, time(11, 45), 'Control de rutina', 'Completado', 'Mascota en buen estado', 1, 1, 3),
                (max_id + 4, hoy, time(14, 0), 'Consulta por dolor', 'Pendiente', None, 1, 1, 4),
                (max_id + 5, hoy, time(15, 30), 'Cirugía menor', 'Pendiente', None, 1, 1, 5),
                # Consultas para otro empleado también
                (max_id + 6, hoy, time(9, 30), 'Examen de laboratorio', 'Pendiente', None, 1, 2, 6),
                (max_id + 7, hoy, time(16, 0), 'Consulta dermatológica', 'Pendiente', None, 1, 2, 7),
            ]
            
            for consulta in consultas_nuevas:
                cursor.execute("""
                    INSERT INTO Consulta_Quito (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, consulta)
            
            conn.commit()
            print(f"✅ Se crearon {len(consultas_nuevas)} consultas para hoy")
            
            # Verificar que se crearon
            cursor.execute("""
                SELECT idConsulta, fecha, hora, motivo, estado, idEmpleado, idMascota
                FROM Consulta_Quito 
                WHERE fecha = ? AND idEmpleado = 1
                ORDER BY hora
            """, (hoy,))
            consultas_verificacion = cursor.fetchall()
            
            print(f"\nConsultas para empleado ID 1 en {hoy}:")
            for consulta in consultas_verificacion:
                print(f"  ID: {consulta[0]}, Hora: {consulta[2]}, Motivo: {consulta[3]}, Estado: {consulta[4]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_y_crear_consultas_hoy()
