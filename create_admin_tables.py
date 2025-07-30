import pyodbc
from app.config import ConfigQuito, ConfigGuayaquil

def create_admin_tables():
    """Crear tablas de administradores para ambas sedes"""
    
    # Crear tabla Admin_Quito
    try:
        conn_quito = pyodbc.connect(ConfigQuito.conn_str())
        cursor = conn_quito.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Admin_Quito'
        """)
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                CREATE TABLE Admin_Quito (
                    idAdmin INT PRIMARY KEY,
                    nombre NVARCHAR(100) NOT NULL,
                    correo NVARCHAR(100) NOT NULL,
                    idClinica INT NOT NULL DEFAULT 1
                )
            """)
            
            # Insertar datos de ejemplo
            cursor.execute("""
                INSERT INTO Admin_Quito (idAdmin, nombre, correo, idClinica) VALUES
                (1001, 'Carlos Administrador', 'carlos.admin@vetred.com', 1),
                (1002, 'Ana Gerente', 'ana.gerente@vetred.com', 1)
            """)
            
            conn_quito.commit()
            print("✅ Tabla Admin_Quito creada exitosamente con datos de ejemplo")
        else:
            print("ℹ️ Tabla Admin_Quito ya existe")
            
        cursor.close()
        conn_quito.close()
        
    except Exception as e:
        print(f"❌ Error creando tabla Admin_Quito: {e}")
    
    # Crear tabla Admin_Guayaquil
    try:
        conn_guayaquil = pyodbc.connect(ConfigGuayaquil.conn_str())
        cursor = conn_guayaquil.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Admin_Guayaquil'
        """)
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                CREATE TABLE Admin_Guayaquil (
                    idAdmin INT PRIMARY KEY,
                    nombre NVARCHAR(100) NOT NULL,
                    correo NVARCHAR(100) NOT NULL,
                    idClinica INT NOT NULL DEFAULT 2
                )
            """)
            
            # Insertar datos de ejemplo
            cursor.execute("""
                INSERT INTO Admin_Guayaquil (idAdmin, nombre, correo, idClinica) VALUES
                (2001, 'Pedro Administrador', 'pedro.admin@vetred.com', 2),
                (2002, 'María Supervisora', 'maria.supervisora@vetred.com', 2)
            """)
            
            conn_guayaquil.commit()
            print("✅ Tabla Admin_Guayaquil creada exitosamente con datos de ejemplo")
        else:
            print("ℹ️ Tabla Admin_Guayaquil ya existe")
            
        cursor.close()
        conn_guayaquil.close()
        
    except Exception as e:
        print(f"❌ Error creando tabla Admin_Guayaquil: {e}")

if __name__ == "__main__":
    create_admin_tables()
