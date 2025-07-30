import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil
from datetime import date, time

def verificar_empleados_y_consultas():
    """Verificar qué empleados tienen consultas"""
    
    print("=== VERIFICACIÓN DE EMPLEADOS Y SUS CONSULTAS ===")
    
    try:
        # Verificar empleados en Quito
        print("\n🏢 EMPLEADOS EN QUITO:")
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        cursor.execute("SELECT idEmpleado, nombre, idClinica FROM Empleado_Quito ORDER BY idEmpleado")
        empleados_quito = cursor.fetchall()
        
        for emp in empleados_quito:
            print(f"  ID: {emp[0]}, Nombre: {emp[1]}, Clínica: {emp[2]}")
            
            # Verificar consultas para este empleado
            cursor.execute("""
                SELECT COUNT(*) as total, 
                       MIN(fecha) as primera_fecha, 
                       MAX(fecha) as ultima_fecha
                FROM Consulta_Quito 
                WHERE idEmpleado = ?
            """, (emp[0],))
            
            consulta_info = cursor.fetchone()
            if consulta_info[0] > 0:
                print(f"    📋 {consulta_info[0]} consultas (desde {consulta_info[1]} hasta {consulta_info[2]})")
                
                # Ver consultas específicas
                cursor.execute("""
                    SELECT TOP 3 idConsulta, fecha, hora, motivo, estado 
                    FROM Consulta_Quito 
                    WHERE idEmpleado = ?
                    ORDER BY fecha DESC, hora DESC
                """, (emp[0],))
                
                consultas_recientes = cursor.fetchall()
                for cons in consultas_recientes:
                    print(f"      - ID:{cons[0]} {cons[1]} {cons[2]} - {cons[3]} ({cons[4]})")
            else:
                print(f"    ❌ Sin consultas")
        
        cursor.close()
        conn_quito.close()
        
        # Verificar empleados en Guayaquil
        print("\n🏢 EMPLEADOS EN GUAYAQUIL:")
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            cursor.execute("SELECT idEmpleado, nombre, idClinica FROM Empleado_Guayaquil ORDER BY idEmpleado")
            empleados_guayaquil = cursor.fetchall()
            
            for emp in empleados_guayaquil:
                print(f"  ID: {emp[0]}, Nombre: {emp[1]}, Clínica: {emp[2]}")
                
                # Verificar consultas para este empleado
                cursor.execute("""
                    SELECT COUNT(*) as total, 
                           MIN(fecha) as primera_fecha, 
                           MAX(fecha) as ultima_fecha
                    FROM Consulta_Guayaquil 
                    WHERE idEmpleado = ?
                """, (emp[0],))
                
                consulta_info = cursor.fetchone()
                if consulta_info[0] > 0:
                    print(f"    📋 {consulta_info[0]} consultas (desde {consulta_info[1]} hasta {consulta_info[2]})")
                    
                    # Ver consultas específicas
                    cursor.execute("""
                        SELECT TOP 3 idConsulta, fecha, hora, motivo, estado 
                        FROM Consulta_Guayaquil 
                        WHERE idEmpleado = ?
                        ORDER BY fecha DESC, hora DESC
                    """, (emp[0],))
                    
                    consultas_recientes = cursor.fetchall()
                    for cons in consultas_recientes[:3]:  # Solo primeras 3
                        print(f"      - ID:{cons[0]} {cons[1]} {cons[2]} - {cons[3]} ({cons[4]})")
                else:
                    print(f"    ❌ Sin consultas")
            
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"❌ Error conectando a Guayaquil: {e}")
        
        # Crear consultas de prueba para otros empleados
        print("\n🔧 CREANDO CONSULTAS DE PRUEBA PARA OTROS EMPLEADOS...")
        
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        hoy = date.today()
        
        # Obtener el próximo ID disponible
        cursor.execute("SELECT MAX(idConsulta) FROM Consulta_Quito")
        max_id = cursor.fetchone()[0] or 0
        
        # Consultas para Ana Gómez (ID: 2)
        consultas_ana = [
            (max_id + 8, hoy, time(8, 30), 'Consulta preventiva', 'Pendiente', None, 1, 2, 1),
            (max_id + 9, hoy, time(12, 0), 'Revisión post-operatoria', 'Completado', 'Recuperación exitosa', 1, 2, 3),
            (max_id + 10, hoy, time(16, 30), 'Consulta de emergencia', 'Pendiente', None, 1, 2, 5),
        ]
        
        # Consultas para Luis Martínez (ID: 6)
        consultas_luis = [
            (max_id + 11, hoy, time(9, 15), 'Control de peso', 'Pendiente', None, 1, 6, 2),
            (max_id + 12, hoy, time(13, 45), 'Consulta nutricional', 'Pendiente', None, 1, 6, 4),
            (max_id + 13, hoy, time(17, 0), 'Chequeo anual', 'Completado', 'Mascota en excelente estado', 1, 6, 6),
        ]
        
        todas_consultas = consultas_ana + consultas_luis
        
        for consulta in todas_consultas:
            try:
                cursor.execute("""
                    INSERT INTO Consulta_Quito (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, consulta)
                print(f"  ✅ Consulta creada: Empleado {consulta[7]}, {consulta[1]} {consulta[2]}")
            except Exception as e:
                print(f"  ❌ Error creando consulta para empleado {consulta[7]}: {e}")
        
        conn_quito.commit()
        cursor.close()
        conn_quito.close()
        
        print(f"\n✅ Proceso completado. Se intentaron crear {len(todas_consultas)} consultas adicionales.")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    verificar_empleados_y_consultas()
