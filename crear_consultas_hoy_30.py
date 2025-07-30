import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil
from datetime import date, time

def crear_consultas_hoy_30():
    """Crear consultas para el 30 de julio"""
    
    hoy = date.today()  # 2025-07-30
    print(f"Creando consultas para hoy: {hoy}")
    
    try:
        # CONSULTAS PARA QUITO
        print("\n🏢 CREANDO CONSULTAS EN QUITO...")
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        # Obtener el próximo ID disponible
        cursor.execute("SELECT MAX(idConsulta) FROM Consulta_Quito")
        max_id = cursor.fetchone()[0] or 0
        
        consultas_quito = [
            # Carlos Pérez (ID: 1)
            (max_id + 1, hoy, time(9, 0), 'Revisión general', 'Pendiente', None, 1, 1, 1),
            (max_id + 2, hoy, time(11, 30), 'Vacunación anual', 'Pendiente', None, 1, 1, 2),
            (max_id + 3, hoy, time(14, 0), 'Control post-operatorio', 'Completado', 'Mascota recuperándose bien', 1, 1, 3),
            
            # Ana Gómez (ID: 2)
            (max_id + 4, hoy, time(8, 30), 'Consulta de emergencia', 'Pendiente', None, 1, 2, 4),
            (max_id + 5, hoy, time(12, 45), 'Revisión nutricional', 'Pendiente', None, 1, 2, 5),
            (max_id + 6, hoy, time(16, 0), 'Chequeo de rutina', 'Completado', 'Todo normal', 1, 2, 6),
            
            # Luis Martínez (ID: 6)
            (max_id + 7, hoy, time(10, 15), 'Consulta dermatológica', 'Pendiente', None, 1, 6, 7),
            (max_id + 8, hoy, time(15, 30), 'Cirugía menor', 'Pendiente', None, 1, 6, 8),
        ]
        
        for consulta in consultas_quito:
            try:
                cursor.execute("""
                    INSERT INTO Consulta_Quito (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, consulta)
                print(f"  ✅ Consulta creada: Empleado {consulta[7]}, {consulta[2]} - {consulta[3]}")
            except Exception as e:
                print(f"  ❌ Error creando consulta para empleado {consulta[7]}: {e}")
        
        conn_quito.commit()
        cursor.close()
        conn_quito.close()
        
        # CONSULTAS PARA GUAYAQUIL
        print("\n🏢 CREANDO CONSULTAS EN GUAYAQUIL...")
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            # Obtener el próximo ID disponible
            cursor.execute("SELECT MAX(idConsulta) FROM Consulta_Guayaquil")
            max_id_guayaquil = cursor.fetchone()[0] or 0
            
            consultas_guayaquil = [
                # Juan López (ID: 3)
                (max_id_guayaquil + 1, hoy, time(9, 30), 'Consulta preventiva', 'Pendiente', None, 2, 3, 1),
                (max_id_guayaquil + 2, hoy, time(13, 0), 'Revisión general', 'Completado', 'Mascota en buen estado', 2, 3, 2),
                
                # Maria Silva (ID: 4)
                (max_id_guayaquil + 3, hoy, time(10, 45), 'Vacunación', 'Pendiente', None, 2, 4, 3),
                (max_id_guayaquil + 4, hoy, time(14, 30), 'Control de peso', 'Pendiente', None, 2, 4, 4),
                (max_id_guayaquil + 5, hoy, time(17, 0), 'Consulta urgente', 'Completado', 'Atendida satisfactoriamente', 2, 4, 5),
            ]
            
            for consulta in consultas_guayaquil:
                try:
                    cursor.execute("""
                        INSERT INTO Consulta_Guayaquil (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, consulta)
                    print(f"  ✅ Consulta creada: Empleado {consulta[7]}, {consulta[2]} - {consulta[3]}")
                except Exception as e:
                    print(f"  ❌ Error creando consulta para empleado {consulta[7]}: {e}")
            
            conn_guayaquil.commit()
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"❌ Error conectando a Guayaquil: {e}")
        
        print(f"\n✅ Consultas creadas para {hoy}")
        
        # Verificar que se crearon correctamente
        print("\n🔍 VERIFICANDO CONSULTAS CREADAS...")
        
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        for empleado_id in [1, 2, 6]:
            cursor.execute("""
                SELECT COUNT(*) FROM Consulta_Quito 
                WHERE idEmpleado = ? AND fecha = ?
            """, (empleado_id, hoy))
            count = cursor.fetchone()[0]
            print(f"  Empleado {empleado_id} (Quito): {count} consultas para hoy")
        
        cursor.close()
        conn_quito.close()
        
        try:
            conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
            cursor = conn_guayaquil.cursor()
            
            for empleado_id in [3, 4]:
                cursor.execute("""
                    SELECT COUNT(*) FROM Consulta_Guayaquil 
                    WHERE idEmpleado = ? AND fecha = ?
                """, (empleado_id, hoy))
                count = cursor.fetchone()[0]
                print(f"  Empleado {empleado_id} (Guayaquil): {count} consultas para hoy")
            
            cursor.close()
            conn_guayaquil.close()
            
        except Exception as e:
            print(f"❌ Error verificando Guayaquil: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    crear_consultas_hoy_30()
