import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil
from datetime import date, time

def create_sample_consultas():
    """Crear consultas de ejemplo para probar el sistema"""
    
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Verificar si la tabla Consulta existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Consulta'
        """)
        
        if cursor.fetchone()[0] == 0:
            # Crear tabla Consulta si no existe
            cursor.execute("""
                CREATE TABLE Consulta (
                    idConsulta INT PRIMARY KEY,
                    fecha DATE NOT NULL,
                    hora TIME NOT NULL,
                    motivo NVARCHAR(255) NOT NULL,
                    estado NVARCHAR(50) NOT NULL DEFAULT 'Pendiente',
                    observaciones NVARCHAR(500),
                    idClinica INT NOT NULL,
                    idEmpleado INT NOT NULL,
                    idMascota INT NOT NULL
                )
            """)
            print("✅ Tabla Consulta creada")
        
        # Verificar si ya hay consultas
        cursor.execute("SELECT COUNT(*) FROM Consulta")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar consultas de ejemplo para hoy
            hoy = date.today()
            
            consultas_ejemplo = [
                (101, hoy, time(9, 0), 'Revisión general', 'Completado', 'Paciente en buen estado', 1, 1, 1001),
                (102, hoy, time(10, 30), 'Vacunación', 'Completado', 'Vacunas aplicadas correctamente', 1, 1, 1002),
                (103, hoy, time(11, 45), 'Control de rutina', 'Pendiente', None, 1, 1, 1003),
                (104, hoy, time(14, 0), 'Consulta por dolor', 'Pendiente', None, 1, 1, 1004),
                (105, hoy, time(15, 30), 'Cirugía menor', 'Pendiente', None, 1, 1, 1005),
                # Consultas para empleado ID 2
                (106, hoy, time(9, 30), 'Examen de laboratorio', 'Pendiente', None, 1, 2, 1006),
                (107, hoy, time(11, 0), 'Consulta dermatológica', 'Pendiente', None, 1, 2, 1007),
                (108, hoy, time(16, 0), 'Revisión post-operatoria', 'Pendiente', None, 1, 2, 1008),
                # Consultas para empleado ID 3
                (109, hoy, time(8, 30), 'Consulta de emergencia', 'Completado', 'Atendido correctamente', 2, 3, 1009),
                (110, hoy, time(13, 30), 'Control de peso', 'Pendiente', None, 2, 3, 1010)
            ]
            
            for consulta in consultas_ejemplo:
                cursor.execute("""
                    INSERT INTO Consulta (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, consulta)
            
            conn.commit()
            print(f"✅ Se insertaron {len(consultas_ejemplo)} consultas de ejemplo")
        else:
            print(f"ℹ️ Ya existen {count} consultas en la base de datos")
            
            # Verificar si hay consultas para hoy
            hoy = date.today()
            cursor.execute("SELECT COUNT(*) FROM Consulta WHERE fecha = ?", (hoy,))
            consultas_hoy = cursor.fetchone()[0]
            
            if consultas_hoy == 0:
                print(f"No hay consultas para hoy ({hoy}). Agregando consultas para hoy...")
                
                # Encontrar el próximo ID disponible
                cursor.execute("SELECT MAX(idConsulta) FROM Consulta")
                max_id = cursor.fetchone()[0] or 0
                
                consultas_hoy_ejemplo = [
                    (max_id + 1, hoy, time(9, 0), 'Revisión general', 'Completado', 'Paciente en buen estado', 1, 1, 1),
                    (max_id + 2, hoy, time(10, 30), 'Vacunación', 'Completado', 'Vacunas aplicadas correctamente', 1, 1, 2),
                    (max_id + 3, hoy, time(11, 45), 'Control de rutina', 'Pendiente', None, 1, 1, 3),
                    (max_id + 4, hoy, time(14, 0), 'Consulta por dolor', 'Pendiente', None, 1, 1, 4),
                    (max_id + 5, hoy, time(15, 30), 'Cirugía menor', 'Pendiente', None, 1, 1, 5),
                    # Consultas para empleado ID 2
                    (max_id + 6, hoy, time(9, 30), 'Examen de laboratorio', 'Pendiente', None, 1, 2, 1),
                    (max_id + 7, hoy, time(11, 0), 'Consulta dermatológica', 'Pendiente', None, 1, 2, 2),
                    (max_id + 8, hoy, time(16, 0), 'Revisión post-operatoria', 'Pendiente', None, 1, 2, 3),
                ]
                
                for consulta in consultas_hoy_ejemplo:
                    cursor.execute("""
                        INSERT INTO Consulta (idConsulta, fecha, hora, motivo, estado, observaciones, idClinica, idEmpleado, idMascota)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, consulta)
                
                conn.commit()
                print(f"✅ Se agregaron {len(consultas_hoy_ejemplo)} consultas para hoy")
            else:
                print(f"Ya hay {consultas_hoy} consultas programadas para hoy")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creando consultas de ejemplo: {e}")

if __name__ == "__main__":
    create_sample_consultas()
