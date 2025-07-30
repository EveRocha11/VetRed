import pyodbc
from app.config import Config

try:
    # Conectar a la base de datos
    conn = pyodbc.connect(Config.conn_str(), autocommit=True)
    cursor = conn.cursor()
    
    # Verificar si la tabla existe
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'Cliente_Contacto'
    """)
    
    if cursor.fetchone()[0] == 0:
        print("La tabla Cliente_Contacto no existe. Creándola...")
        cursor.execute("""
            CREATE TABLE Cliente_Contacto (
                idCliente INT,
                correo VARCHAR(100),
                direccion VARCHAR(255),
                telefono VARCHAR(20),
                PRIMARY KEY (idCliente, correo)
            );
        """)
        print("Tabla creada exitosamente.")
    
    # Verificar si hay datos
    cursor.execute("SELECT COUNT(*) FROM Cliente_Contacto")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Insertando datos de ejemplo...")
        # Insertar datos de ejemplo
        datos = [
            (1, 'juan.perez@email.com', 'Av. Principal 123, Guayaquil', '+593 99 123 4567'),
            (1, 'juan.trabajo@email.com', 'Av. Principal 123, Guayaquil', '+593 99 123 4567'),
            (2, 'maria.gonzalez@email.com', 'Calle Secundaria 456, Guayaquil', '+593 99 234 5678'),
            (3, 'carlos.rodriguez@email.com', 'Av. de los Libertadores 789, Guayaquil', '+593 99 345 6789'),
            (4, 'ana.silva@email.com', 'Calle Las Flores 321, Guayaquil', '+593 99 456 7890')
        ]
        
        for dato in datos:
            try:
                cursor.execute("""
                    INSERT INTO Cliente_Contacto (idCliente, correo, direccion, telefono) 
                    VALUES (?, ?, ?, ?)
                """, dato)
                print(f"Insertado: Cliente {dato[0]} - {dato[1]}")
            except Exception as e:
                print(f"Error insertando {dato}: {e}")
        
        print("Datos insertados exitosamente.")
    else:
        print(f"La tabla ya tiene {count} registros.")
    
    # Mostrar los datos actuales
    cursor.execute("SELECT * FROM Cliente_Contacto")
    print("\nDatos en la tabla:")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Correo: {row[1]}, Dirección: {row[2]}, Teléfono: {row[3]}")
    
    cursor.close()
    conn.close()
    print("\nScript completado exitosamente.")
    
except Exception as e:
    print(f"Error: {e}")
