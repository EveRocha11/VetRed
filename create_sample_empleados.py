import pyodbc
from app.config import ConfigQuito
from datetime import date

def create_sample_empleados():
    """Crear empleados de ejemplo para probar el sistema"""
    
    try:
        conn = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn.cursor()
        
        # Verificar si la tabla Empleado existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Empleado'
        """)
        
        if cursor.fetchone()[0] == 0:
            # Crear tabla Empleado si no existe
            cursor.execute("""
                CREATE TABLE Empleado (
                    idEmpleado INT PRIMARY KEY,
                    nombre NVARCHAR(100) NOT NULL,
                    direccion NVARCHAR(255),
                    salario DECIMAL(10,2),
                    fechaContratacion DATE NOT NULL,
                    idClinica INT NOT NULL
                )
            """)
            print("✅ Tabla Empleado creada")
        
        # Verificar si ya hay empleados
        cursor.execute("SELECT COUNT(*) FROM Empleado")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar empleados de ejemplo
            empleados_ejemplo = [
                (123, 'María González', 'Av. 6 de Diciembre 123, Quito', 1500.00, date(2023, 1, 15), 1),
                (124, 'Carlos Mendoza', 'Av. República 456, Quito', 1400.00, date(2023, 3, 10), 1),
                (125, 'Ana Rodríguez', 'Calle Amazonas 789, Quito', 1600.00, date(2022, 11, 5), 1),
                (201, 'Pedro Álvarez', 'Av. 9 de Octubre 321, Guayaquil', 1450.00, date(2023, 2, 20), 2),
                (202, 'Laura Jiménez', 'Malecón 2000, Guayaquil', 1550.00, date(2023, 4, 12), 2)
            ]
            
            for empleado in empleados_ejemplo:
                cursor.execute("""
                    INSERT INTO Empleado (idEmpleado, nombre, direccion, salario, fechaContratacion, idClinica)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, empleado)
            
            conn.commit()
            print(f"✅ Se insertaron {len(empleados_ejemplo)} empleados de ejemplo")
            print("Empleados creados:")
            for emp in empleados_ejemplo:
                print(f"  - ID {emp[0]}: {emp[1]} (Clínica {emp[5]})")
        else:
            print(f"ℹ️ Ya existen {count} empleados en la base de datos")
            # Mostrar empleados existentes
            cursor.execute("SELECT idEmpleado, nombre, idClinica FROM Empleado")
            empleados = cursor.fetchall()
            print("Empleados existentes:")
            for emp in empleados:
                print(f"  - ID {emp[0]}: {emp[1]} (Clínica {emp[2]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creando empleados de ejemplo: {e}")

if __name__ == "__main__":
    create_sample_empleados()
